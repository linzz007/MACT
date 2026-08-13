# P0 Baseline Experiment Summary

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505`

## Main Table

| Method | WTQ Acc | TabFact Acc | CRT Acc | Overall Acc | Avg Token | Avg Time | Fail/Missing | Token Ratio to MACT |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MyAgent | 141/200 = 0.7050 | 162/200 = 0.8100 | 133/200 = 0.6650 | 436/600 = 0.7267 | 6517.84 | 17.73 | 0/0 | 0.5758 |
| MACT | 156/200 = 0.7800 | 185/200 = 0.9250 | 124/200 = 0.6200 | 465/600 = 0.7750 | 11318.89 | 126.86 | 4/4 | 1.0000 |
| Direct-CoT | 126/200 = 0.6300 | 149/200 = 0.7450 | 111/200 = 0.5550 | 386/600 = 0.6433 | 712.67 | 2.55 | 1/1 | 0.0630 |
| Single-Agent Pandas | 138/200 = 0.6900 | 159/200 = 0.7950 | 124/200 = 0.6200 | 421/600 = 0.7017 | 1074.24 | 7.60 | 22/28 | 0.0949 |

## Source Files

### MyAgent
- wtq: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505/myagent_formal200/merged/wtq_qwen3-32b-local.jsonl`
- tabfact: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505/myagent_formal200/merged/tabfact_qwen3-32b-local.jsonl`
- crt: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505/myagent_formal200/merged/crt_qwen3-32b-local.jsonl`

### MACT
- wtq: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505/mact/wtq_mact_formal200.jsonl`
- tabfact: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505/mact/tabfact_mact_formal200.jsonl`
- crt: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505/mact/crt_mact_formal200.jsonl`

### Direct-CoT
- wtq: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505/direct_cot_formal200/merged/wtq_qwen3-32b-local.jsonl`
- tabfact: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505/direct_cot_formal200/merged/tabfact_qwen3-32b-local.jsonl`
- crt: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505/direct_cot_formal200/merged/crt_qwen3-32b-local.jsonl`

### Single-Agent Pandas
- wtq: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505/single_agent_pandas_formal200/merged/wtq_qwen3-32b-local.jsonl`
- tabfact: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505/single_agent_pandas_formal200/merged/tabfact_qwen3-32b-local.jsonl`
- crt: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505/single_agent_pandas_formal200/merged/crt_qwen3-32b-local.jsonl`
