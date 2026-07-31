# TabFact policy v6 full200 comparison

- Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_tabfact_policy_v6_full200_20260731_1030`
- MyAgent commit: `490c352`
- Merged rows: 200/200
- Current MyAgent: 185/200, avg tokens 2320.97, avg elapsed 10.50s, failures/missing 0/0
- Old MyAgent: 185/200, avg tokens 2426.89, avg elapsed 10.76s
- MACT: 189/200, avg tokens 10830.83, avg elapsed 103.16s, failures/missing 0/0
- Current vs MACT: -4 correct, token ratio 0.2143, elapsed ratio 0.1018
- Current vs old MyAgent: 0 correct, token ratio 0.9564
- Acceptance: TabFact pass = False

## Transition Counts

- old wrong -> current correct: 8
- old correct -> current wrong: 8
- MACT correct -> current wrong: 11
- current correct -> MACT wrong: 7
