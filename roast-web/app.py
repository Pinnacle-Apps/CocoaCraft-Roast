"""CocoaCraft Roast: isolated Vercel proof of concept.

This endpoint deliberately does not import Artisan's Qt desktop runtime.
Roasting curves below are simulated; real Artisan profile loading comes next.
"""
from io import BytesIO

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response

app = FastAPI(title="CocoaCraft Roast — Plotting Prototype", version="0.1.0")


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "cocoacraft-roast", "mode": "simulation"}


def render_chart() -> bytes:
    """Render a demonstrative two-axis roasting chart using NumPy and Matplotlib."""
    elapsed = np.linspace(0, 18, 181)
    bean = 28 + 105 * (1 - np.exp(-elapsed / 8.5)) + 0.17 * elapsed
    environment = 155 - 23 * np.exp(-elapsed / 2.7) + 2 * np.sin(elapsed / 3)
    target = 28 + 108 * (1 - np.exp(-elapsed / 9))
    ror = np.gradient(bean, elapsed)  # Celsius per minute

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    fig, ax = plt.subplots(figsize=(13.5, 7.2), dpi=120)
    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#161f30")
    ax2 = ax.twinx()
    ax.plot(elapsed, environment, color="#e8a260", linewidth=2, label="Environment (ET)")
    ax.plot(elapsed, bean, color="#58d4b6", linewidth=2.6, label="Bean (BT)")
    ax.plot(elapsed, target, color="#80a9fa", linestyle="--", linewidth=1.4, alpha=0.9, label="Target BT")
    ax2.plot(elapsed, ror, color="#f4d16d", linewidth=2, label="Bean RoR")
    for x, name in [(0, "CHARGE"), (7, "MID-ROAST"), (18, "DROP")]:
        ax.axvline(x, color="#aab7cb", linestyle=":", alpha=0.5)
        ax.text(x + 0.14, 151, name, fontsize=8, color="#cbd5e1", rotation=90, va="top")
    ax.set(xlabel="Roast time (minutes)", ylabel="Temperature (°C)", xlim=(0, 18), ylim=(20, 165))
    ax2.set(ylabel="Rate of rise (°C/min)", ylim=(0, 17))
    ax.tick_params(colors="#d6e1ef")
    ax2.tick_params(colors="#f4d16d")
    ax.xaxis.label.set_color("#d6e1ef")
    ax.yaxis.label.set_color("#d6e1ef")
    ax2.yaxis.label.set_color("#f4d16d")
    for axis in (ax, ax2):
        for spine in axis.spines.values():
            spine.set_color("#627086")
    ax.grid(True, alpha=0.16, color="#bbc8d8")
    fig.suptitle("CocoaCraft Roast  |  Simulation preview", color="#f1f5f9", fontsize=17, fontweight="bold")
    lines = ax.get_lines()[:3] + ax2.get_lines()[:1]
    legend = ax.legend(lines, [line.get_label() for line in lines], loc="lower right",
                       facecolor="#253249", edgecolor="#627086", framealpha=0.95)
    for text in legend.get_texts():
        text.set_color("#f1f5f9")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    buf = BytesIO()
    fig.savefig(buf, format="svg", facecolor=fig.get_facecolor())
    plt.close(fig)
    return buf.getvalue()


@app.get("/api/chart.svg")
def chart():
    return Response(content=render_chart(), media_type="image/svg+xml",
                    headers={"Cache-Control": "no-store"})


@app.get("/", response_class=HTMLResponse)
def index():
    return """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CocoaCraft Roast | Plotting Test</title>
<style>body{margin:0;background:#0b1220;color:#e5e7eb;font:16px system-ui,sans-serif}
main{max-width:1300px;margin:36px auto;padding:0 20px}
h1{margin-bottom:6px}.sub{color:#a8b8d0}
img{width:100%;border:1px solid #334155;border-radius:12px}
a{color:#8ebaff}</style></head><body><main>
<h1>CocoaCraft Roast</h1><p class="sub">Python + NumPy + Matplotlib deployment test. Sample readings are simulated, not actual Artisan data.</p>
<img src="/api/chart.svg" alt="Simulated roast curves of bean temperature, environment temperature and rate of rise">
<p><a href="/api/health">Service health</a> · <a href="/api/chart.svg">Full-size SVG</a></p>
</main></body></html>"""
