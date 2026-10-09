"""Copy the selected Artisan methods exactly; never import its desktop runtime."""
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'src/artisanlib/canvas.py'
NAMES = ('compute_ror_simple', 'compute_ror')


def extract():
    source = SOURCE.read_text(encoding='utf-8')
    tree = ast.parse(source)
    methods = {n.name: n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name in NAMES}
    chunks = []
    records = []
    for name in NAMES:
        node = methods[name]
        start = min([node.lineno] + [d.lineno for d in node.decorator_list])
        chunk = '\n'.join(source.splitlines()[start-1:node.end_lineno])
        chunks.append(chunk)
        records.append({'method': name, 'source': 'src/artisanlib/canvas.py',
                        'start_line': start, 'end_line': node.end_lineno,
                        'sha256': hashlib.sha256(chunk.encode()).hexdigest()})
    header = '\n'.join(source.splitlines()[:27])
    module = header + '''
# Extracted for CocoaCraft Roast; methods below are verbatim from imported Artisan.
# Only the surrounding class and import boundary were added. AGPL-3.0-or-later.
import logging
import warnings
import numpy

_log = logging.getLogger(__name__)


class ArtisanRoR:
    def __init__(self, polyfit: bool = False):
        self.polyfitRoRcalc = polyfit

''' + '\n\n'.join(chunks) + '\n'
    return module, records


if __name__ == '__main__':
    module, records = extract()
    destination = ROOT / 'roast-web/cocoaroast/vendor'
    destination.mkdir(parents=True, exist_ok=True)
    (destination / 'artisan_ror.py').write_text(module, encoding='utf-8')
    (destination / 'provenance.json').write_text(json.dumps(records, indent=2) + '\n', encoding='utf-8')
