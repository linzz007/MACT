# P4a Mechanism Fix Targeted Qwen Validation

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305`

Scope: fresh Qwen3 runner execution over the affected rows identified by offline projection. This is not a full P4a rerun and not a paired MACT comparison.

| Dataset | Input/Merged/Eval | Correct | Accuracy | Avg Tokens | Avg Elapsed s | Failed | Missing |
|---|---:|---:|---:|---:|---:|---:|---:|
| tabfact | 3/3/3 | 3/3 | 1.0000 | 354.3 | 1.25 | 0 | 0 |
| crt | 9/9/9 | 9/9 | 1.0000 | 4738.2 | 8.07 | 0 | 0 |
| overall | 12/12/12 | 12/12 | 1.0000 | 3642.2 | 6.37 | 0 | 0 |

## Rows

### tabfact
- `tabfact-test-7551` correct=True pred=`true` gold=`['true']` shortcut=`TabFact only-not-country claim checked deterministically.` tokens=344 elapsed=1.50s
- `tabfact-test-7952` correct=True pred=`true` gold=`['true']` shortcut=`TabFact same-row cell mentions checked deterministically.` tokens=378 elapsed=1.19s
- `tabfact-test-11907` correct=True pred=`true` gold=`['true']` shortcut=`TabFact same-row cell mentions checked deterministically.` tokens=341 elapsed=1.07s

### crt
- `crt-287` correct=True pred=`Yes` gold=`['Yes']` shortcut=`CRT penalty score relation checked deterministically.` tokens=10130 elapsed=13.59s
- `crt-298` correct=True pred=`3:2` gold=`['3:2']` shortcut=`CRT medal ratio computed deterministically.` tokens=386 elapsed=1.57s
- `crt-242` correct=True pred=`1.01` gold=`['1.01']` shortcut=`CRT total-points season ratio rounded deterministically.` tokens=544 elapsed=4.27s
- `crt-704` correct=True pred=`6.4` gold=`['6.4']` shortcut=`CRT threshold-filtered average rounded deterministically.` tokens=12456 elapsed=14.67s
- `crt-232` correct=True pred=`434` gold=`['434']` shortcut=`CRT year-established variation computed as range.` tokens=385 elapsed=1.20s
- `crt-299` correct=True pred=`12.5%` gold=`['12.5%']` shortcut=`CRT medal probability computed deterministically.` tokens=8442 elapsed=14.65s
- `crt-105` correct=True pred=`netherlands` gold=`['netherlands']` shortcut=`` tokens=9568 elapsed=19.83s
- `crt-308` correct=True pred=`6:8` gold=`['6:8']` shortcut=`CRT partner win-loss ratio formatted deterministically.` tokens=332 elapsed=1.16s
- `crt-286` correct=True pred=`['manchester city and aalborg bk']` gold=`['manchester city and aalborg bk']` shortcut=`CRT penalty score relation checked deterministically.` tokens=401 elapsed=1.71s
