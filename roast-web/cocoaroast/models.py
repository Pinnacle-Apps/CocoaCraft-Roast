"""Versioned transport models; no database or hardware dependencies."""
from datetime import datetime, timezone
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator

MAX_SAMPLES = 10000


class Model(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False)


class Sample(Model):
    elapsed_seconds: float
    bean_temperature: float | None = None
    environment_temperature: float | None = None
    power_percent: float | None = Field(default=None, ge=0, le=100)
    airflow_percent: float | None = Field(default=None, ge=0, le=100)
    drum_speed_rpm: float | None = Field(default=None, ge=0)


class Event(Model):
    elapsed_seconds: float
    kind: Literal['charge', 'drop', 'cooling_end', 'observation', 'control_change', 'artisan_marker']
    label: str = Field(min_length=1, max_length=120)
    notes: str = Field(default='', max_length=2000)
    original_marker: str | None = None


class CacaoMetadata(Model):
    origin: str = Field(default='', max_length=200)
    lot: str = Field(default='', max_length=200)
    bean_form: Literal['whole', 'nib', 'unknown'] = 'unknown'
    fermentation: str = Field(default='', max_length=200)
    moisture_percent: float | None = Field(default=None, ge=0, le=100)
    beans_per_100g: float | None = Field(default=None, gt=0)
    batch_mass_kg: float | None = Field(default=None, gt=0)
    output_mass_kg: float | None = Field(default=None, ge=0)
    roaster: str = Field(default='', max_length=200)
    probe_location: str = Field(default='', max_length=300)
    sensory_notes: str = Field(default='', max_length=4000)


class ProductionLink(Model):
    production_run_id: UUID
    step_id: UUID | None = None
    machine_run_id: UUID | None = None
    adapter: Literal['mock'] = 'mock'


class EngineSettings(Model):
    delta_samples: int = Field(default=5, ge=1, le=120)
    ror_method: Literal['artisan_simple', 'artisan_polyfit'] = 'artisan_simple'


class RoastSession(Model):
    schema_version: Literal['1.0'] = '1.0'
    id: UUID = Field(default_factory=uuid4)
    owner_user_id: UUID
    name: str = Field(default='Untitled cacao roast', min_length=1, max_length=160)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    temperature_unit: Literal['C', 'F'] = 'C'
    production_link: ProductionLink | None = None
    metadata: CacaoMetadata = Field(default_factory=CacaoMetadata)
    samples: list[Sample] = Field(default_factory=list, max_length=MAX_SAMPLES)
    events: list[Event] = Field(default_factory=list, max_length=500)
    settings: EngineSettings = Field(default_factory=EngineSettings)
    source_kind: Literal['manual', 'artisan_import', 'mock_replay', 'reference_copy'] = 'manual'
    source_profile_text: str | None = Field(default=None, max_length=1000000)
    reference_profile_id: str | None = Field(default=None, max_length=160)
    notes: str = Field(default='', max_length=8000)

    @model_validator(mode='after')
    def ordered_samples(self):
        times = [s.elapsed_seconds for s in self.samples]
        if any(b <= a for a, b in zip(times, times[1:])):
            raise ValueError('Sample times must be strictly increasing; no implicit sorting or resampling')
        if self.events and (not times or any(e.elapsed_seconds < times[0] or e.elapsed_seconds > times[-1] for e in self.events)):
            raise ValueError('Events must be within the recorded sample range')
        return self
