# Qwen3 Runtime Preflight

Generated: `2026-08-03 09:32:03 CST`

| item | value |
|---|---|
| status | `ready_existing_endpoint` |
| ready | `True` |
| recommendation | Use the queue script with the healthy endpoint list. |
| endpoints | `http://127.0.0.1:8000/v1, http://127.0.0.1:8001/v1` |
| target GPUs | `0, 1, 2, 3` |

## Endpoint Health

| endpoint | healthy | returncode | stderr |
|---|---:|---:|---|
| `http://127.0.0.1:8000/v1` | `True` | `0` | `` |
| `http://127.0.0.1:8001/v1` | `True` | `0` | `` |

## GPU Snapshot

| gpu | memory used MiB | memory total MiB | util % | name |
|---:|---:|---:|---:|---|
| 0 | 45815 | 49140 | 0 | NVIDIA GeForce RTX 4090 |
| 1 | 45815 | 49140 | 0 | NVIDIA GeForce RTX 4090 |
| 2 | 45839 | 49140 | 0 | NVIDIA GeForce RTX 4090 |
| 3 | 45839 | 49140 | 0 | NVIDIA GeForce RTX 4090 |
| 4 | 42007 | 49140 | 0 | NVIDIA GeForce RTX 4090 |
| 5 | 42001 | 49140 | 0 | NVIDIA GeForce RTX 4090 |
| 6 | 42011 | 49140 | 0 | NVIDIA GeForce RTX 4090 |
| 7 | 42005 | 49140 | 0 | NVIDIA GeForce RTX 4090 |

## GPU Process Evidence

Compute apps listed by `nvidia-smi`: `4`.

| gpu uuid | pid | process | used memory MiB |
|---|---:|---|---:|
| `GPU-b60c901c-e7d4-6374-1110-66f13113b972` | `136786` | `VLLM::Worker_TP0` | `45806` |
| `GPU-97aea1c0-ca5f-a4a9-df19-b7711523ffea` | `136787` | `VLLM::Worker_TP1` | `45806` |
| `GPU-bd6c20f6-42b2-f1c4-7b85-4bf639543b50` | `136788` | `VLLM::Worker_TP0` | `45830` |
| `GPU-e64e35e3-7917-8d00-6785-d1cb484fb375` | `136789` | `VLLM::Worker_TP1` | `45830` |
