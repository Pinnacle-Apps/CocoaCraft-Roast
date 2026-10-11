const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.ROAST_BROWSER_CHANNEL?{channel:process.env.ROAST_BROWSER_CHANNEL}:{})});
 try{
  const page=await browser.newPage({acceptDownloads:true});
  page.on('pageerror',e=>{throw e});
  await page.goto('file://'+path.resolve(__dirname,'../roast-web/cocoaroast/workspace.html'));
  await page.locator('#name').fill('QA roasted profile');
  await page.locator('#add-target').click();
  await page.locator('#add-target').click();
  await page.locator('[data-target="1"][data-field="bean"]').fill('110');
  await page.locator('[data-target="1"][data-field="bean"]').dispatchEvent('change');
  await page.locator('#unit').selectOption('F');
  assert.equal(await page.locator('#unit').inputValue(),'F');
  assert.equal(await page.locator('[data-target="1"][data-field="bean"]').inputValue(),'230');
  await page.locator('#reading-minute').fill('2');
  await page.locator('#reading-bean').fill('120');
  await page.locator('#add-reading').click();
  await page.locator('#inspection-name').fill('Color');
  await page.locator('#inspection-result').selectOption('pass');
  await page.locator('#inspection-actual').fill('Visually acceptable');
  await page.locator('#add-inspection').click();
  assert.equal(await page.locator('#inspections tr').count(),1);
  await page.locator('#event-minute').fill('2');
  await page.locator('#event-label').fill('Visual observation');
  await page.locator('#add-event').click();
  const pending=page.waitForEvent('download');
  await page.locator('#export').click();
  const download=await pending;
  const exported=JSON.parse(fs.readFileSync(await download.path(),'utf8'));
  assert.equal(exported.unit,'F');
  assert.equal(exported.targets.length,2);
  assert.equal(exported.readings.length,1);
  assert.equal(exported.inspections[0].actual,'Visually acceptable');
  assert.equal(exported.events.length,1);
  page.once('dialog',d=>d.accept());
  await page.locator('#new').click();
  assert.equal(await page.locator('#inspections tr').count(),0);
  await page.locator('#import').setInputFiles({name:'roast.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(exported))});
  await page.waitForFunction(() => document.getElementById('name').value === 'QA roasted profile' || document.getElementById('status').textContent.startsWith('Import failed'));
  assert.equal(await page.locator('#name').inputValue(),'QA roasted profile');
  assert.equal(await page.locator('#inspections tr').count(),1);
  assert.equal(await page.locator('#readings tr').count(),1);
  assert.equal(await page.locator('#targets tr').count(),2);
  await page.locator('#import').setInputFiles({name:'malformed.json',mimeType:'application/json',buffer:Buffer.from('{"format":"wrong"}')});
  assert.equal(await page.locator('#name').inputValue(),'QA roasted profile');
  assert.match(await page.locator('#status').innerText(),/Import failed/);
  // Cross-origin parent bridge, with network mocked. No customer account or live API.
  const embedded=await browser.newContext();
  const host=await embedded.newPage();
  const source=fs.readFileSync(path.join(__dirname,'../roast-web/cocoaroast/workspace.html'),'utf8');
  await embedded.route('https://www.cocoa-craft.com/test-bridge',r=>r.fulfill({
    status:200,contentType:'text/html',
    body:'<!doctype html><style>body{margin:0}iframe{width:100%;height:1000px;border:0}</style><iframe id="roast" referrerpolicy="origin" src="https://roast-preview.example.test/"></iframe><script>window.received=[];window.addEventListener("message",e=>{if(e.origin==="https://roast-preview.example.test"){window.received.push(e.data)}})</script>'
  }));
  await embedded.route('https://roast-preview.example.test/',r=>r.fulfill({status:200,contentType:'text/html',body:source}));
  await host.goto('https://www.cocoa-craft.com/test-bridge');
  const roast=host.frameLocator('#roast');
  await roast.locator('#save-os').waitFor({state:'visible'});
  await roast.locator('#name').fill('Embedded QA draft');
  assert.equal(await roast.locator('#save-os').innerText(),'Save Roast Profile to CocoaCraft');
  for(const width of [320,375,768,900,1280]){
   await host.setViewportSize({width,height:1000});
   const child=host.frames().find(f=>f.url()==='https://roast-preview.example.test/');
   assert.ok(await child.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth), 'embedded overflow at '+width);
   assert.ok(await child.evaluate(()=>[...document.querySelectorAll('.scroll')].every(e=>e.scrollWidth>e.clientWidth||e.clientWidth>=650)));
  }
  await roast.locator('#save-os').click();
  const child=host.frames().find(f=>f.url()==='https://roast-preview.example.test/');
  await child.evaluate(()=>document.getElementById('save-os').onclick());
  assert.equal(await roast.locator('#save-os').isDisabled(),true);
  await host.waitForFunction(()=>window.received?.length===1);
  assert.equal(await host.evaluate(()=>window.received[0].type),'cocoacraft.roast.save-draft.v1');
  assert.equal(await host.evaluate(()=>window.received[0].workspace.name),'Embedded QA draft');
  assert.equal(await host.evaluate(()=>window.received.length),1);
  // Wrong source cannot complete a save, even with the right origin.
  await child.evaluate(()=>window.dispatchEvent(new MessageEvent('message',{origin:'https://www.cocoa-craft.com',source:window,data:{type:'cocoacraft.roast.save-result.v1',ok:true}})));
  assert.equal(await roast.locator('#save-os').isDisabled(),true);
  await host.evaluate(()=>document.getElementById('roast').contentWindow.postMessage({type:'cocoacraft.roast.save-result.v1',ok:true},'https://roast-preview.example.test'));
  await roast.locator('#save-status').getByText('Roast profile saved as a draft', {exact:false}).waitFor();
  assert.equal(await roast.locator('#save-os').isDisabled(),true);
  assert.equal(await roast.locator('#saved-profiles a').getAttribute('href'),'https://www.cocoa-craft.com/workspace/roast-profiles');
  await roast.locator('#name').fill('Changed draft');
  assert.equal(await roast.locator('#save-os').isDisabled(),false);
  await roast.locator('#save-os').click();
  await host.waitForFunction(()=>window.received.length===2);
  await host.evaluate(()=>document.getElementById('roast').contentWindow.postMessage({type:'cocoacraft.roast.save-result.v1',ok:false,error:'Sign in to CocoaCraft, then save again.'},'https://roast-preview.example.test'));
  await roast.locator('#save-status').getByText('Save failed:', {exact:false}).waitFor();
  assert.equal(await roast.locator('#save-os').isDisabled(),false);
  assert.match(await roast.locator('#save-status').innerText(),/Sign in/);
  await roast.locator('#save-os').click();
  await host.waitForFunction(()=>window.received.length===3);
  await host.evaluate(()=>document.getElementById('roast').contentWindow.postMessage({type:'cocoacraft.roast.save-result.v1',ok:false,error:'Save canceled.'},'https://roast-preview.example.test'));
  await roast.locator('#save-status').getByText('Save canceled.', {exact:false}).waitFor();
  assert.equal(await roast.locator('#save-os').isDisabled(),false);
  // An unrelated embedding origin gets no save capability.
  await embedded.route('https://untrusted.example.test/',r=>r.fulfill({contentType:'text/html',body:'<iframe id="roast" referrerpolicy="origin" src="https://roast-preview.example.test/"></iframe>'}));
  await host.goto('https://untrusted.example.test/');
  assert.equal(await host.frameLocator('#roast').locator('#save-os').isHidden(),true);
  await embedded.close();
  console.log('PASS: mocked embedded bridge, duplicate guards, error/cancel states, strict origin/source checks, responsive layout (no live authenticated persistence)');
  console.log('PASS: browser workflow, unit conversion, manual checks, JSON roundtrip, invalid import safety');
 }finally{await browser.close()}
})().catch(err=>{console.error(err);process.exitCode=1});
