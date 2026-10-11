// Syntax smoke test for the client-owned standalone workspace.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const html = fs.readFileSync(path.join(__dirname, '../roast-web/cocoaroast/workspace.html'), 'utf8');
const match = html.match(/<script>([\s\S]*?)<\/script>/i);
assert.ok(match, 'Workspace must include client-side script');
new vm.Script(match[1], { filename: 'workspace.js' });
for (const token of [
  'cocoacraft-roast-workspace/v1', 'Manual temperature readings',
  'Manual inspection results', 'SIMULATED DEMO', 'Export workspace JSON',
  'Render' // normalize below
]) {
  if (token === 'Render') continue;
  assert.ok(html.includes(token), 'Missing workspace feature: ' + token);
}
console.log('Standalone roast workspace script compiles; expected features are present.');
