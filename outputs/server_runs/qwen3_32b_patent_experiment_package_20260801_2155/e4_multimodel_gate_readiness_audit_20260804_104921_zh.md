# E4 Multi-Model Gate Readiness Audit

Generated: `2026-08-04 10:49:21 CST`

Decision: `no_candidate_wait`.

| item | value |
|---|---|
| can start Gate-10 now | `False` |
| local models discovered | `4` |
| untested local models | `0` |
| API keys present | `0` |
| API provider profiles | `0` |
| default GPU pool available | `False` |
| visible model/runner processes | `2` |

## Local Models

| model | paths | status |
|---|---|---|
| Qwen2.5-14B-Instruct-AWQ | `/home/ubuntu/models/Qwen2.5-14B-Instruct-AWQ` | `known_tested_or_no_go` |
| Qwen2.5-3B-Instruct | `/home/ubuntu/models/Qwen2.5-3B-Instruct` | `known_tested_or_no_go` |
| Qwen3-14B-AWQ | `/home/ubuntu/models/Qwen3-14B-AWQ` | `known_tested_or_no_go` |
| Qwen3-32B | `/home/ubuntu/.cache/huggingface/hub/models--Qwen--Qwen3-32B/snapshots/9216db5781bf21249d130ec9da846c4624c16137`<br>`/home/ubuntu/models/Qwen3-32B` | `known_tested_or_no_go` |

## API Readiness

- API keys present: `[]`
- API provider profiles: `[]`

## Runtime Snapshot

| GPU | memory MiB | util % |
|---:|---:|---:|
| 0 | 45815 | 0 |
| 1 | 45815 | 0 |
| 2 | 45839 | 0 |
| 3 | 45839 | 0 |
| 4 | 42031 | 100 |
| 5 | 42031 | 10 |
| 6 | 42031 | 100 |
| 7 | 42031 | 100 |

Visible model/runner processes: `2`.

## Conclusion

No E4 Gate-10 should start now: no untested local model path and no API provider profile are available. Keep E4 pending/no-candidate and avoid rerunning known no-go models.

## Next Actions

- If untested_local_model_paths becomes non-empty, run prepare_model_gate_run.py --readiness-audit <latest audit> and start Gate-10.
- If an API key appears, generate an API gate run with prepare_model_gate_run.py --backend api and run healthcheck_services.sh before Gate-10.
- If no candidates are present, keep E4 pending/no-candidate and do not consume GPU time on known no-go models.
