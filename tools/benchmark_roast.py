"""Local headless measurements. Synthetic fixture only; not a hosted performance claim."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import sys
import time
from uuid import UUID

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'roast-web'))
started = time.perf_counter()
from cocoaroast.models import RoastSession, Sample
from cocoaroast.engine import analyze
from cocoaroast.plotting import render_svg
import_seconds = time.perf_counter() - started

session = RoastSession(owner_user_id=UUID('00000000-0000-4000-8000-000000000001'),
    name='Synthetic software replay fixture', source_kind='mock_replay',
    samples=[Sample(elapsed_seconds=i, bean_temperature=25 + i / 20,
                    environment_temperature=150 + i / 100) for i in range(1800)])
def measure(_):
    start = time.perf_counter()
    analyze(session)
    analyzed = time.perf_counter()
    image = render_svg(session)
    return {'analysis_seconds': analyzed - start, 'total_seconds': time.perf_counter() - start,
            'svg_bytes': len(image)}

first = measure(None)
with ThreadPoolExecutor(max_workers=5) as pool:
    concurrent = list(pool.map(measure, range(5)))
result = {'environment': 'Local Windows Python 3.12, not Vercel', 'samples': 1800,
          'import_seconds': import_seconds, 'first_request': first,
          'five_concurrent_requests': concurrent,
          'limitations': 'No hosted cold-start, HTTP/auth latency, memory retention or deployed bundle measurement'}
out = ROOT / 'docs/roast/local-benchmark.json'
out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, indent=2))
