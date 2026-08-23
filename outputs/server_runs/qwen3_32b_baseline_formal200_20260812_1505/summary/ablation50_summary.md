# Qwen3-32B Ablation-50 Summary

Updated: 2026-08-23 23:30 CST

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
| No question routing | 0.660 | 0.900 | 0.760 | 116/150 = 0.7733 | 8353.59 | 21.077s | 0/0 |
| No risk scoring | 0.740 | 0.880 | 0.820 | 122/150 = 0.8133 | 6664.23 | 18.473s | 0/0 |

WTQ note: `no_deterministic_shortcuts` has WTQ `primary_accuracy=0.680` and `exact_match=0.660`; the table uses primary accuracy for dataset-level accuracy.

## File Locations

| Variant | Root |
|---|---|
| Legacy collaboration | `ablation/legacy_gate50/` |
| No strong verification | `ablation/no_strong_gate50/` |
| No deterministic shortcuts | `ablation/no_deterministic_shortcuts_gate50/` |
| No question routing | `ablation/no_question_routing_gate50/` |
| No risk scoring | `ablation/no_risk_scoring_gate50/` |
| No table compression | `ablation/no_table_compression_gate50/` prepared, not run |

Each variant root contains:

- `raw/<dataset>/*.jsonl`
- `merged/<dataset>_qwen3-32b-local.jsonl`
- `eval/<dataset>_qwen3-32b-local_eval.json`
- `logs/<dataset>/*.log`

## Interpretation

The current Gate-50 split does not isolate the value of strong verification: legacy and no-strong have identical accuracy and near-identical token/time. A targeted high-risk split is needed before making a strong patent claim about the strong-verification branch.

The deterministic-shortcut ablation is informative. Removing deterministic shortcuts reduces primary overall accuracy from `0.7733` to `0.7067` and increases average token usage from about `2516` to about `7465`. The main drops are on TabFact (`0.86` to `0.72`) and CRT (`0.80` to `0.72`). This supports a patent-describable claim that deterministic shortcuts / answer normalization reduce unnecessary LLM work while preserving accuracy on table verification and calculation reasoning tasks.

The no-question-routing ablation has the same overall primary accuracy as legacy/no-strong on this gate50 split, but it raises average token usage to `8353.59` and average time to `21.077s`. This supports question routing mainly as an efficiency/path-selection mechanism on the current split.

The no-risk-scoring ablation is not accuracy-negative on this broad gate50 split: it reaches `122/150 = 0.8133`, above legacy/no-strong, while average token usage rises to `6664.23`. This should be treated as boundary evidence. Do not claim from this split alone that risk scoring improves accuracy; the safer claim is that risk scoring is a selective cost/path-control component whose accuracy value needs targeted high-risk evidence.

## Prepared Expansion

New mechanism-isolation switches were added on 2026-08-23 and wired through `code/tqa.py` and `scripts/server/run_sharded_tqa.py`:

- `--disable_question_routing`: forces the complex path and records `question_routing_enabled=false`.
- `--disable_risk_scoring`: fixes the selective risk assessment at medium and records `risk_scoring_enabled=false`.
- `--disable_table_compression`: keeps the full original table and records `table_compression_enabled=false`.

Prepared scripts in this run package:

- `run_ablation_no_question_routing50.sh`
- `run_ablation_no_risk_scoring50.sh`
- `run_ablation_no_table_compression50.sh`

Static verification passed before execution:

- `python -m py_compile code/my_agents.py code/tqa.py scripts/server/run_sharded_tqa.py scripts/server/prepare_baseline_experiment_run.py`
- `python -m unittest discover -s tests -p 'test_myagent_pipeline.py' -v` (`243` tests)
- `bash -n` for the three prepared scripts
- `run_sharded_tqa.py --dry-run` confirmed the new flags are passed through to `code/tqa.py`

Execution status: `run_ablation_no_question_routing50.sh` and `run_ablation_no_risk_scoring50.sh` completed on 2026-08-23 using only GPUs `4,5,6,7`. `run_ablation_no_table_compression50.sh` remains prepared but not executed.
