# Qwen3-32B Patent Mechanism Evidence

Created: 2026-08-01 22:22 CST

This directory synthesizes existing frozen artifacts into a patent-facing
mechanism evidence matrix. It does not run Qwen3 and does not create a new
benchmark result.

Inputs:

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_all200_acceptance_20260731_132611/qwen3_policy_v6b_all200_acceptance_summary.json
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_coarse_ablation_gate50_20260801_0040/coarse_ablation_gate50_summary.json
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_mechanism_attribution_20260801_0033/mechanism_attribution_summary.json
```

Outputs:

```text
patent_mechanism_evidence_matrix.json
patent_mechanism_evidence_matrix.md
```

Regenerate:

```bash
python /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_patent_mechanism_evidence_20260801_2222/build_patent_mechanism_evidence.py
```
