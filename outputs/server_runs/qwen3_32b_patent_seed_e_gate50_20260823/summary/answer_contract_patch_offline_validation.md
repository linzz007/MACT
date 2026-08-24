# Answer-Contract Patch Offline Validation

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_seed_e_gate50_20260823`

This file records deterministic offline checks for the Seed-E answer-contract patch. It does not replace a focused model rerun; the current sandbox cannot reach the resident vLLM services on `127.0.0.1:8000/8001`.

| ID | Dataset | Previous | Offline Canonicalized | Contract Decimal Places | Old Code Valid Under New Contract | Expected Effect |
|---|---|---:|---:|---:|---|---|
| nu-3415 | wtq | `China` | `CHN` | `None` | `None` | direct canonicalization fix |
| crt-280 | crt | `0.16666666666666666` | `1/6` | `None` | `True` | direct canonicalization fix |
| crt-502 | crt | `13.64` | `13.64` | `3` | `False` | old two-decimal code rejected; requires focused model rerun |
| crt-290 | crt | `9.0` | `9.0` | `3` | `False` | old two-decimal code rejected; requires focused model rerun |

## Notes

- `nu-3415` and `crt-280` are direct post-execution normalization fixes: no additional model reasoning is needed once the old value is produced.
- `crt-502` and `crt-290` require a focused model rerun because the previous run already rounded inside generated code; the new contract rejects that old `round(..., 2)` shape and should force a new plan with three-decimal output.
- The patch also marks scalar `NaN` invalid so failed filters can trigger replanning rather than being accepted as a valid answer.
- Focused inputs are prepared at `input/diagnostic/seed_e_answer_contract_wtq.jsonl` and `input/diagnostic/seed_e_answer_contract_crt.jsonl`.
