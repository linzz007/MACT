# Current Formal Result Ledger

Generated: `2026-08-03 11:42:55 CST`

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
| WTQ targeted fresh affected slice | wtq | 9/9/9 | 9/9 | 7/9 | +2 | n/a | 5437.33 | 8.98 | 0/0 | `pass` |
| P4b WTQ after-fix full50 | wtq | 50/50/50 | 46/50 | 43/50 | +3 | 0.5571 | 6300.16 | 14.51 | 0/0 | `complete_dataset_superiority` |
| P4b WTQ after-fix full50 | tabfact | 50/50/50 | 45/50 | 44/50 | +1 | 0.2156 | 2308.92 | 10.48 | 0/0 | `complete_dataset_superiority` |
| P4b WTQ after-fix full50 | crt | 50/50/50 | 30/50 | 24/50 | +6 | 0.7740 | 9823.82 | 21.99 | 0/0 | `complete_dataset_superiority` |
| P4b WTQ after-fix full50 | aggregate | 150/150/150 | 121/150 | 111/150 | +10 | 0.5310 | 6144.30 | 15.66 | 0/0 | `accepted_after_targeted_all_dataset_superiority` |
| E3 Seed-C current-only Gate-50 | wtq | 50/50/50 | 40/50 | n/a | n/a | 0.6013 | 6318.56 | 15.25 | 0/0 | `current_seed_gate_pass` |
| E3 Seed-C current-only Gate-50 | tabfact | 50/50/50 | 44/50 | n/a | n/a | 0.2604 | 2820.02 | 10.65 | 0/0 | `current_seed_gate_inspect` |
| E3 Seed-C current-only Gate-50 | crt | 50/50/50 | 30/50 | n/a | n/a | 0.9118 | 11679.92 | 25.33 | 0/0 | `current_seed_gate_pass` |
| E3 Seed-C current-only Gate-50 | aggregate | 150/150/150 | 114/150 | n/a | n/a | 0.6096 | 6939.50 | 17.07 | 0/0 | `stop_or_inspect` |
| E3 Seed-D current-only Gate-50 | wtq | 50/50/50 | 30/50 | n/a | n/a | 0.6329 | 6650.02 | 17.54 | 0/0 | `current_seed_gate_inspect` |
| E3 Seed-D current-only Gate-50 | tabfact | 50/50/50 | 38/50 | n/a | n/a | 0.2682 | 2905.16 | 11.68 | 0/0 | `current_seed_gate_inspect` |
| E3 Seed-D current-only Gate-50 | crt | 50/50/50 | 30/50 | n/a | n/a | 0.7829 | 10028.56 | 27.39 | 0/0 | `current_seed_gate_pass` |
| E3 Seed-D current-only Gate-50 | aggregate | 150/150/150 | 98/150 | n/a | n/a | 0.5735 | 6527.91 | 18.87 | 0/0 | `stop_or_inspect` |

## Pending Result Rows

| stage | status | dataset | required rows | observed input rows | pass condition | evidence exists |
|---|---|---|---:|---:|---|---|
| E3 Seed-C paired Gate-50 | `not_required` | wtq_tabfact_crt | 150 | 150 | strict_all_dataset_superiority=true for strong claim; existing paired criteria accepted only supports overall/token claim | json=`False`, md=`False` |
| E3 Seed-D paired Gate-50 | `not_required` | wtq_tabfact_crt | 150 | 150 | strict_all_dataset_superiority=true for strong claim; existing paired criteria accepted only supports overall/token claim | json=`False`, md=`False` |
| Additional model gate funnel | `pending_new_candidate` | wtq_tabfact_crt | Gate-10=30, Gate-50=150, Gate-150=450, paired-200=600 | None | Follow prepare_model_gate_run.py and summarize_model_gate_results.py decisions; only Gate-150 decision=paired200 enters paired-200. | json=`False`, md=`False` |

## Runtime Preflight

Latest status: `start_service_required`.
Recommendation: Start Qwen3 vLLM on the target GPUs, then rerun this preflight.

## Can Write Now

- Qwen3-32B full200 stage: MyAgent beats MACT on WTQ, TabFact, and CRT with lower aggregate tokens.
- P4b new-seed Gate-50 supports overall/token evidence but exposes WTQ risk.
- WTQ targeted fresh closure has completed, and P4b after-targeted Gate-50 shows all-dataset superiority.
- E3 Seed-C current-only Gate-50 is a documented stability boundary: overall 114/150, decision stop_or_inspect.
- E3 Seed-D current-only Gate-50 is a second documented stability boundary: overall 98/150, decision stop_or_inspect.
- E3 Seed-C/Seed-D offline boundary diagnosis has explained the current-gate boundary as semantic accuracy stability, not runtime/tool failure or token-budget failure.
- E4 latest readiness audit has completed with no untested local model path and no API provider profile, so no Gate-10 should be started yet.

## Claims Not Supported Yet

- A viable additional model gate has completed.
- The full patent experiment section is final.
