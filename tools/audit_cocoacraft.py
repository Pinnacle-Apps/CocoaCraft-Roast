"""Read the pinned CocoaCraft Git source and structure snapshots; no database access."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('repository', type=Path)
args = parser.parse_args()
ref = 'origin/main'
git = ['git', '-c', 'safe.directory=' + args.repository.resolve().as_posix()]
def read(path):
    return subprocess.check_output(git + ['show', f'{ref}:{path}'], cwd=args.repository)

snapshot = read('docs/supabase-schema-snapshot.json')
sql = read('docs/supabase-schema-snapshot.sql')
data = json.loads(snapshot)
names = ['roast_profiles', 'production_runs', 'production_run_steps', 'machine_runs', 'machine_telemetry', 'org_members']
tables = [t for t in data['tables'] if t['table_name'] in names]
result = {'commit': subprocess.check_output(git + ['rev-parse', ref], cwd=args.repository, text=True).strip(),
          'generated_at': data.get('generated_at'), 'snapshots': {
          'docs/supabase-schema-snapshot.json': hashlib.sha256(snapshot).hexdigest(),
          'docs/supabase-schema-snapshot.sql': hashlib.sha256(sql).hexdigest()},
          'tables': [{'name': t['table_name'], 'schema': t['table_schema'],
                     'columns': [c['column_name'] for c in t['columns']],
                     'policies': t.get('policies', []), 'constraints': t.get('constraints', [])} for t in tables]}
for t in tables:
    if f'"public"."{t["table_name"]}"' not in sql.decode():
        raise ValueError(f'Missing table in SQL snapshot: {t["table_name"]}')
out = Path(__file__).resolve().parents[1] / 'docs/checkpoint-a/cocoacraft-context.json'
out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(result['commit'], result['generated_at'], [t['table_name'] for t in tables])
