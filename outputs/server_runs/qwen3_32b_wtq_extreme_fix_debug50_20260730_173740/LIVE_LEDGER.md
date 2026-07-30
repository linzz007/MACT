# Qwen3-32B WTQ Extreme Fix Debug50 Ledger

Run directory:

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_wtq_extreme_fix_debug50_20260730_173740
```

## Purpose

Measure whether the myAgent WTQ `only/top/first/last/earliest/latest` global-row compression patch converts the earlier offline row-recall gain into model-measured accuracy on the 50-row WTQ discordant debug subset.

This is a targeted debug subset, not a representative benchmark. It contains old myAgent wrong rows: 40 `mact_only` and 10 prioritized `neither`.

## Timeline

| time | item | status | notes |
|---|---|---|---|
| 2026-07-30 17:37:40 CST | run directory | created | input converted from `wtq_discordant_debug_subset_50.jsonl`; `answer` field populated from `gold_answer` |
| 2026-07-30 17:38:50 CST | vLLM services | started | Qwen3-32B on GPU `4,5` port `8000` and GPU `6,7` port `8001` |
| 2026-07-30 17:40:03 CST | healthcheck | ready | both ports returned `ok` |
| 2026-07-30 17:40 CST | debug50 run | started | two shards, 25 rows per endpoint |
| 2026-07-30 17:45 CST | shard01 row 22 | failed once | `verification_gap` crashed on numpy array truth-value comparison |
| 2026-07-30 17:49 CST | runtime fix 1 | applied | `verification_gap` now uses explicit non-empty execution-result detection |
| 2026-07-30 17:52 CST | shard01 row 22 retry | failed once | `_to_serializable` crashed on multi-element numpy array `.item()` |
| 2026-07-30 17:54 CST | runtime fix 2 | applied | `_to_serializable` now serializes numpy arrays through `tolist()` |
| 2026-07-30 17:55 CST | shard01 row 22 retry | failed once | top-level `_json_default` crashed on multi-element numpy array `.item()` |
| 2026-07-30 17:57 CST | runtime fix 3 | applied | `_json_default` now serializes numpy arrays through `tolist()` |
| 2026-07-30 17:58 CST | remaining 4 rows | complete | `nu-4299`, `nu-983`, `nu-1498`, `nu-2396` appended to shard01 output |
| 2026-07-30 17:58 CST | merge/eval | complete | final merged output has 50/50 rows, eval has 0 exec failures and 0 missing answers |
| 2026-07-30 17:59 CST | measured comparison | complete | `wtq_debug50_extreme_fix_measured_comparison.md/json` generated |

## Final Files

```text
input/wtq_debug50_with_answer.jsonl
myagent_debug50/raw/wtq/wtq_shard00_out.jsonl
myagent_debug50/raw/wtq/wtq_shard01_out.jsonl
myagent_debug50/merged/wtq_qwen3-32b-local.jsonl
myagent_debug50/eval/wtq_qwen3-32b-local_eval.json
wtq_debug50_extreme_fix_measured_comparison.md
wtq_debug50_extreme_fix_measured_comparison.json
qwen3_32b_4gpu_2svc.env
```

Failed attempt logs are retained for audit:

```text
myagent_debug50/logs/wtq/wtq_shard01.log
myagent_debug50/logs/wtq/wtq_shard01_remaining_22_25.log
myagent_debug50/logs/wtq/wtq_shard01_remaining_22_25_retry.log
myagent_debug50/logs/wtq/wtq_shard01_remaining_22_25_retry2.log
```

## Final Metrics

| scope | rows | old myAgent correct | new myAgent correct | MACT correct | new avg tokens | new avg compression |
|---|---:|---:|---:|---:|---:|---:|
| all debug50 | 50 | 0 | 14 | 40 | 6857.72 | 0.4781 |
| newly global-triggered | 18 | 0 | 10 | 15 | 6768.22 | 0.6055 |
| strict recoverable offline | 10 | 0 | 7 | 9 | 6327.00 | 0.6342 |
| mact_only bucket | 40 | 0 | 14 | 40 | 6698.20 | 0.4703 |
| neither bucket | 10 | 0 | 0 | 0 | 7495.80 | 0.5092 |

Overall debug50 token ratios:

```text
new myAgent / MACT: 0.6009
new myAgent / old myAgent: 1.0213
```

## Interpretation

The compression patch has measurable targeted benefit: the adversarial old-myAgent-wrong debug subset improves from `0/50` to `14/50`. The strict row-loss subset improves from `0/10` to `7/10`, which supports the original root-cause hypothesis.

The patch does not make myAgent beat MACT on this debug subset: MACT remains `40/50` because the subset was intentionally selected around MACT-only rows. The next model-measured step should be a representative WTQ regression slice, not another hand-picked discordant subset.
