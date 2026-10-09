"""Parse Artisan data safely, retaining the complete original file for round trips."""
import ast
import json
from uuid import UUID

from .models import Event, MAX_SAMPLES, RoastSession, Sample

MARKERS = ('CHARGE', 'DRY END', 'FC START', 'FC END', 'SC START', 'SC END', 'DROP', 'COOLING END')


def import_artisan(text: str, owner: UUID) -> RoastSession:
    if len(text.encode('utf-8')) > 1000000:
        raise ValueError('Profile exceeds the 1 MB import limit')
    try:
        profile = json.loads(text)
    except json.JSONDecodeError:
        tree = ast.parse(text, mode='eval')
        if sum(1 for _ in ast.walk(tree)) > 100000:
            raise ValueError('Profile is too complex')
        profile = ast.literal_eval(tree)
    if not isinstance(profile, dict):
        raise ValueError('Artisan profile must be an object')
    times, et, bt = (profile.get(key) for key in ('timex', 'temp1', 'temp2'))
    if not all(isinstance(v, list) for v in (times, et, bt)):
        raise ValueError('Artisan timex, temp1 and temp2 arrays are required')
    if not (2 <= len(times) <= MAX_SAMPLES and len(times) == len(et) == len(bt)):
        raise ValueError('Profile arrays must have equal lengths and 2–10000 samples')
    if any(isinstance(v, bool) or not isinstance(v, (float, int)) for seq in (times, et, bt) for v in seq):
        raise ValueError('Profile samples must be numbers')
    # Preserve -1 probe-dropout semantics as explicit missing readings.
    samples = [Sample(elapsed_seconds=t, environment_temperature=None if e == -1 else e,
                      bean_temperature=None if b == -1 else b) for t, e, b in zip(times, et, bt)]
    events = []
    indexes = profile.get('timeindex', [])
    if not isinstance(indexes, list) or len(indexes) > 8:
        raise ValueError('timeindex must contain at most eight marker positions')
    for position, index in enumerate(indexes):
        if isinstance(index, bool) or not isinstance(index, int):
            raise ValueError('Marker indexes must be integers')
        # Artisan: CHARGE absent=-1; subsequent markers absent=0.
        if (index == -1 and position == 0) or (index == 0 and position > 0):
            continue
        if index < 0 or index >= len(samples):
            raise ValueError('Marker index is outside the profile')
        kind = {0: 'charge', 6: 'drop', 7: 'cooling_end'}.get(position, 'artisan_marker')
        events.append(Event(elapsed_seconds=times[index], kind=kind,
                            label=MARKERS[position], original_marker=MARKERS[position]))
    return RoastSession(owner_user_id=owner, name=profile.get('title') or 'Imported Artisan profile',
                        temperature_unit=profile.get('mode', 'C'), samples=samples, events=events,
                        source_kind='artisan_import', source_profile_text=text)


def original_artisan_text(session: RoastSession) -> str:
    if session.source_profile_text is None:
        raise ValueError('This session has no original Artisan source file')
    return session.source_profile_text
