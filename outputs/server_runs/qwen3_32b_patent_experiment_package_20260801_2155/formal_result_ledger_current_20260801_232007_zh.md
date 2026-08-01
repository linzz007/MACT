# Current Formal Result Ledger

Generated: `2026-08-01 23:20:07 CST`

Overall status: `active_not_complete`.

## Completed Result Rows

| stage | dataset | rows input/merged/eval | MyAgent | MACT/ref | delta | token ratio | avg tokens | avg elapsed s | failed/missing | decision |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Qwen3-32B full200 anchor | wtq | 200/200/200 | 155/200 | 148/200 | +7 | 0.6187 | 6501.02 | 16.80 | 0/0 | `complete_full200_dataset_superiority` |
| Qwen3-32B full200 anchor | tabfact | 200/200/200 | 194/200 | 189/200 | +5 | 0.2014 | 2181.67 | 9.76 | 0/0 | `complete_full200_dataset_superiority` |
| Qwen3-32B full200 anchor | crt | 200/200/200 | 140/200 | 113/200 | +27 | 0.8461 | 10839.17 | 24.46 | 0/0 | `complete_full200_dataset_superiority` |
| Qwen3-32B full200 anchor | aggregate | 600/600/600 | 489/600 | 450/600 | +39 | 0.5717 | 6507.29 | 17.01 | 0/0 | `complete_full200_all_dataset_superiority` |
| P4b new-seed paired Gate-50 | wtq | 50/50/50 | 37/50 | 43/50 | -6 | 0.5980 | 6763.02 | 17.28 | 0/0 | `complete_dataset_risk` |
| P4b new-seed paired Gate-50 | tabfact | 50/50/50 | 45/50 | 44/50 | +1 | 0.2156 | 2308.92 | 10.48 | 0/0 | `complete_dataset_superiority` |
| P4b new-seed paired Gate-50 | crt | 50/50/50 | 30/50 | 24/50 | +6 | 0.7740 | 9823.82 | 21.99 | 0/0 | `complete_dataset_superiority` |
| P4b new-seed paired Gate-50 | aggregate | 150/150/150 | 112/150 | 111/150 | +1 | 0.5444 | 6298.59 | 16.59 | 0/0 | `accepted_existing_paired_gate_but_not_all_dataset_superiority` |

## Pending Result Rows

| stage | status | dataset | required rows | observed input rows | pass condition | evidence exists |
|---|---|---|---:|---:|---|---|
| WTQ targeted fresh affected slice | `pending_runtime` | wtq | 9 | 9 | merged_rows=9, eval_rows=9, failed=0, missing=0, myagent_correct>=7 | json=`False`, md=`False` |
| P4b WTQ after-fix full50 | `pending_after_targeted_pass` | wtq | 50 | 50 | myagent_correct>43, token_ratio<0.75, failed=0, missing=0 | json=`False`, md=`False` |
| E3 Seed-C current-only Gate-50 | `pending_runtime` | wtq_tabfact_crt | 150 | 150 | summary decision=run_paired_mact; failed/missing=0; token ratio below MACT full200 references | json=`False`, md=`False` |
| E3 Seed-C paired Gate-50 | `pending_after_current_only_pass` | wtq_tabfact_crt | 150 | 150 | strict_all_dataset_superiority=true for strong claim; existing paired criteria accepted only supports overall/token claim | json=`False`, md=`False` |
| E3 Seed-D current-only Gate-50 | `pending_runtime` | wtq_tabfact_crt | 150 | 150 | summary decision=run_paired_mact; failed/missing=0; token ratio below MACT full200 references | json=`False`, md=`False` |
| E3 Seed-D paired Gate-50 | `pending_after_current_only_pass` | wtq_tabfact_crt | 150 | 150 | strict_all_dataset_superiority=true for strong claim; existing paired criteria accepted only supports overall/token claim | json=`False`, md=`False` |
| Additional model gate funnel | `pending_new_candidate` | wtq_tabfact_crt | Gate-10=30, Gate-50=150, Gate-150=450, paired-200=600 | None | Follow prepare_model_gate_run.py and summarize_model_gate_results.py decisions; only Gate-150 decision=paired200 enters paired-200. | json=`False`, md=`False` |

## Runtime Preflight

Latest status: `blocked_gpu_runtime_residual`.
Recommendation: Do not start Qwen3 on the target GPUs yet. Ask the server owner to clear/reset the runtime or authorize another clean GPU pair.

## Can Write Now

- Qwen3-32B full200 stage: MyAgent beats MACT on WTQ, TabFact, and CRT with lower aggregate tokens.
- P4b new-seed Gate-50 supports overall/token evidence but exposes WTQ risk.

## Claims Not Supported Yet

- WTQ targeted fresh closure has completed.
- E3 Seed-C/Seed-D stability has run.
- A viable additional model gate has completed.
- The full patent experiment section is final.
