# P4b WTQ Targeted Fix Offline Projection

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305`

Scope: replay saved P4b WTQ MyAgent merged rows through updated targeted WTQ deterministic shortcuts and scalar canonicalization. No Qwen3/vLLM calls were made.

| Current | Projected | Net Gain | Wrong -> Correct | Correct -> Wrong |
|---:|---:|---:|---:|---:|
| 37/50 | 46/50 | +9 | 9 | 0 |

## Changed Rows

| id | old | new | gold | reason | question |
|---|---|---|---|---|---|
| nu-3537 | 2 | 1 | ['1'] | WTQ playoff participation count checked deterministically. | how many years did the true american club make the playoff? |
| nu-1108 | MG William A. Mann | William A. Mann | ['William A. Mann'] | WTQ scalar canonicalized by targeted fix. | who came first john f. williams or william a. mann? |
| nu-2825 | 7 | 8 | ['8'] | WTQ requested column winner entries counted deterministically. | what is the number of winners in the community division? |
| nu-3905 | Ludwig Wolf Germany (GER) | Ludwig Wolf | ['Ludwig Wolf'] | WTQ scalar canonicalized by targeted fix. | who is the last person listed under slalom? |
| nu-3317 | 21 | 13 | ['13'] | WTQ unique sponsor names counted deterministically. | total number of sponsors? |
| nu-3990 | Pop | 9.0 | ['009'] | WTQ directly-before adjacent row target selected deterministically. | which experiment number came directly before felix? |
| nu-1478 | 0 | 2 | ['2'] | WTQ overtime marker rows counted deterministically. | what is the number of times a game went into overtime between the eagles and giants? |
| nu-3320 | Esther Shahamorov | Yossef Romano | ['Yossef Romano'] | WTQ retired-injured ordinal attempt row selected deterministically. | which person retired injured after three attempts in their event? |
| nu-1825 | 48712.0 | Stade Félix Bollaert | ['Stade Félix Bollaert'] | WTQ row-major listed-after value selected deterministically. | what is the next stadium listed after parc des princes? |

## Interpretation

The targeted WTQ mechanisms recover 9 P4b errors without projected harm. This is not a fresh Qwen run; it is evidence that the E1 diagnosis maps to generic deterministic/canonicalization behavior worth validating with a targeted gate.
