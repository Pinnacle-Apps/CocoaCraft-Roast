"""Stateless software service. SPDX-License-Identifier: AGPL-3.0-or-later."""
from uuid import UUID
from pathlib import Path
import os
import re
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
from pydantic import Field
from .auth import require_account
from .engine import analyze
from .models import Model, RoastSession
from .plotting import render_svg
from .profiles import import_artisan, original_artisan_text
from .references import catalog


class BodyLimitMiddleware:
    """Bound actual streamed bytes before JSON/AST parsing."""
    def __init__(self, app, limit=2000000):
        self.app, self.limit = app, limit

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)
        chunks, size = [], 0
        while True:
            message = await receive()
            if message['type'] == 'http.disconnect':
                return
            chunk = message.get('body', b'')
            size += len(chunk)
            if size > self.limit:
                return await JSONResponse({'detail': 'Request exceeds 2 MB'}, status_code=413)(scope, receive, send)
            chunks.append(chunk)
            if not message.get('more_body', False):
                break
        sent = False
        async def buffered_receive():
            nonlocal sent
            if not sent:
                sent = True
                return {'type': 'http.request', 'body': b''.join(chunks), 'more_body': False}
            return await receive()
        await self.app(scope, buffered_receive, send)


app = FastAPI(title='CocoaCraft Roast', version='0.2.0')
app.add_middleware(BodyLimitMiddleware)


@app.middleware('http')
async def response_policy(request: Request, call_next):
    response = await call_next(request)
    response.headers['Cache-Control'] = 'no-store'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'no-referrer'
    return response


class TargetPoint(Model):
    minute: float = Field(ge=0, le=240)
    bean: float = Field(ge=-20, le=500)


class ChartRequest(Model):
    session: RoastSession
    target_points: list[TargetPoint] = Field(default_factory=list, max_length=16)
    replay_until: float | None = Field(default=None, ge=0, le=14400)


class ImportRequest(Model):
    profile_text: str = Field(max_length=1000000)


def owned_session(session: RoastSession, owner: UUID) -> RoastSession:
    if session.owner_user_id != owner:
        raise HTTPException(403, 'Session belongs to another account')
    if session.production_link is not None and session.production_link.adapter == 'mock':
        raise HTTPException(501, 'Production linking is only available in the local mock adapter at this stage')
    # CocoaCraft verifies/persists the actual relational link with its own RLS.
    # This stateless service only calculates from the owner-supplied document.
    return session


@app.get('/api/health')
def health():
    return {'status': 'ok', 'service': 'cocoacraft-roast', 'mode': 'software-foundation',
            'persistence': 'client-owned-export', 'hardware': False, 'ai': False}


@app.get('/api/source')
def source():
    revision = os.environ.get('VERCEL_GIT_COMMIT_SHA', '')
    exact = bool(re.fullmatch(r'[0-9a-f]{40}', revision))
    repository = 'https://github.com/Pinnacle-Apps/CocoaCraft-Roast'
    return {'license': 'AGPL-3.0-or-later',
            'repository': repository, 'revision': revision if exact else None,
            'corresponding_source': repository + '/tree/' + revision if exact else repository,
            'notice': 'Artisan notices retained. Deployments must publish their exact corresponding source revision.'}


@app.post('/api/v1/sessions/import', response_model=RoastSession)
def import_profile(payload: ImportRequest, owner: UUID = Depends(require_account)):
    try:
        return import_artisan(payload.profile_text, owner)
    except (ValueError, SyntaxError, RecursionError, TypeError) as exc:
        raise HTTPException(422, 'Invalid or unsupported Artisan profile') from exc


@app.post('/api/v1/sessions/validate', response_model=RoastSession)
def validate_session(session: RoastSession, owner: UUID = Depends(require_account)):
    return owned_session(session, owner)


@app.post('/api/v1/sessions/analyze')
def analyze_session(session: RoastSession, owner: UUID = Depends(require_account)):
    return analyze(owned_session(session, owner))


@app.post('/api/v1/sessions/chart.svg')
def chart(payload: ChartRequest | RoastSession, owner: UUID = Depends(require_account)):
    # Original single-session chart calls remain supported.
    if isinstance(payload, RoastSession):
        session, points, cutoff = payload, [], None
    else:
        session, points, cutoff = payload.session, payload.target_points, payload.replay_until
    if any(b.minute <= a.minute for a, b in zip(points, points[1:])):
        raise HTTPException(422, 'Target times must increase')
    return Response(render_svg(owned_session(session, owner), points, cutoff), media_type='image/svg+xml',
                    headers={'Content-Security-Policy': "default-src 'none'; style-src 'unsafe-inline'; sandbox"})


@app.post('/api/v1/sessions/export')
def export_session(session: RoastSession, owner: UUID = Depends(require_account)):
    return JSONResponse(owned_session(session, owner).model_dump(mode='json'),
                        headers={'Content-Disposition': 'attachment; filename="roast-session.json"'})


@app.post('/api/v1/sessions/original.alog')
def export_original(session: RoastSession, owner: UUID = Depends(require_account)):
    try:
        text = original_artisan_text(owned_session(session, owner))
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    return Response(text, media_type='text/plain', headers={'Content-Disposition': 'attachment; filename="original.alog"'})


@app.get('/api/v1/reference-profiles')
def references(owner: UUID = Depends(require_account)):
    return {'profiles': catalog.entries(), 'policy': 'Reviewed, documented references only; editable copies for every account'}


@app.post('/api/v1/reference-profiles/{reference_id}/copy', response_model=RoastSession)
def copy_reference(reference_id: str, owner: UUID = Depends(require_account)):
    try:
        return catalog.copy_for_user(reference_id, owner)
    except KeyError as exc:
        raise HTTPException(404, 'Curated reference profile not found') from exc


@app.get('/', response_class=HTMLResponse)
def index():
    """Standalone manual workspace: all state remains client-owned."""
    return Path(__file__).with_name('workspace.html').read_text(encoding='utf-8')
