# Qwen3-32B Ablation-50 Summary

Updated: 2026-08-14 10:39 CST

Run package:

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505/
```

Endpoint/GPU policy:

- Use only `http://127.0.0.1:8000/v1` on GPUs `4,5` and `http://127.0.0.1:8001/v1` on GPUs `6,7`.
- Do not use GPUs `0,1,2,3` unless the user explicitly changes the constraint.

## Results

| Variant | WTQ | TabFact | CRT | Overall primary | Avg token | Avg time | Fail/Missing |
|---|---:|---:|---:|---:|---:|---:|---:|
| Legacy collaboration | 0.660 | 0.860 | 0.800 | 116/150 = 0.7733 | 2516.49 | 13.957s | 0/0 |
| No strong verification | 0.660 | 0.860 | 0.800 | 116/150 = 0.7733 | 2516.47 | 13.973s | 0/0 |
| No deterministic shortcuts | 0.680 | 0.720 | 0.720 | 106/150 = 0.7067 | 7464.50 | 22.227s | 0/0 |

WTQ note: `no_deterministic_shortcuts` has WTQ `primary_accuracy=0.680` and `exact_match=0.660`; the table uses primary accuracy for dataset-level accuracy.

## File Locations

| Variant | Root |
|---|---|
| Legacy collaboration | `ablation/legacy_gate50/` |
| No strong verification | `ablation/no_strong_gate50/` |
| No deterministic shortcuts | `ablation/no_deterministic_shortcuts_gate50/` |

Each variant root contains:

- `raw/<dataset>/*.jsonl`
- `merged/<dataset>_qwen3-32b-local.jsonl`
- `eval/<dataset>_qwen3-32b-local_eval.json`
- `logs/<dataset>/*.log`

## Interpretation

The current Gate-50 split does not isolate the value of strong verification: legacy and no-strong have identical accuracy and near-identical token/time. A targeted high-risk split is needed before making a strong patent claim about the strong-verification branch.

The deterministic-shortcut ablation is informative. Removing deterministic shortcuts reduces primary overall accuracy from `0.7733` to `0.7067` and increases average token usage from about `2516` to about `7465`. The main drops are on TabFact (`0.86` to `0.72`) and CRT (`0.80` to `0.72`). This supports a patent-describable claim that deterministic shortcuts / answer normalization reduce unnecessary LLM work while preserving accuracy on table verification and calculation reasoning tasks.
