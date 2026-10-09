"""Mock-first boundaries; never imports Artisan device drivers or writes live records."""
from copy import deepcopy
from typing import Protocol
from uuid import UUID

from .models import ProductionLink, RoastSession, Sample


class SessionRepository(Protocol):
    def save(self, session: RoastSession) -> None: ...
    def get(self, session_id: UUID, owner: UUID) -> RoastSession: ...


class MemorySessionRepository:
    """Local test adapter only. Do not instantiate this in a Vercel request handler."""
    def __init__(self):
        self._sessions = {}

    def save(self, session: RoastSession) -> None:
        previous = self._sessions.get(session.id)
        if previous is not None and previous.owner_user_id != session.owner_user_id:
            raise PermissionError('Session belongs to another account')
        self._sessions[session.id] = session.model_copy(deep=True)

    def get(self, session_id: UUID, owner: UUID) -> RoastSession:
        session = self._sessions[session_id]
        if session.owner_user_id != owner:
            raise PermissionError('Session belongs to another account')
        return session.model_copy(deep=True)


class MockProductionAdapter:
    def __init__(self, runs: dict[UUID, UUID]):
        self._owners = deepcopy(runs)

    def link(self, session: RoastSession, link: ProductionLink) -> RoastSession:
        if self._owners.get(link.production_run_id) != session.owner_user_id:
            raise PermissionError('Mock production run unavailable to this account')
        return session.model_copy(update={'production_link': link}, deep=True)


class MockReplayAdapter:
    """Deterministic replay of recorded samples; no clock, process or hardware required."""
    def read(self, session: RoastSession, through_seconds: float) -> list[Sample]:
        return [s.model_copy(deep=True) for s in session.samples if s.elapsed_seconds <= through_seconds]
