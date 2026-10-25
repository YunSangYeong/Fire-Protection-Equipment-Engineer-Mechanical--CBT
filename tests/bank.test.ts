import { describe,it,expect } from 'vitest';
import { BASE_BANK as bank, SUBJECTS, fingerprint, validateQuestion } from '../src/model';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
describe('자체 제작 은행 실수량·추적성·재현',()=>{
 it('1000개 고유 문항, 과목별 260/360/20/360개, 실제 상태와 권리',()=>{
   expect(bank).toHaveLength(1000);
   expect(new Set(bank.map(q=>q.id)).size).toBe(1000);
   expect(new Set(bank.map(fingerprint)).size).toBe(1000);
   SUBJECTS.forEach((s,i)=>expect(bank.filter(q=>q.subject===s)).toHaveLength([260,360,20,360][i]));
   for(const q of bank){expect(()=>validateQuestion(q)).not.toThrow();expect(q.type).toBe('original');expect(q.year).toBeNull();expect(q.session).toBeNull();expect(q.verificationStatus).toBe('reviewed');expect(q.reviewNote).toContain('외부');expect(q.rights).toContain('CC BY 4.0');expect(q.explanation.length).toBeGreaterThan(30);}
 });
 it('46개 수치 변형 family 각 20개, 개념 80개를 분리 집계한다',()=>{
   expect(bank.filter(q=>!q.family)).toHaveLength(80);
   const families=new Set(bank.flatMap(q=>q.family?[q.family]:[]));expect(families.size).toBe(46);
   for(const f of families){const qs=bank.filter(q=>q.family===f);expect(qs).toHaveLength(20);expect(new Set(qs.map(q=>JSON.stringify(q.calculation!.values))).size).toBe(20);}
 });
 it('기존 200문항의 ID·본문·보기·답안·메타데이터를 그대로 보존한다',()=>{
   const digest=createHash('sha256').update(JSON.stringify(bank.slice(0,200))).digest('hex');
   expect(digest).toBe('4aab8a9d4172069480740b4f6ed2902afa27771a87f8cc1263a1b336f781e17f');
 });
 it('동일 원고 재생성은 바이트 단위로 동일하다',()=>{
   const path='src/data/questions-main.json';const hash=()=>createHash('sha256').update(readFileSync(path)).digest('hex');const before=hash();execFileSync('python3',['scripts/generate_bank.py']);expect(hash()).toBe(before);
 });
});
for(const q of bank.filter(q=>q.calculation)) it(`독립 SI 계산·보기 동치 확인 ${q.id}`,()=>{
 const c=q.calculation!,v=c.values;
 const formulas:Record<string,()=>number>={
  hydrostatic:()=>1000*9.8*v[0]/1000,
  continuity:()=>v[0]/10000*v[1]*1000,
  power:()=>1000*9.8*(v[0]/1000)*v[1]/1000,
  'water-volume':()=>v[0]*v[1]/1000,
  mixture:()=>v[0]*v[1]/100,
  'nozzle-speed':()=>Math.sqrt(2*v[1]*v[0]),
  'sensible-heat':()=>v[0]*v[1]*v[2],
  'latent-heat':()=>v[0]*v[1],
  'heat-flux':()=>v[0]/v[1],
  'radiation-ratio':()=>v[0]*Math.pow(v[1],4),
  'wall-conduction':()=>v[0]*v[1]*v[2]/v[3],
  'linear-expansion':()=>v[0]*v[1]*v[2]*1000,
  'constant-volume-pressure':()=>v[0]*v[2]/v[1],
  'constant-pressure-volume':()=>v[0]*v[2]/v[1],
  'oxygen-volume':()=>v[0]*(v[1]/100),
  'heat-release':()=>v[0]*v[1],
  'fire-load':()=>v[0]*v[1]/v[2],
  'water-temperature-mix':()=> (v[0]*v[2]+v[1]*v[3])/(v[0]+v[1]),
  'mass-flow':()=>v[0]*v[1],
  'momentum-force':()=>v[0]*v[1]*(v[3]-v[2]),
  'dynamic-pressure':()=>0.5*v[0]*v[1]**2/1000,
  'reynolds-number':()=>v[0]*v[1]*v[2]/v[3],
  'darcy-loss':()=>v[0]*(v[1]/v[2])*v[3]**2/(2*v[4]),
  'minor-loss':()=>v[0]*v[1]**2/(2*v[2]),
  'laminar-friction':()=>64000/v[0],
  'poiseuille-flow':()=>v[4]*v[0]*v[1]**4/(128*v[2]*v[3])*1e6,
  'buoyancy':()=>v[0]*v[1]*v[2],
  'differential-manometer':()=>(v[0]-v[1])*v[2]*v[3]/1000,
  'pipe-area':()=>v[1]*(v[0]/10)**2/4,
  'pipe-velocity':()=>4*(v[0]/1000)/(v[2]*(v[1]/1000)**2),
  'hydraulic-radius':()=>v[0]/4,
  'bulk-compression':()=>v[0]*v[1]/v[2],
  'shaft-power':()=>v[0]/v[1],
  'pump-efficiency':()=>v[0]/v[1]*100,
  'affinity-flow':()=>v[0]*(v[2]/v[1]),
  'affinity-head':()=>v[0]*(v[2]/v[1])**2,
  'affinity-power':()=>v[0]*(v[2]/v[1])**3,
  'nozzle-k':()=>v[0]*Math.sqrt(v[1]),
  'parallel-outlet-flow':()=>v[0]*v[1],
  'spray-density':()=>v[0]/v[1],
  'foam-water-volume':()=>v[0]*(100-v[1])/100,
  'rectangular-tank':()=>v[0]*v[1]*v[2]*1000,
  'cylindrical-tank':()=>v[2]*v[0]**2*v[1]*1000,
  'pressure-force':()=>v[0]*1000*v[1],
  'liquid-thermal-expansion':()=>v[0]*v[1]*v[2],
  'isothermal-gas-volume':()=>v[0]*v[1]/v[2],
 };
 expect(formulas[c.kind], c.kind).toBeDefined();
 const raw = formulas[c.kind]();
 const precision = c.precision ?? 2;
 const scale = 10**precision;
 const rounded = Math.round((raw + Number.EPSILON*Math.max(1,Math.abs(raw))*4)*scale)/scale;
 expect(rounded).toBeCloseTo(c.result,9);
 const parsed=q.choices.map(x=>Number(x.split(' ')[0]));
 expect(parsed.filter(x=>Math.abs(x-c.result)<1e-8)).toHaveLength(1);
 expect(parsed[q.answer-1]).toBeCloseTo(c.result,9);
 expect(q.choices[q.answer-1]).toContain(c.unit);
 expect(q.explanation).toContain(c.unit);
});
