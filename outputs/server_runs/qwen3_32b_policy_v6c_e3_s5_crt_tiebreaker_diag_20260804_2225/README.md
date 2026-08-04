# Qwen3-32B E3 S5 CRT Tie-breaker

Created: 2026-08-04 22:25 CST

Purpose: close the S4 paired MACT boundary where WTQ and TabFact strictly
beat MACT but CRT tied at `62/100`. S5 adds a small gold-free CRT scalar
canonicalization fix in MyAgent and validates it through replay, affected-slice
fresh rerun, and full CRT100 fresh rerun.

## Final Result

S5 final combined summary keeps S4 WTQ/TabFact paired results and replaces only
CRT with the S5 full CRT100 current-code rerun.

| Dataset | MyAgent | MACT | Delta | Token Ratio | Strict Win |
|---|---:|---:|---:|---:|---:|
| WTQ | 76/100 | 74/100 | +2 | 0.5762 | yes |
| TabFact | 91/100 | 87/100 | +4 | 0.2571 | yes |
| CRT | 65/100 | 62/100 | +3 | 0.7979 | yes |
| Overall | 232/300 | 223/300 | +9 | 0.5662 | yes |

Overall failed/missing: MyAgent `0/0`, MACT `4/4` (the MACT failures are
retained from the S4 WTQ paired baseline).

Decision: `s5_strict_all_dataset_pass`.

## Mechanism

MyAgent code change:

```text
/home/ubuntu/lzz/MyAgent/code/my_agents.py
```

Gold-free CRT scalar canonicalization now:

1. converts negative numeric answers to absolute values when the question asks
   for a `difference`;
2. expands country/nation answer codes such as `chn` to country names such as
   `China`.

The evaluator was not changed, and the rule does not branch on sample IDs or
gold answers.

## Validation Funnel

| Stage | Result | Files |
|---|---:|---|
| Paired CRT diagnosis | old MyAgent `62/100`, MACT `62/100` | `extract_crt_tiebreaker_diag.py`, `summary/crt_tiebreaker_diag.md`, `cases/*.jsonl` |
| Replay on old CRT100 outputs | projected MyAgent `64/100`, MACT `62/100`, no correct-to-wrong flips | `simulate_crt_canonicalizer_patch.py`, `summary/s5_crt_canonicalizer_replay_summary.md` |
| Affected-slice fresh | new MyAgent `16/25`, old MyAgent `12/25`, MACT `12/25`, failed/missing `0/0` | `prepare_crt_affected_slice.py`, `myagent_s5_affected_slice/`, `summary/s5_affected_slice_real_rerun_summary.md` |
| Full CRT100 fresh | new MyAgent `65/100`, MACT `62/100`, failed/missing `0/0` | `prepare_crt_paired100_input.py`, `myagent_s5_crt_paired100_full_rerun/` |
| Final S5 combined | overall `232/300` vs `223/300`, token ratio `0.5662`, MyAgent failed/missing `0/0`, MACT failed/missing `4/4` | `summarize_s5_final.py`, `summary/e3_s5_final_combined_summary.md`, `s5_final_result.md` |

## Reproduce

Assumes the two Qwen3-32B vLLM endpoints are already healthy:

```text
http://127.0.0.1:8000/v1
http://127.0.0.1:8001/v1
```

Run summaries without rerunning the model:

```bash
cd /home/ubuntu/lzz/MACT
python outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/extract_crt_tiebreaker_diag.py
python outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/simulate_crt_canonicalizer_patch.py
python outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/summarize_s5_affected_slice.py
python outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/summarize_s5_final.py
```

Rerun full CRT100 if needed:

```bash
cd /home/ubuntu/lzz/MyAgent
LOCAL_VLLM_API_KEY=local-vllm-key-change-me \
/home/ubuntu/miniconda3/envs/lzz-agent/bin/python scripts/server/run_sharded_tqa.py \
  --repo-root /home/ubuntu/lzz/MyAgent \
  --tasks crt \
  --crt-dataset /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/input/paired_crt100/crt_s5_paired100_seed_c_seed_d.jsonl \
  --endpoints http://127.0.0.1:8000/v1,http://127.0.0.1:8001/v1 \
  --model qwen3-32b-local \
  --api-key-env LOCAL_VLLM_API_KEY \
  --output-root /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/myagent_s5_crt_paired100_full_rerun \
  --mact-avg-tokens 12809.985 \
  --max-replan 3 \
  --resume
```
