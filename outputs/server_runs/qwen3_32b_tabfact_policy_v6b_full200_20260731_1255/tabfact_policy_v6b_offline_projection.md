# TabFact policy v6b offline projection

- Source run: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_tabfact_policy_v6_full200_20260731_1030`
- Base current: 185/200
- Projected current: 194/200
- MACT baseline: 189/200
- Triggered rows: 11
- Gains / harms: 9 / 0

## Gains

- `tabfact-test-7116` two_entity_appearance_count: false -> true
- `tabfact-test-3333` same_row_cell_mention: true -> false
- `tabfact-test-2518` column_value_count_assertion: false -> true
- `tabfact-test-8310` entity_metric_difference_value: false -> true
- `tabfact-test-3450` column_value_count_assertion: false -> true
- `tabfact-test-3499` column_value_count_assertion: false -> true
- `tabfact-test-12699` entity_attribute: true -> false
- `tabfact-test-12773` same_row_cell_mention: true -> false
- `tabfact-test-5960` first_last_time_gap: false -> true
