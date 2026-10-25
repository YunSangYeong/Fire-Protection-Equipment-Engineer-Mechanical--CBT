import { test,expect,type Page } from '@playwright/test';
async function open(page:Page){await page.getByRole('button',{name:'메뉴 열기',exact:true}).click();await expect(page.locator('.sidebar')).toHaveClass(/open/);await page.waitForTimeout(350);}
async function visibleInside(page:Page, label:string){const el=page.locator('.sidebar').getByRole('button',{name:label,exact:true});const b=await el.boundingBox();expect(b).not.toBeNull();expect(b!.y).toBeGreaterThanOrEqual(0);expect(b!.y+b!.height).toBeLessThanOrEqual(page.viewportSize()!.height);return el;}
for(const size of [{width:390,height:480},{width:740,height:360}]){
 test(`실제 휠 상하 이동 및 하단 백업·초기화·상단 접근 ${size.width}x${size.height}`,async({page})=>{
  await page.setViewportSize(size);await page.goto('');await open(page);
  const sidebar=page.locator('.sidebar');await expect(sidebar).toHaveCSS('overflow-y','auto');
  const b=await sidebar.boundingBox();await page.mouse.move(b!.x+100,Math.min(220,size.height-50));await page.mouse.wheel(0,1500);
  await expect.poll(()=>sidebar.evaluate(el=>el.scrollTop)).toBeGreaterThan(0);
  const backup=await visibleInside(page,'학습 기록 백업');const download=page.waitForEvent('download');await backup.click();expect((await download).suggestedFilename()).toBe('fire-mechanical-study-backup.json');
  const reset=await visibleInside(page,'데이터 초기화');await reset.click();await expect(page.getByRole('dialog')).toBeVisible();await page.getByRole('button',{name:'돌아가기',exact:true}).click();
  await page.mouse.move(b!.x+100,Math.min(220,size.height-50));await page.mouse.wheel(0,-1500);await expect.poll(()=>sidebar.evaluate(el=>el.scrollTop)).toBe(0);
  await (await visibleInside(page,'학습 대시보드')).click();await expect(sidebar).not.toHaveClass(/open/);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 });
 test(`CDP 실제 터치 스와이프 상하 이동 ${size.width}x${size.height}`,async({page})=>{
  await page.setViewportSize(size);await page.goto('');await open(page);
  const cdp=await page.context().newCDPSession(page);await cdp.send('Emulation.setTouchEmulationEnabled',{enabled:true});
  async function swipe(from:number,to:number){
   await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:130,y:from}]});
   for(let i=1;i<=12;i++){await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:130,y:from+(to-from)*i/12}]});await page.waitForTimeout(20);}
   await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await page.waitForTimeout(250);
  }
  const sidebar=page.locator('.sidebar');for(let i=0;i<4;i++)await swipe(size.height-70,90);
  await expect.poll(()=>sidebar.evaluate(el=>el.scrollTop)).toBeGreaterThan(0);
  await visibleInside(page,'학습 기록 백업');await visibleInside(page,'데이터 초기화');
  for(let i=0;i<4;i++)await swipe(90,size.height-70);
  await expect.poll(()=>sidebar.evaluate(el=>el.scrollTop)).toBe(0);
  await (await visibleInside(page,'학습 대시보드')).click();await expect(sidebar).not.toHaveClass(/open/);
 });
}
test('글자 확대 메뉴와 각 화면 상단 배너 없음',async({page})=>{
 await page.setViewportSize({width:390,height:480});await page.goto('');await page.addStyleTag({content:'.sidebar {font-size:150%} .sidebar nav button {font-size:1em}'});
 for(const label of ['학습 대시보드','실전 모의시험','랜덤 문제풀이','오답노트','북마크','학습 통계','문제은행 관리']){
  await open(page);await page.mouse.move(120,220);await page.mouse.wheel(0,-1500);await page.locator('nav').getByRole('button',{name:label,exact:true}).click();await expect(page.locator('.criteria-note')).toHaveCount(0);
 }
});
