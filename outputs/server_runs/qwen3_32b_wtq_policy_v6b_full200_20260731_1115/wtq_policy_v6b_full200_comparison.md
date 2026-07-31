# WTQ policy v6b full200 comparison

- Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_wtq_policy_v6b_full200_20260731_1115`
- MyAgent commit: `490c352`
- Merged rows: 200/200
- Current MyAgent: 155/200, avg tokens 6501.02, avg elapsed 16.80s, failures/missing 0/0
- Old MyAgent: 131/200, avg tokens 6226.93, avg elapsed 15.94s
- MACT: 148/200, avg tokens 10508.03, avg elapsed 114.78s, failures/missing 5/5
- Current vs MACT: +7 correct, token ratio 0.6187, elapsed ratio 0.1464
- Current vs old MyAgent: +24 correct, token ratio 1.0440
- Acceptance: WTQ pass = True

## Transition Counts

- old wrong -> current correct: 25
- old correct -> current wrong: 1
- MACT correct -> current wrong: 17
- current correct -> MACT wrong: 24
