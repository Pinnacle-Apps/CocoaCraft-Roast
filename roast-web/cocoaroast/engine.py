"""Request-local analysis using Artisan's original RoR implementations."""
from .models import RoastSession
from .vendor.artisan_ror import ArtisanRoR


def analyze(session: RoastSession) -> dict:
    engine = ArtisanRoR(polyfit=session.settings.ror_method == 'artisan_polyfit')
    times, bt, et, ror_bt, ror_et = [], [], [], [], []
    for sample in session.samples:
        times.append(sample.elapsed_seconds)
        bt.append(-1 if sample.bean_temperature is None else sample.bean_temperature)
        et.append(-1 if sample.environment_temperature is None else sample.environment_temperature)
        ror_bt.append(engine.compute_ror(bt[-1], times, bt, ror_bt, session.settings.delta_samples))
        ror_et.append(engine.compute_ror(et[-1], times, et, ror_et, session.settings.delta_samples))
    return {'elapsed_seconds': times, 'bean_ror': ror_bt, 'environment_ror': ror_et,
            'ror_unit': f'{session.temperature_unit}/min', 'method': session.settings.ror_method,
            'scope': 'Artisan RoR only; desktop smoothing, AUC, alarms and PID are not yet ported',
            'missing_reading_policy': 'Artisan -1 sentinel; repeat prior RoR on final dropout'}
