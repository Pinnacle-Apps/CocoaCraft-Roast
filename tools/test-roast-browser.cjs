const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({headless:true});
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
    body:'<!doctype html><iframe id="roast" referrerpolicy="origin" src="https://roast-preview.example.test/"></iframe><script>window.received=[];window.addEventListener("message",e=>{if(e.origin==="https://roast-preview.example.test"){window.received.push(e.data);document.getElementById("roast").contentWindow.postMessage({type:"cocoacraft.roast.save-result.v1",ok:true},"https://roast-preview.example.test")}})</script>'
  }));
  await embedded.route('https://roast-preview.example.test/',r=>r.fulfill({status:200,contentType:'text/html',body:source}));
  await host.goto('https://www.cocoa-craft.com/test-bridge');
  const roast=host.frameLocator('#roast');
  await roast.locator('#save-os').waitFor({state:'visible'});
  await roast.locator('#name').fill('Embedded QA draft');
  await roast.locator('#save-os').click();
  await host.waitForFunction(()=>window.received?.length===1);
  assert.equal(await host.evaluate(()=>window.received[0].type),'cocoacraft.roast.save-draft.v1');
  assert.equal(await host.evaluate(()=>window.received[0].workspace.name),'Embedded QA draft');
  await roast.locator('#status').getByText('Draft saved in CocoaCraft OS.').waitFor();
  await embedded.close();
  console.log('PASS: authorized embedded save bridge and response');
  console.log('PASS: browser workflow, unit conversion, manual checks, JSON roundtrip, invalid import safety');
 }finally{await browser.close()}
})().catch(err=>{console.error(err);process.exitCode=1});
