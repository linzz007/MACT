# Qwen3-32B MyAgent policy v6b all200 acceptance against MACT

## Verdict

- pass: True
- aggregate accuracy: MyAgent 489/600 (0.815) vs MACT 450/600 (0.750), delta +39
- aggregate token ratio: 0.571670 (MyAgent 6507.29 vs MACT 11382.95 avg tokens)
- aggregate elapsed ratio: 0.133695
- current failures / missing answers: 0 / 0

## Per Dataset

| Dataset | MyAgent | MACT | Delta | Token Ratio | Elapsed Ratio | Failures | Missing | Eval | Merged |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| wtq | 155/200 (0.775) | 148/200 (0.740) | +7 | 0.618672 | 0.146383 | 0 | 0 | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_wtq_policy_v6b_full200_20260731_1115/myagent_wtq_full200/eval/wtq_qwen3-32b-local_eval.json` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_wtq_policy_v6b_full200_20260731_1115/myagent_wtq_full200/merged/wtq_qwen3-32b-local.jsonl` |
| tabfact | 194/200 (0.970) | 189/200 (0.945) | +5 | 0.201432 | 0.094573 | 0 | 0 | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_tabfact_policy_v6b_full200_20260731_1255/myagent_tabfact_full200/eval/tabfact_qwen3-32b-local_eval.json` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_tabfact_policy_v6b_full200_20260731_1255/myagent_tabfact_full200/merged/tabfact_qwen3-32b-local.jsonl` |
| crt | 140/200 (0.700) | 113/200 (0.565) | +27 | 0.846150 | 0.149454 | 0 | 0 | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_crt_full200_current_20260730_1822/myagent_crt200/eval/crt_qwen3-32b-local_eval.json` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_crt_full200_current_20260730_1822/myagent_crt200/merged/crt_qwen3-32b-local.jsonl` |

## Source Comparison Files

- WTQ: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_wtq_policy_v6b_full200_20260731_1115/wtq_policy_v6b_full200_comparison.json`
- TabFact: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_tabfact_policy_v6b_full200_20260731_1255/tabfact_policy_v6b_full200_comparison.json`
- CRT: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_crt_full200_current_20260730_1822/crt_full200_current_comparison.json`

## Notes

- Accuracy passes per dataset: WTQ, TabFact, and CRT each exceed MACT on the same 200-row validation slice.
- Token usage is below MACT for every dataset; CRT saving is modest, while aggregate token usage is clearly lower due to WTQ and TabFact savings.
