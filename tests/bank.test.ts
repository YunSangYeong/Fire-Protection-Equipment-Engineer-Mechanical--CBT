import { describe,it,expect } from 'vitest';
import { BASE_BANK as bank, SUBJECTS, fingerprint, validateQuestion } from '../src/model';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
describe('자체 제작 은행 실수량·추적성·재현',()=>{
 it('200개 고유 문항, 과목별 20/80/20/80개, 실제 상태와 권리',()=>{
   expect(bank).toHaveLength(200);
   expect(new Set(bank.map(q=>q.id)).size).toBe(200);
   expect(new Set(bank.map(fingerprint)).size).toBe(200);
   SUBJECTS.forEach((s,i)=>expect(bank.filter(q=>q.subject===s)).toHaveLength([20,80,20,80][i]));
   for(const q of bank){expect(()=>validateQuestion(q)).not.toThrow();expect(q.type).toBe('original');expect(q.year).toBeNull();expect(q.session).toBeNull();expect(q.verificationStatus).toBe('reviewed');expect(q.reviewNote).toContain('외부');expect(q.rights).toContain('CC BY 4.0');expect(q.explanation.length).toBeGreaterThan(30);}
 });
 it('6개 수치 변형 family 각 20개, 개념 80개를 분리 집계한다',()=>{
   expect(bank.filter(q=>!q.family)).toHaveLength(80);
   const families=new Set(bank.flatMap(q=>q.family?[q.family]:[]));expect(families.size).toBe(6);
   for(const f of families){const qs=bank.filter(q=>q.family===f);expect(qs).toHaveLength(20);expect(new Set(qs.map(q=>JSON.stringify(q.calculation!.values))).size).toBe(20);}
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
 };
 expect(formulas[c.kind]()).toBeCloseTo(c.result,9);
 const parsed=q.choices.map(x=>Number(x.split(' ')[0]));
 expect(parsed.filter(x=>Math.abs(x-c.result)<1e-8)).toHaveLength(1);
 expect(parsed[q.answer-1]).toBeCloseTo(c.result,9);
 expect(q.choices[q.answer-1]).toContain(c.unit);
 expect(q.explanation).toContain(c.unit);
});
