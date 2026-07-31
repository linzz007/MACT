#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, '/home/ubuntu/lzz/MyAgent/code')
from evaluate_results import dataset_accuracy, load_jsonl, summarize_rows
RUN_DIR=Path('/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_coarse_ablation_gate50_20260801_0040')
MODEL_SAFE='qwen3-32b-local'
BASELINES={
 'wtq': {
  'current':'/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_wtq_policy_v6b_full200_20260731_1115/myagent_wtq_full200/merged/wtq_qwen3-32b-local.jsonl',
  'old':'/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_canonical_myagent_full200_raw_artifacts_20260730_2008/wtq_shortcutfix2/merged/wtq_qwen3-32b-local.jsonl',
  'mact':'/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723/wtq_mact_full200.jsonl'},
 'tabfact': {
  'current':'/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_tabfact_policy_v6b_full200_20260731_1255/myagent_tabfact_full200/merged/tabfact_qwen3-32b-local.jsonl',
  'old':'/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_canonical_myagent_full200_raw_artifacts_20260730_2008/tabfact_crt_current_blind200/merged/tabfact_qwen3-32b-local.jsonl',
  'mact':'/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723/tabfact_mact_full200.jsonl'},
 'crt': {
  'current':'/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_crt_full200_current_20260730_1822/myagent_crt200/merged/crt_qwen3-32b-local.jsonl',
  'old':'/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_canonical_myagent_full200_raw_artifacts_20260730_2008/tabfact_crt_current_blind200/merged/crt_qwen3-32b-local.jsonl',
  'mact':'/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723/crt_mact_full200.jsonl'},
}
def correct(rows): return sum(1 for r in rows if dataset_accuracy(r))
def compact(rows):
    s,_=summarize_rows(rows)
    return {'rows':s.get('num_samples'), 'correct':correct(rows), 'primary_accuracy':s.get('primary_accuracy'), 'avg_total_tokens':s.get('avg_total_tokens'), 'avg_elapsed_seconds':s.get('avg_elapsed_seconds'), 'num_failed_exec':s.get('num_failed_exec'), 'num_missing_answer':s.get('num_missing_answer'), 'num_em_mismatch':s.get('num_em_mismatch')}
def aligned(path, ids):
    by={r['id']:r for r in load_jsonl(path)}
    return [by[i] for i in ids]
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--variant', required=True)
    args=ap.parse_args()
    out={'variant':args.variant,'run_dir':str(RUN_DIR),'datasets':{}}
    for task in ['wtq','tabfact','crt']:
        merged=RUN_DIR/'variants'/args.variant/'merged'/f'{task}_{MODEL_SAFE}.jsonl'
        if not merged.exists():
            out['datasets'][task]={'status':'missing','merged_path':str(merged)}
            continue
        rows=load_jsonl(str(merged))
        ids=[r['id'] for r in rows]
        variant_summary=compact(rows)
        refs={name:compact(aligned(path, ids)) for name,path in BASELINES[task].items()}
        out['datasets'][task]={
            'status':'complete',
            'merged_path':str(merged),
            'eval_path':str(RUN_DIR/'variants'/args.variant/'eval'/f'{task}_{MODEL_SAFE}_eval.json'),
            'variant':variant_summary,
            'current_reference':refs['current'],
            'old_reference':refs['old'],
            'mact_reference':refs['mact'],
            'delta_vs_current':variant_summary['correct']-refs['current']['correct'],
            'delta_vs_old':variant_summary['correct']-refs['old']['correct'],
            'delta_vs_mact':variant_summary['correct']-refs['mact']['correct'],
            'token_ratio_vs_current':variant_summary['avg_total_tokens']/refs['current']['avg_total_tokens'] if refs['current']['avg_total_tokens'] else None,
            'token_ratio_vs_mact':variant_summary['avg_total_tokens']/refs['mact']['avg_total_tokens'] if refs['mact']['avg_total_tokens'] else None,
        }
    out_path=RUN_DIR/f'{args.variant}_gate50_summary.json'
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    md=[f'# {args.variant} Gate-50 Summary','', '| Dataset | Variant | Current Ref | Old Ref | MACT Ref | Δ vs Current | Token Ratio vs Current | Failed | Missing |', '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for task,d in out['datasets'].items():
        if d['status']!='complete':
            md.append(f'| {task} | missing | - | - | - | - | - | - | - |')
            continue
        md.append('| {task} | {vc}/{vr} | {cc}/{cr} | {oc}/{orows} | {mc}/{mr} | {delta:+d} | {tr:.4f} | {fail} | {miss} |'.format(task=task, vc=d['variant']['correct'], vr=d['variant']['rows'], cc=d['current_reference']['correct'], cr=d['current_reference']['rows'], oc=d['old_reference']['correct'], orows=d['old_reference']['rows'], mc=d['mact_reference']['correct'], mr=d['mact_reference']['rows'], delta=d['delta_vs_current'], tr=d['token_ratio_vs_current'] or 0, fail=d['variant']['num_failed_exec'], miss=d['variant']['num_missing_answer']))
    md_path=RUN_DIR/f'{args.variant}_gate50_summary.md'
    md_path.write_text('\n'.join(md)+'\n', encoding='utf-8')
    print(out_path)
    print(md_path)
if __name__=='__main__': main()
