# Qwen3-32B TabFact policy v6b full200

- Purpose: fresh TabFact full200 validation after MyAgent commit `ef19d9d`.
- Model: `qwen3-32b-local` via vLLM on GPU `6,7`, port `8000`.
- Endpoint: `http://127.0.0.1:8000/v1`.
- Input: `input/tabfact_full200.jsonl`, copied from the policy-v6 full200 input.
- Rows: 200.
- MACT baseline: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723/tabfact_mact_full200.jsonl`.
- Old MyAgent baseline: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_canonical_myagent_full200_raw_artifacts_20260730_2008/tabfact_crt_current_blind200/merged/tabfact_qwen3-32b-local.jsonl`.
- Offline projection from policy-v6 raw: `194/200` vs MACT `189/200`, gains/harms `9/0`.

Run command:

```bash
cd /home/ubuntu/lzz/MyAgent
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate lzz-agent
export LOCAL_VLLM_API_KEY=local-vllm-key-change-me
python scripts/server/run_sharded_tqa.py \
  --repo-root . \
  --tasks tabfact \
  --tabfact-dataset /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_tabfact_policy_v6b_full200_20260731_1255/input/tabfact_full200.jsonl \
  --endpoints http://127.0.0.1:8000/v1 \
  --model qwen3-32b-local \
  --api-key-env LOCAL_VLLM_API_KEY \
  --output-root /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_tabfact_policy_v6b_full200_20260731_1255/myagent_tabfact_full200 \
  --max-replan 3 \
  --mact-avg-tokens 10830.825 \
  --resume
```
