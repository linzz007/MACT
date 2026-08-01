# Patent Package Checksums

Generated: `2026-08-01 23:39:13 CST`

| item | value |
|---|---:|
| checksum records | 74 |
| package files | 42 |
| manifest reference files | 51 |
| missing or pending references | 4 |

Verify from workspace root:

```bash
cd /home/ubuntu/lzz
sha256sum -c MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/SHA256SUMS
```

Missing or pending references are not checksum failures. They are expected for future WTQ fresh, E3, and multi-model outputs until those runs complete.

## Missing Or Pending References

- `wtq_e2_targeted_projection.fresh_summary_json_pending_path` -> `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_targeted_fresh_summary.json`
- `wtq_e2_targeted_projection.fresh_summary_md_pending_path` -> `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_targeted_fresh_summary.md`
- `wtq_e2_targeted_projection.after_targeted_summary_json_pending_path` -> `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_after_wtq_targeted_paired_summary.json`
- `wtq_e2_targeted_projection.after_targeted_summary_md_pending_path` -> `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_after_wtq_targeted_paired_summary.md`
