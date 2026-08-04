# Qwen3 Runtime Preflight

Generated: `2026-08-04 10:25:26 CST`

| item | value |
|---|---|
| status | `ready_existing_endpoint` |
| ready | `True` |
| recommendation | Use the queue script with the healthy endpoint list. |
| endpoints | `http://127.0.0.1:8000/v1` |
| target GPUs | `2, 3` |

## Endpoint Health

| endpoint | healthy | returncode | stderr |
|---|---:|---:|---|
| `http://127.0.0.1:8000/v1` | `True` | `0` | `` |

## GPU Snapshot

| gpu | memory used MiB | memory total MiB | util % | name |
|---:|---:|---:|---:|---|
| 0 | 45728 | 49140 | 99 | NVIDIA GeForce RTX 4090 |
| 1 | 25395 | 49140 | 0 | NVIDIA GeForce RTX 4090 |
| 2 | 45839 | 49140 | 0 | NVIDIA GeForce RTX 4090 |
| 3 | 45839 | 49140 | 0 | NVIDIA GeForce RTX 4090 |
| 4 | 42031 | 49140 | 11 | NVIDIA GeForce RTX 4090 |
| 5 | 42031 | 49140 | 100 | NVIDIA GeForce RTX 4090 |
| 6 | 42031 | 49140 | 100 | NVIDIA GeForce RTX 4090 |
| 7 | 42031 | 49140 | 100 | NVIDIA GeForce RTX 4090 |

## GPU Process Evidence

Compute apps listed by `nvidia-smi`: `2`.

| gpu uuid | pid | process | used memory MiB |
|---|---:|---|---:|
| `GPU-bd6c20f6-42b2-f1c4-7b85-4bf639543b50` | `158938` | `VLLM::Worker_TP0` | `45830` |
| `GPU-e64e35e3-7917-8d00-6785-d1cb484fb375` | `158939` | `VLLM::Worker_TP1` | `45830` |
