# Qwen3-32B WTQ policy v6b full200

- Purpose: fresh WTQ full200 validation after MyAgent commit `490c352`.
- Model: `qwen3-32b-local` via vLLM on GPU `6,7`, port `8000`.
- Endpoint: `http://127.0.0.1:8000/v1`.
- Input: `input/wtq_full200.jsonl`, copied from the policy-v6 full200 input.
- Rows: 200.
- MACT baseline: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723/wtq_mact_full200.jsonl`.
- Old MyAgent baseline: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_canonical_myagent_full200_raw_artifacts_20260730_2008/wtq_shortcutfix2/raw/wtq/wtq_shard00_out.jsonl`.
- Reason for fresh run: policy-v6 partial exposed regressions on `nu-4268` and `nu-484`; do not resume the old raw file after v6b code changes.

Run command:

```bash
cd /home/ubuntu/lzz/MyAgent
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate lzz-agent
export LOCAL_VLLM_API_KEY=local-vllm-key-change-me
python scripts/server/run_sharded_tqa.py \
  --repo-root . \
  --tasks wtq \
  --wtq-dataset /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_wtq_policy_v6b_full200_20260731_1115/input/wtq_full200.jsonl \
  --endpoints http://127.0.0.1:8000/v1 \
  --model qwen3-32b-local \
  --api-key-env LOCAL_VLLM_API_KEY \
  --output-root /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_wtq_policy_v6b_full200_20260731_1115/myagent_wtq_full200 \
  --max-replan 3 \
  --mact-avg-tokens 10508.03 \
  --resume
```
