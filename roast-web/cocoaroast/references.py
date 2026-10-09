"""Only reviewed, documented references may enter the catalog."""
from uuid import UUID, uuid4
from datetime import datetime, timezone
from pydantic import Field

from .models import Model, RoastSession


class CuratedReference(Model):
    id: str = Field(min_length=1, max_length=160)
    source_citation: str = Field(min_length=1, max_length=1000)
    reviewed_by: str = Field(min_length=1, max_length=200)
    reviewed_at: datetime
    applicability: str = Field(min_length=1, max_length=2000)
    session: RoastSession


class ReferenceCatalog:
    def __init__(self, references: list[CuratedReference]):
        if len({r.id for r in references}) != len(references):
            raise ValueError('Duplicate reference id')
        self._references = {r.id: r.model_copy(deep=True) for r in references}

    def entries(self) -> list[dict]:
        return [r.model_dump(mode='json', exclude={'session'}) for r in self._references.values()]

    def copy_for_user(self, reference_id: str, owner: UUID) -> RoastSession:
        reference = self._references[reference_id]
        return reference.session.model_copy(update={
            'id': uuid4(), 'owner_user_id': owner, 'production_link': None,
            'created_at': datetime.now(timezone.utc), 'source_kind': 'reference_copy',
            'reference_profile_id': reference.id}, deep=True)


# No bean-origin recipes are invented or represented as validated cacao references.
catalog = ReferenceCatalog([])
