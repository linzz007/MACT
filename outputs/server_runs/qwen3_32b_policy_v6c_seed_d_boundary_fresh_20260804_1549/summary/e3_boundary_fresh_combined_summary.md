# E3 Boundary Fresh Combined Summary

Generated: `2026-08-04 16:04:17 CST`

| seed | evidence | correct | token ratio | failed/missing | decision |
|---|---|---|---|---|---|
| seed_c | inherited_seed_c_s3 | 118/150 | 0.6073 | 0/0 | s3_seed_pass_run_paired_mact_candidate |
| seed_d | mixed | 111/150 | 0.5516 | 0/0 | seed_d_boundary_fresh_passes_current_gate |

Combined: `229/300`, token ratio `0.5794`, failed/missing `0/0`.
Decision: `boundary_fresh_pass_run_paired_mact_candidate`, paired_mact_next=`True`.

## Limitations

- Seed-D WTQ and TabFact are fresh v6c reruns.
- Seed-D CRT is inherited from the S3 run because this patch did not change CRT shortcut paths and CRT already passed its current gate.
- Seed-C is inherited from the S3 run; an optional full S3 rerun can be used before paired MACT if stricter freshness is required.
