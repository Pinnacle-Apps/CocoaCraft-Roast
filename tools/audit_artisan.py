"""Generate a static, reproducible source inventory without importing Qt or drivers."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def inventory():
    modules = []
    for path in sorted((ROOT / 'src').glob('*/*.py')):
        source = path.read_text(encoding='utf-8-sig')
        tree = ast.parse(source)
        imports = sorted({n.module or '' for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)} |
                         {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names})
        functions = []
        def visit(nodes, prefix=''):
            for node in nodes:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    functions.append({'name': prefix + node.name, 'line': node.lineno,
                                      'end_line': node.end_lineno,
                                      'calls': sorted({ast.unparse(n.func) for n in ast.walk(node)
                                                       if isinstance(n, ast.Call)})})
                elif isinstance(node, ast.ClassDef):
                    visit(node.body, prefix + node.name + '.')
        visit(tree.body)
        modules.append({'path': path.relative_to(ROOT).as_posix(),
                        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                        'lines': len(source.splitlines()), 'imports': imports,
                        'qt_imports': [i for i in imports if i.startswith('PyQt')],
                        'functions': functions})
    return modules


if __name__ == '__main__':
    modules = inventory()
    out = ROOT / 'docs/checkpoint-a'
    out.mkdir(parents=True, exist_ok=True)
    base = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    (out / 'function-dependency-map.json').write_text(json.dumps(
        {'source_commit': base, 'method': 'AST static inventory; calls are syntactic, not resolved runtime edges',
         'modules': modules}, indent=2) + '\n', encoding='utf-8')
    rows = ['# Artisan module and dependency map', '',
            'Full method-level calls and source hashes: `function-dependency-map.json`.', '',
            '| Module | Lines | Functions | Direct Qt imports | Internal imports |',
            '|---|---:|---:|---|---|']
    for m in modules:
        internal = [i for i in m['imports'] if i.startswith(('artisanlib', 'plus'))]
        rows.append(f"| `{m['path']}` | {m['lines']} | {len(m['functions'])} | {', '.join(m['qt_imports']) or 'None'} | {', '.join(internal)} |")
    (out / 'module-map.md').write_text('\n'.join(rows) + '\n', encoding='utf-8')
    print(f"Inventoried {len(modules)} modules, {sum(len(m['functions']) for m in modules)} functions")
