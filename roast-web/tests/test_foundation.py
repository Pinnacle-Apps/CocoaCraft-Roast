import ast
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
from uuid import UUID, uuid4
import numpy

WEB = Path(__file__).resolve().parents[1]
ROOT = WEB.parent
sys.path.insert(0, str(WEB))
from cocoaroast.models import RoastSession, Sample, ProductionLink
from cocoaroast.profiles import import_artisan, original_artisan_text
from cocoaroast.engine import analyze
from cocoaroast.adapters import MemorySessionRepository, MockProductionAdapter, MockReplayAdapter
from cocoaroast.references import CuratedReference, ReferenceCatalog
from cocoaroast.vendor.artisan_ror import ArtisanRoR

USER = UUID('00000000-0000-4000-8000-000000000001')
OTHER = UUID('00000000-0000-4000-8000-000000000002')
PROFILE = "{'title': 'Test cacao', 'mode': 'C', 'timex': [-2, 0, 2, 4], 'temp1': [140, 141, 142, 143], 'temp2': [25, 26, -1, 28], 'timeindex': [1, 0, 0, 0, 0, 0, 3, 0], 'unknown': ('preserve', 7)}"


class CoreTests(unittest.TestCase):
    def test_verbatim_source_and_numerical_parity(self):
        spec = importlib.util.spec_from_file_location('extract_ror', ROOT / 'tools/extract_ror.py')
        extractor = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(extractor)
        expected, _ = extractor.extract()
        self.assertEqual(expected, (WEB / 'cocoaroast/vendor/artisan_ror.py').read_text(encoding='utf-8'))
        source_tree = ast.parse((ROOT / 'src/artisanlib/canvas.py').read_text(encoding='utf-8'))
        methods = [n for n in ast.walk(source_tree) if isinstance(n, ast.FunctionDef) and n.name in extractor.NAMES]
        oracle_class = ast.ClassDef(name='Oracle', bases=[], keywords=[], body=methods, decorator_list=[])
        module = ast.fix_missing_locations(ast.Module(body=[oracle_class], type_ignores=[]))
        import warnings, logging
        namespace = {'numpy': numpy, 'warnings': warnings, '_log': logging.getLogger('oracle')}
        exec(compile(module, 'Artisan-original-methods', 'exec'), namespace)
        rng = numpy.random.default_rng(721)
        for polyfit in (False, True):
            for window in (1, 3, 5, 12):
                times = numpy.cumsum(rng.uniform(.4, 2, 80)).tolist()
                readings = (numpy.arange(80) * .3 + rng.normal(0, .1, 80)).tolist()
                readings[20], readings[21], readings[36] = -1, -1, -1
                oracle = namespace['Oracle']()
                oracle.polyfitRoRcalc = polyfit
                actual = ArtisanRoR(polyfit)
                previous = []
                for i in range(1, len(times)+1):
                    want = oracle.compute_ror(readings[i-1], times[:i], readings[:i], previous, window)
                    got = actual.compute_ror(readings[i-1], times[:i], readings[:i], previous, window)
                    self.assertEqual(got, want)
                    previous.append(want)

    def test_linear_ror_units_and_dropouts(self):
        for polyfit in (False, True):
            session = RoastSession(owner_user_id=USER, settings={'ror_method': 'artisan_polyfit' if polyfit else 'artisan_simple'},
                samples=[Sample(elapsed_seconds=t, bean_temperature=20 + t / 6) for t in range(20)])
            data = analyze(session)
            self.assertAlmostEqual(data['bean_ror'][-1], 10, places=8)
            session.samples.append(Sample(elapsed_seconds=20, bean_temperature=None))
            self.assertEqual(analyze(session)['bean_ror'][-1], data['bean_ror'][-1])

    def test_lossless_source_and_session_roundtrip(self):
        session = import_artisan(PROFILE, USER)
        self.assertIsNone(session.samples[2].bean_temperature)
        self.assertEqual([e.kind for e in session.events], ['charge', 'drop'])
        restored = RoastSession.model_validate_json(session.model_dump_json())
        self.assertEqual(original_artisan_text(restored), PROFILE)
        self.assertEqual(restored, session)

    def test_invalid_profiles(self):
        for source in ("__import__('os').system('echo unsafe')", '[1,2]',
                       '{"timex":[0,0],"temp1":[1,2],"temp2":[3,4]}',
                       '{"timex":[0,1],"temp1":[1],"temp2":[3,4]}',
                       '{"timex":[0,1],"temp1":[NaN,2],"temp2":[3,4]}'):
            with self.subTest(source=source), self.assertRaises((ValueError, SyntaxError)):
                import_artisan(source, USER)

    def test_upstream_profile_corpus(self):
        paths = list((ROOT / 'src/test').rglob('*.alog'))
        self.assertGreaterEqual(len(paths), 5)
        for path in paths:
            with self.subTest(path=path.name):
                text = path.read_text(encoding='utf-8-sig')
                session = import_artisan(text, USER)
                self.assertEqual(original_artisan_text(session), text)
                self.assertEqual(len(analyze(session)['bean_ror']), len(session.samples))

    def test_mock_scope_and_unified_record(self):
        session = import_artisan(PROFILE, USER)
        run = uuid4()
        adapter = MockProductionAdapter({run: USER})
        linked = adapter.link(session, ProductionLink(production_run_id=run))
        self.assertEqual(set(session.model_dump()), set(linked.model_dump()))
        self.assertEqual(linked.samples, session.samples)
        with self.assertRaises(PermissionError):
            adapter.link(session.model_copy(update={'owner_user_id': OTHER}), linked.production_link)
        repo = MemorySessionRepository()
        repo.save(linked)
        with self.assertRaises(PermissionError):
            repo.get(linked.id, OTHER)
        loaded = repo.get(linked.id, USER)
        loaded.name = 'changed'
        self.assertNotEqual(repo.get(linked.id, USER).name, loaded.name)
        self.assertEqual(len(MockReplayAdapter().read(session, 0)), 2)

    def test_reference_copies_are_editable_and_isolated(self):
        original = import_artisan(PROFILE, OTHER)
        ref = CuratedReference(id='test-fixture', source_citation='Synthetic test fixture, not guidance',
            reviewed_by='test runner', reviewed_at=datetime.now(timezone.utc),
            applicability='Tests only', session=original)
        catalog = ReferenceCatalog([ref])
        first = catalog.copy_for_user(ref.id, USER)
        first.samples[0].bean_temperature = 999
        second = catalog.copy_for_user(ref.id, USER)
        self.assertNotEqual(second.samples[0].bean_temperature, 999)
        self.assertNotEqual(first.id, second.id)
        self.assertIsNone(second.production_link)


class ApiTests(unittest.TestCase):
    def setUp(self):
        from fastapi.testclient import TestClient
        from cocoaroast.api import app
        self.app = app
        self.client = TestClient(app)

    def tearDown(self):
        self.app.dependency_overrides.clear()
        self.client.close()

    def authenticate(self):
        from cocoaroast.auth import require_account
        self.app.dependency_overrides[require_account] = lambda: USER

    def test_standalone_workspace_is_available_without_account(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('CocoaCraft Roast', response.text)
        self.assertIn('cocoacraft-roast-workspace/v1', response.text)
        self.assertIn('Export workspace JSON', response.text)
        self.assertIn('Manual temperature readings', response.text)
        self.assertIn('Milestones and manual checks', response.text)
        self.assertIn('No automatic quality acceptance', response.text)
        self.assertEqual(response.headers['cache-control'], 'no-store')

    def test_fail_closed_for_every_private_route(self):
        self.assertEqual(self.client.get('/api/health').status_code, 200)
        for path in ('import', 'validate', 'analyze', 'chart.svg', 'export', 'original.alog'):
            self.assertEqual(self.client.post('/api/v1/sessions/' + path, json={}).status_code, 401)
        self.assertEqual(self.client.get('/api/v1/reference-profiles').status_code, 401)
        with patch.dict('os.environ', {}, clear=True):
            self.assertEqual(self.client.get('/api/v1/reference-profiles', headers={'Authorization': 'Bearer invalid'}).status_code, 503)

    def test_auth_validated_upstream_and_anonymous_rejected(self):
        headers = {'Authorization': 'Bearer user-token'}
        with patch.dict('os.environ', {'COCOACRAFT_SUPABASE_URL': 'https://test.supabase.co',
                                     'COCOACRAFT_SUPABASE_PUBLISHABLE_KEY': 'test-key'}, clear=True):
            with patch('cocoaroast.auth.httpx.Client') as mock_client:
                response = mock_client.return_value.__enter__.return_value.get.return_value
                response.status_code = 200
                response.json.return_value = {'id': str(USER), 'is_anonymous': False}
                self.assertEqual(self.client.get('/api/v1/reference-profiles', headers=headers).status_code, 200)
                response.json.return_value = {'id': str(USER), 'is_anonymous': True}
                self.assertEqual(self.client.get('/api/v1/reference-profiles', headers=headers).status_code, 401)
                response.status_code = 401
                self.assertEqual(self.client.get('/api/v1/reference-profiles', headers=headers).status_code, 401)

    def test_import_analyze_render_export_and_isolation(self):
        self.authenticate()
        result = self.client.post('/api/v1/sessions/import', json={'profile_text': PROFILE})
        self.assertEqual(result.status_code, 200)
        session = result.json()
        self.assertEqual(self.client.post('/api/v1/sessions/analyze', json=session).status_code, 200)
        chart = self.client.post('/api/v1/sessions/chart.svg', json=session)
        self.assertEqual(chart.status_code, 200)
        self.assertIn('<svg', chart.text)
        self.assertEqual(chart.headers['cache-control'], 'no-store')
        self.assertEqual(self.client.post('/api/v1/sessions/export', json=session).json(), session)
        self.assertEqual(self.client.post('/api/v1/sessions/original.alog', json=session).text, PROFILE)
        session['owner_user_id'] = str(OTHER)
        self.assertEqual(self.client.post('/api/v1/sessions/analyze', json=session).status_code, 403)

    def test_oversize_streams_and_no_live_production_link(self):
        self.authenticate()
        self.assertEqual(self.client.post('/api/v1/sessions/import', content=b'x' * 2000001).status_code, 413)
        session = import_artisan(PROFILE, USER)
        session.production_link = ProductionLink(production_run_id=uuid4())
        self.assertEqual(self.client.post('/api/v1/sessions/analyze', json=session.model_dump(mode='json')).status_code, 501)
        session.production_link.adapter = 'cocoacraft'
        linked = self.client.post('/api/v1/sessions/analyze', json=session.model_dump(mode='json'))
        self.assertEqual(linked.status_code, 200)
        session.owner_user_id = OTHER
        self.assertEqual(self.client.post('/api/v1/sessions/analyze', json=session.model_dump(mode='json')).status_code, 403)

    def test_concurrent_rendering_and_title_escaping(self):
        from cocoaroast.plotting import render_svg
        session = import_artisan(PROFILE, USER)
        session.name = '<script>alert(1)</script>'
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(render_svg, [session] * 4))
        for result in results:
            self.assertIn(b'<svg', result)
            self.assertNotIn(b'<script>', result)


if __name__ == '__main__':
    unittest.main()
