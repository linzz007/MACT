# WTQ Formal-200 Patch Validation 7168923

Date: 2026-08-14 CST

Run root: `outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505`

Code:

- Runner HEAD: MyAgent `7168923`
- Main code patches: `d646885`, `7e18c84`, `cdc644c`

GPU / endpoint scope:

- `8000`: Qwen3-32B local service on GPUs `4,5`
- `8001`: Qwen3-32B local service on GPUs `6,7`
- GPUs `0,1,2,3` were not used; repeated `nvidia-smi pmon -c 1` checks showed no visible compute PID on `0-3`.

Files:

- Input: `input/formal200/wtq.jsonl`
- Output root: `diagnostics/wtq_formal200_patch_7168923`
- Merged: `diagnostics/wtq_formal200_patch_7168923/merged/wtq_qwen3-32b-local.jsonl`
- Eval: `diagnostics/wtq_formal200_patch_7168923/eval/wtq_qwen3-32b-local_eval.json`
- Compare JSON: `diagnostics/wtq_formal200_patch_7168923_compare.json`

## Main Result

| System | Rows | WTQ primary accuracy | Exact match | Avg token | Avg time | Failed/Missing |
|---|---:|---:|---:|---:|---:|---:|
| Old MyAgent formal200 | 200 | 141/200 = 0.7050 | 140/200 = 0.7000 | 6326.39 | 16.663s | 0/0 |
| Previous patched MyAgent `f102b96` | 200 | 147/200 = 0.7350 | 145/200 = 0.7250 | 6228.74 | 16.140s | 0/0 |
| Current patched MyAgent `7168923` | 200 | 157/200 = 0.7850 | 155/200 = 0.7750 | 6076.32 | 15.424s | 0/0 |
| MACT formal200 | 200 | 156/200 = 0.7800 | 153/200 = 0.7650 | 10484.65 | 115.088s | 4/4 |

Current MyAgent is now slightly above MACT on WTQ: `157/200` vs `156/200`.

Compared with MACT, current MyAgent WTQ uses about `57.95%` of MACT tokens and `13.40%` of MACT time, with no failed or missing answers.

## Delta

Against old MyAgent:

- Old wrong -> current right: `16` rows
- Old right -> current wrong: `0` rows
- Net WTQ gain: `+16`

Against previous patched MyAgent `f102b96`:

- Previous wrong -> current right: `10` rows
- Previous right -> current wrong: `0` rows
- Net WTQ gain: `+10`

Current MyAgent vs MACT:

| Pair bucket | Count |
|---|---:|
| Current MyAgent only correct | 18 |
| MACT only correct | 17 |

The remaining MACT-only WTQ rows are:

`nu-15`, `nu-35`, `nu-40`, `nu-49`, `nu-72`, `nu-82`, `nu-96`, `nu-112`, `nu-119`, `nu-127`, `nu-133`, `nu-136`, `nu-139`, `nu-159`, `nu-161`, `nu-173`, `nu-179`.

## Updated Overall Estimate

Replacing only WTQ with this new patched WTQ result, while keeping the existing TabFact and CRT formal200 results unchanged:

| Dataset | Current MyAgent correct | MACT correct |
|---|---:|---:|
| WTQ | 157/200 | 156/200 |
| TabFact | 162/200 | 185/200 |
| CRT | 133/200 | 124/200 |
| Overall | 452/600 = 0.7533 | 465/600 = 0.7750 |

Current MyAgent is now ahead on WTQ and CRT, but still behind overall because TabFact has a `23`-row deficit.

Updated overall token/time estimate for MyAgent is:

- Avg token: `(6076.32 + 2796.515 + 10430.63) / 3 = 6434.49`
- Avg time: `(15.424 + 13.400 + 23.134) / 3 = 17.319s`

Compared with MACT overall avg token `11318.89` and avg time `126.861s`, current MyAgent remains much cheaper: about `56.85%` of tokens and `13.65%` of time.

## Decision

The WTQ optimization subgoal is achieved for Qwen3-32B formal200: MyAgent exceeds MACT on WTQ while keeping token/time much lower.

The overall patent-data goal is not complete. The next priority should shift to TabFact, because the current overall gap is dominated by TabFact (`162/200` vs MACT `185/200`).
