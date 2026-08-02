# Qwen3 Runtime Preflight

Generated: `2026-08-02 10:52:18 CST`

| item | value |
|---|---|
| status | `blocked_gpu_runtime_residual` |
| ready | `False` |
| recommendation | Do not start Qwen3 on the target GPUs yet. Ask the server owner to clear/reset the runtime or authorize another clean GPU pair. |
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
| 0 | 24029 | 49140 | 100 | NVIDIA GeForce RTX 4090 |
| 1 | 24029 | 49140 | 100 | NVIDIA GeForce RTX 4090 |
| 2 | 24009 | 49140 | 100 | NVIDIA GeForce RTX 4090 |
| 3 | 24029 | 49140 | 100 | NVIDIA GeForce RTX 4090 |
| 4 | 42005 | 49140 | 10 | NVIDIA GeForce RTX 4090 |
| 5 | 42001 | 49140 | 100 | NVIDIA GeForce RTX 4090 |
| 6 | 42003 | 49140 | 100 | NVIDIA GeForce RTX 4090 |
| 7 | 42005 | 49140 | 100 | NVIDIA GeForce RTX 4090 |

## GPU Process Evidence

Compute apps listed by `nvidia-smi`: `0`.

No compute apps were reported.
