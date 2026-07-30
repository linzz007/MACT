# WTQ Extreme/Only Global Rows Offline Check

Generated at: 2026-07-30 17:32:46 CST

This is an offline compression-coverage check for the minimal myAgent patch that adds `only/top/first/last/earliest/latest` as global-row triggers. It does not call the model and is not an accuracy measurement.

## Summary

| metric | value |
|---|---:|
| debug_subset_rows | 50 |
| mact_only_rows | 40 |
| neither_rows | 10 |
| newly_global_triggered | 18 |
| literal_gold_row_loss_recoverable | 10 |
| affected_avg_old_cell_ratio | 0.2158 |
| affected_avg_estimated_new_cell_ratio_same_cols | 0.6055 |

## By Bucket

| bucket | newly_global_triggered | literal_gold_row_loss_recoverable |
|---|---:|---:|
| mact_only | 15 | 9 |
| neither | 3 | 1 |

## Newly Triggered Rows

| id | bucket | loss_category | terms | old rows | original rows | old ratio | estimated new ratio | question |
|---|---|---|---|---:|---:|---:|---:|---|
| nu-2873 | mact_only | gold_row_kept_col_dropped | only | 24 | 24 | 0.2000 | 0.2000 | who drove the only saab car? |
| nu-3949 | mact_only | gold_col_kept_row_dropped | only | 3 | 11 | 0.1169 | 0.4286 | derby and which other station are the only ones to not have a frequency? |
| nu-2223 | mact_only | gold_col_kept_row_dropped | only | 2 | 12 | 0.1250 | 0.7500 | name the only player transferred from albirex niigata. |
| nu-1951 | mact_only | gold_cell_selected | only | 12 | 18 | 0.1905 | 0.2857 | what was the outcome the only time a hard surface was used? |
| nu-4328 | mact_only | gold_col_kept_row_dropped | top | 1 | 10 | 0.0500 | 0.5000 | which country has the top number of silver medals won? |
| nu-2850 | mact_only | gold_col_kept_row_dropped | top | 2 | 6 | 0.1212 | 0.3636 | which singles charted in the top five of canada and also australia? |
| nu-2635 | mact_only | gold_cell_selected | first, only | 11 | 11 | 0.6667 | 0.6667 | list the only coach that won promotion to the first tier. |
| nu-2139 | mact_only | gold_col_kept_row_dropped | only | 2 | 7 | 0.1143 | 0.4000 | what is sinnamon's only hit of 1984? |
| nu-830 | mact_only | gold_cell_selected | last | 8 | 8 | 1.0000 | 1.0000 | who was ranked last among this group? |
| nu-3375 | mact_only | gold_col_kept_row_dropped | only | 3 | 8 | 0.3000 | 0.8000 | what was the competition in his only race in malaysia? |
| nu-1870 | mact_only | gold_col_kept_row_dropped | only | 2 | 9 | 0.2222 | 1.0000 | in the beginning of the show thee were only 3 judges, but what series did the show change to 4 judges? |
| nu-4291 | mact_only | gold_col_kept_row_dropped | only | 3 | 21 | 0.0714 | 0.5000 | name the position with only two players in such a position. |
| nu-1424 | mact_only | gold_not_literal_or_computed | first | 1 | 17 | 0.0252 | 0.4286 | what was the first date they played the 49ers? |
| nu-1845 | mact_only | gold_cell_selected | first | 6 | 8 | 0.4500 | 0.6000 | which is the first model listed with 10 krooni as the denomination? |
| nu-53 | mact_only | gold_col_kept_row_dropped | earliest | 2 | 32 | 0.0625 | 1.0000 | what is the earliest date kodak made 16mm film? |
| nu-2178 | neither | gold_col_kept_row_dropped | first | 2 | 21 | 0.0571 | 0.6000 | who was the first us ambassador to grenada appointed by bill clinton? |
| nu-3088 | neither | gold_cell_selected | last | 1 | 16 | 0.0234 | 0.3750 | what was the score of the last game of the season? |
| nu-4299 | neither | gold_cell_selected | first | 15 | 171 | 0.0877 | 1.0000 | which artist did jaycen joshua work with before his first job with rick ross? |

## Interpretation

- The patch targets row recall for boundary/extreme questions; it does not address planner arithmetic/counting or cases where the gold cell was already present but selected incorrectly.
- `literal_gold_row_loss_recoverable` is the strictest offline signal: the gold column was already kept and only the gold row was lost before the patch.
- The estimated new cell ratio assumes columns remain unchanged and only row retention expands to the original row count.
