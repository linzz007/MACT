# P4a After-Fix Gate-50 Summary

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305`

Scope: WTQ uses the original P4a current run because it already passed; TabFact and CRT use fresh after-fix full50 reruns in `myagent_current_after_fix/`. This is still a MyAgent current-only gate, not paired MACT.

| Dataset | Rows Input/Merged/Eval | Correct | Accuracy | Token Ratio vs MACT Full200 Ref | Avg Tokens | Avg Elapsed s | Failed | Missing | Gate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| wtq | 50/50/50 | 37/50 | 0.7400 | 0.6436 | 6763.0 | 17.28 | 0 | 0 | pass |
| tabfact | 50/50/50 | 45/50 | 0.9000 | 0.2132 | 2308.9 | 10.48 | 0 | 0 | pass |
| crt | 50/50/50 | 30/50 | 0.6000 | 0.7669 | 9823.8 | 21.99 | 0 | 0 | pass |
| overall | 150/150/150 | 112/150 | 0.7467 | 0.5533 | 6298.6 | 16.59 | 0 | 0 | p4a_after_fix_pass |

## Interpretation

After the mechanism fix, the P4a current-only new-seed gate meets the predeclared thresholds for all three datasets: WTQ >= 35/50, TabFact >= 45/50, CRT >= 30/50. Token ratios remain below the MACT full200 references. This does not yet prove paired MACT superiority on the new seed; the next evidence step is P4b paired MACT Gate-50 if we choose to spend the run time.
