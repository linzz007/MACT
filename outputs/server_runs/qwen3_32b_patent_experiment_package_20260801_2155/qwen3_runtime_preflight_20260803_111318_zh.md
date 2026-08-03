# Qwen3 Runtime Preflight

Generated: `2026-08-03 11:13:18 CST`

| item | value |
|---|---|
| status | `start_service_required` |
| ready | `False` |
| recommendation | Start Qwen3 vLLM on the target GPUs, then rerun this preflight. |
| endpoints | `http://127.0.0.1:8000/v1, http://127.0.0.1:8001/v1` |
| target GPUs | `0, 1, 2, 3` |

## Endpoint Health

| endpoint | healthy | returncode | stderr |
|---|---:|---:|---|
| `http://127.0.0.1:8000/v1` | `False` | `7` | `curl: (7) Failed to connect to 127.0.0.1 port 8000 after 0 ms: Couldn't connect to server` |
| `http://127.0.0.1:8001/v1` | `False` | `7` | `curl: (7) Failed to connect to 127.0.0.1 port 8001 after 0 ms: Couldn't connect to server` |

## GPU Snapshot

| gpu | memory used MiB | memory total MiB | util % | name |
|---:|---:|---:|---:|---|
| 0 | 3 | 49140 | 0 | NVIDIA GeForce RTX 4090 |
| 1 | 3 | 49140 | 0 | NVIDIA GeForce RTX 4090 |
| 2 | 3 | 49140 | 0 | NVIDIA GeForce RTX 4090 |
| 3 | 3 | 49140 | 0 | NVIDIA GeForce RTX 4090 |
| 4 | 42013 | 49140 | 10 | NVIDIA GeForce RTX 4090 |
| 5 | 42007 | 49140 | 100 | NVIDIA GeForce RTX 4090 |
| 6 | 42015 | 49140 | 100 | NVIDIA GeForce RTX 4090 |
| 7 | 42011 | 49140 | 100 | NVIDIA GeForce RTX 4090 |

## GPU Process Evidence

Compute apps listed by `nvidia-smi`: `0`.

No compute apps were reported.
