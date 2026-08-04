# Current Formal Result Ledger

Generated: `2026-08-05 00:02:34 CST`

Overall status: `qwen3_strict_goal_complete_e4_pending`.

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
| E3 Seed-C S3 current-only after-guard Gate-50 | wtq | 50/50/50 | 40/50 | n/a | n/a | 0.5885 | 6183.56 | 14.63 | 0/0 | `s3_current_seed_gate_pass` |
| E3 Seed-C S3 current-only after-guard Gate-50 | tabfact | 50/50/50 | 46/50 | n/a | n/a | 0.2556 | 2768.34 | 10.92 | 0/0 | `s3_current_seed_gate_pass` |
| E3 Seed-C S3 current-only after-guard Gate-50 | crt | 50/50/50 | 32/50 | n/a | n/a | 0.9200 | 11785.16 | 25.72 | 0/0 | `s3_current_seed_gate_pass` |
| E3 Seed-C S3 current-only after-guard Gate-50 | aggregate | 150/150/150 | 118/150 | n/a | n/a | 0.6073 | 6912.35 | 17.09 | 0/0 | `s3_seed_pass_run_paired_mact_candidate` |
| E3 Seed-D S3 current-only after-guard Gate-50 | wtq | 50/50/50 | 28/50 | n/a | n/a | 0.6417 | 6743.50 | 17.74 | 0/0 | `s3_current_seed_gate_inspect` |
| E3 Seed-D S3 current-only after-guard Gate-50 | tabfact | 50/50/50 | 39/50 | n/a | n/a | 0.2613 | 2829.94 | 11.32 | 0/0 | `s3_current_seed_gate_inspect` |
| E3 Seed-D S3 current-only after-guard Gate-50 | crt | 50/50/50 | 30/50 | n/a | n/a | 0.7612 | 9751.56 | 25.23 | 0/0 | `s3_current_seed_gate_pass` |
| E3 Seed-D S3 current-only after-guard Gate-50 | aggregate | 150/150/150 | 97/150 | n/a | n/a | 0.5659 | 6441.67 | 18.10 | 0/0 | `s3_seed_stop_or_inspect` |
| E3 S3 current-only after-guard combined | aggregate | 300/300/300 | 215/300 | n/a | n/a | 0.5866 | 6677.01 | 17.59 | 0/0 | `s3_stop_or_inspect_boundary_remains` |
| E3 Seed-C v6c boundary-fresh current-only candidate | wtq | 50/50/50 | 40/50 | n/a | n/a | 0.5885 | 6183.56 | 14.63 | 0/0 | `boundary_fresh_current_seed_gate_pass` |
| E3 Seed-C v6c boundary-fresh current-only candidate | tabfact | 50/50/50 | 46/50 | n/a | n/a | 0.2556 | 2768.34 | 10.92 | 0/0 | `boundary_fresh_current_seed_gate_pass` |
| E3 Seed-C v6c boundary-fresh current-only candidate | crt | 50/50/50 | 32/50 | n/a | n/a | 0.9200 | 11785.16 | 25.72 | 0/0 | `boundary_fresh_current_seed_gate_pass` |
| E3 Seed-C v6c boundary-fresh current-only candidate | aggregate | 150/150/150 | 118/150 | n/a | n/a | 0.6073 | 6912.35 | 17.09 | 0/0 | `s3_seed_pass_run_paired_mact_candidate` |
| E3 Seed-D v6c boundary-fresh current-only candidate | wtq | 50/50/50 | 36/50 | n/a | n/a | 0.6217 | 6533.18 | 15.75 | 0/0 | `boundary_fresh_current_seed_gate_pass` |
| E3 Seed-D v6c boundary-fresh current-only candidate | tabfact | 50/50/50 | 45/50 | n/a | n/a | 0.2356 | 2552.16 | 10.25 | 0/0 | `boundary_fresh_current_seed_gate_pass` |
| E3 Seed-D v6c boundary-fresh current-only candidate | crt | 50/50/50 | 30/50 | n/a | n/a | 0.7612 | 9751.56 | 25.23 | 0/0 | `boundary_fresh_current_seed_gate_pass` |
| E3 Seed-D v6c boundary-fresh current-only candidate | aggregate | 150/150/150 | 111/150 | n/a | n/a | 0.5516 | 6278.97 | 17.08 | 0/0 | `seed_d_boundary_fresh_passes_current_gate` |
| E3 v6c boundary-fresh current-only combined candidate | aggregate | 300/300/300 | 229/300 | n/a | n/a | 0.5794 | 6595.66 | 17.08 | 0/0 | `boundary_fresh_pass_run_paired_mact_candidate` |
| E3 S4 paired MACT | wtq | 100/100/100 | 76/100 | 74/100 | +2 | 0.5762 | 6358.37 | 15.19 | MyAgent 0/0; MACT 4/4 | `s4_dataset_strict_pass` |
| E3 S4 paired MACT | tabfact | 100/100/100 | 91/100 | 87/100 | +4 | 0.2571 | 2660.25 | 10.58 | MyAgent 0/0; MACT 0/0 | `s4_dataset_strict_pass` |
| E3 S4 paired MACT | crt | 100/100/100 | 62/100 | 62/100 | +0 | 0.8078 | 10768.36 | 25.47 | MyAgent 0/0; MACT 0/0 | `s4_dataset_tie_strict_boundary` |
| E3 S4 paired MACT | aggregate | 300/300/300 | 229/300 | 223/300 | +6 | 0.5700 | 6595.66 | n/a | MyAgent 0/0; MACT 4/4 | `s4_paired_pass_existing_criteria_not_strict` |
| E3 S5 CRT affected-slice fresh | crt_affected_slice | 25/25/25 | 16/25 | 12/25 | +4 | 0.8218 | 11653.80 | 24.57 | MyAgent 0/0; MACT 0/0 | `s5_affected_slice_pass` |
| E3 S5 final paired combined | wtq | 100/100/100 | 76/100 | 74/100 | +2 | 0.5762 | 6358.37 | 15.19 | MyAgent 0/0; MACT 4/4 | `s5_dataset_strict_pass` |
| E3 S5 final paired combined | tabfact | 100/100/100 | 91/100 | 87/100 | +4 | 0.2571 | 2660.25 | 10.58 | MyAgent 0/0; MACT 0/0 | `s5_dataset_strict_pass` |
| E3 S5 final paired combined | crt | 100/100/100 | 65/100 | 62/100 | +3 | 0.7979 | 10636.63 | 24.64 | MyAgent 0/0; MACT 0/0 | `s5_dataset_strict_pass` |
| E3 S5 final paired combined | aggregate | 300/300/300 | 232/300 | 223/300 | +9 | 0.5662 | 6551.75 | n/a | MyAgent 0/0; MACT 4/4 | `s5_strict_all_dataset_pass` |

## Pending Result Rows

| stage | status | dataset | required rows | observed input rows | pass condition | evidence exists |
|---|---|---|---:|---:|---|---|
| Additional model gate funnel | `pending_new_candidate` | wtq_tabfact_crt | Gate-10=30, Gate-50=150, Gate-150=450, paired-200=600 | None | Follow prepare_model_gate_run.py and summarize_model_gate_results.py decisions; only Gate-150 decision=paired200 enters paired-200. | json=`False`, md=`False` |

## Runtime Preflight

Latest status: `ready_existing_endpoint`.
Recommendation: Use the queue script with the healthy endpoint list.

## Can Write Now

- Qwen3-32B full200 stage: MyAgent beats MACT on WTQ, TabFact, and CRT with lower aggregate tokens.
- P4b new-seed Gate-50 supports overall/token evidence and its WTQ risk has been closed by targeted fresh validation.
- E3 S5 final paired multi-seed result passes the current strong strict target: WTQ/TabFact/CRT all strictly exceed MACT, overall 232/300 vs 223/300, token ratio 0.5662, MyAgent failed/missing 0/0.
- S4 remains useful as historical boundary evidence: existing paired criteria passed, but CRT tied before the S5 answer-contract fix.
- E4 latest readiness audit has completed at 2026-08-05 00:02 with no untested local model path and no API provider profile/key, so no Gate-10 should be started yet.
- The current patent experiment section, completion audit, claim matrix, and patent disclosure draft have been updated with S5 and latest E4 no-candidate evidence.
- The fine-grained mechanism audit has completed for current Qwen3 patent scope; it is evidence synthesis, not a new benchmark row.

## Claims Not Supported Yet

- A viable additional model gate has completed.
- A standalone no-evidence-retention causal ablation has completed.
- The final experiment package closeout has completed after either an E4 candidate result or explicit acceptance of the no-candidate boundary.
