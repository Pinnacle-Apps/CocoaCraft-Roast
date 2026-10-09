"""Matplotlib headless rendering, isolated and serialized for thread safety."""
from io import BytesIO
from threading import Lock
import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
from .engine import analyze
from .models import RoastSession

_render_lock = Lock()


def render_svg(session: RoastSession, target_points=None, replay_until=None) -> bytes:
    analysis = analyze(session)
    with _render_lock, matplotlib.rc_context({'font.family': 'DejaVu Sans', 'svg.fonttype': 'none'}):
        fig = Figure(figsize=(13.5, 7.2), dpi=120, facecolor='#fffaf3')
        ax = fig.subplots()
        ax.set_facecolor('#fffaf3')
        delta = ax.twinx()
        minutes = [s.elapsed_seconds / 60 for s in session.samples]
        bt = [float('nan') if s.bean_temperature is None else s.bean_temperature for s in session.samples]
        et = [float('nan') if s.environment_temperature is None else s.environment_temperature for s in session.samples]
        if target_points:
            ax.plot([p.minute for p in target_points], [p.bean for p in target_points], color='#3d7dbc', linewidth=2.3, linestyle='--', label='Target BT')
        visible = len(minutes) if replay_until is None else sum(t * 60 <= replay_until for t in minutes)
        ax.plot(minutes[:visible], bt[:visible], color='#713b24', linewidth=2.2, label='Bean (BT)')
        ax.plot(minutes[:visible], et[:visible], color='#b98043', linewidth=1.8, label='Environment (ET)')
        delta.plot(minutes[:visible], analysis['bean_ror'][:visible], color='#397b73', linewidth=1.6, label='Bean RoR')
        for event in session.events:
            if replay_until is not None and event.elapsed_seconds > replay_until:
                continue
            ax.axvline(event.elapsed_seconds / 60, color='#8d8177', linestyle=':', alpha=.6)
            ax.annotate(event.label, xy=(event.elapsed_seconds / 60, 1), xycoords=('data', 'axes fraction'),
                        rotation=90, xytext=(3, -5), textcoords='offset points', va='top', fontsize=8, parse_math=False)
        ax.set(xlabel='Elapsed time (minutes)', ylabel=f'Temperature (°{session.temperature_unit})')
        delta.set_ylabel(f'Rate of rise (°{session.temperature_unit}/min)', color='#397b73')
        ax.set_xlim(0, max(1, minutes[-1] if minutes else 0, target_points[-1].minute if target_points else 0))
        temps = [x for x in bt + et if x == x]
        if target_points:
            temps.extend(p.bean for p in target_points)
        if temps:
            ax.set_ylim(min(temps) - 8, max(temps) + 8)
        rors = [x for x in analysis['bean_ror'] if isinstance(x, (int, float)) and x == x]
        if rors:
            delta.set_ylim(min(0, min(rors) - 2), max(2, max(rors) + 2))
        ax.grid(True, alpha=.2)
        handles = [line for line in ax.get_lines() if line.get_label() in ('Target BT', 'Bean (BT)', 'Environment (ET)')] + [line for line in delta.get_lines() if line.get_label() == 'Bean RoR']
        ax.legend(handles, [h.get_label() for h in handles], loc='lower right')
        fig.suptitle('CocoaCraft Roast | ' + session.name, color='#4b281c', fontsize=16, parse_math=False)
        fig.text(.01, .01, 'Artisan RoR · imported/manual data · no validated cacao process guidance', fontsize=8)
        fig.tight_layout(rect=(0, .025, 1, .95))
        buffer = BytesIO()
        try:
            fig.savefig(buffer, format='svg')
            return buffer.getvalue()
        finally:
            fig.clear()
