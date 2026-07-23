# Qwen3-32B Blind200 MACT Full200 Ledger

最后更新：2026-07-23 19:25:23 CST

## 目标

在已完成 `core100` 的基础上，补跑 blind_holdout_200 后 100 条 MACT 输出，形成 Qwen3-32B 下 WTQ / TabFact / CRT 三数据集同 ID `blind200` paired 主证据。

本目录只保存 MACT 侧 raw/log/eval/paired/summary。myAgent 侧 blind200 输出继续使用 MyAgent 仓库中已经完成的 200 行结果。

## 数据口径

| item | value |
|---|---|
| model | Qwen3-32B local |
| served name | `qwen3-32b-local` |
| endpoint | `http://127.0.0.1:8000/v1` |
| dataset split | `/home/ubuntu/lzz/MyAgent/datasets_ready/blind_holdout_200_v1_2026-06-27/*.jsonl` |
| target rows | 200 per dataset |
| seed | copied from `qwen3_32b_blind200_mact_core100_20260722` |
| resume behavior | `--limit 200 --resume`, start index equals existing output line count |

## 当前状态

| dataset | output | rows | status |
|---|---|---:|---|
| WTQ | `wtq_mact_full200.jsonl` | 200/200 | complete; 5 context overflow failures |
| TabFact | `tabfact_mact_full200.jsonl` | 115/200 | running; row101-row115 ok |
| CRT | `crt_mact_full200.jsonl` | 100/200 | seeded from core100; tail100 pending |

## 进度记录

| time | dataset | rows | last id | status | notes |
|---|---|---:|---|---|---|
| 2026-07-23 13:25:38 CST | all | 100/200 each | seed | seeded | copied core100 raw/log/summary |
| 2026-07-23 13:33:25 CST | WTQ | 100/200 | seed | started | host-level `setsid -f bash run_wtq_resume.sh`; healthcheck ok |
| 2026-07-23 13:36:06 CST | WTQ | 101/200 | `nu-4099` | ok | token 8735; elapsed 84.3s |
| 2026-07-23 13:43:32 CST | WTQ | 104/200 | `nu-3939` | ok | row101-row104 all ok; last row token 16520; elapsed 173.7s |
| 2026-07-23 13:55:24 CST | WTQ | 109/200 | `nu-712` | ok | row101-row109 all ok; last row token 7551; elapsed 98.8s |
| 2026-07-23 14:08:29 CST | WTQ | 116/200 | `nu-2903` | ok | row101-row116 all ok; last row token 11749; elapsed 132.6s |
| 2026-07-23 14:15:29 CST | WTQ | 120/200 | `nu-3399` | ok | row101-row120 all ok; last row token 8017; elapsed 102.6s |
| 2026-07-23 14:24:07 CST | WTQ | 124/200 | `nu-3290` | failed | context overflow: input 6145 + max_tokens 2048 > 8192 |
| 2026-07-23 14:24:07 CST | WTQ | 125/200 | `nu-3922` | ok | runner continued after row124; last row token 8291; elapsed 116.7s |
| 2026-07-23 14:24:07 CST | WTQ | 126/200 | `nu-3527` | ok | runner continued; last row token 7678; elapsed 76.6s |
| 2026-07-23 14:37:48 CST | WTQ | 131/200 | `nu-1298` | ok | row127-row131 ok; last row token 6794; elapsed 67.1s |
| 2026-07-23 14:39:01 CST | WTQ | 133/200 | `nu-3139` | failed | context overflow: input 6145 + max_tokens 2048 > 8192 |
| 2026-07-23 14:55:56 CST | WTQ | 138/200 | `nu-824` | ok | row134-row138 ok; last row token 19077; elapsed 307.0s |
| 2026-07-23 15:08:55 CST | WTQ | 144/200 | `nu-976` | ok | row139-row144 ok; last row token 11989; elapsed 130.1s |
| 2026-07-23 15:08:55 CST | WTQ | 145/200 | `nu-2426` | ok | row145 ok; last row token 10617; elapsed 111.2s |
| 2026-07-23 15:17:48 CST | WTQ | 150/200 | `nu-4291` | ok | row146-row150 ok; last row token 7621; elapsed 58.9s |
| 2026-07-23 15:20:10 CST | WTQ | 151/200 | `nu-2973` | ok | row151 ok; last row token 8857; elapsed 100.5s |
| 2026-07-23 15:20:10 CST | WTQ | 152/200 | `nu-1313` | ok | row152 ok; last row token 11224; elapsed 98.6s |
| 2026-07-23 15:23:22 CST | WTQ | 153/200 | `nu-3488` | ok | row153 already included in raw checkpoint; last row token 5876; elapsed 43.4s |
| 2026-07-23 15:36:06 CST | WTQ | 154/200 | `nu-1030` | ok | row154 ok; last row token 28688; elapsed 286.6s |
| 2026-07-23 15:36:06 CST | WTQ | 155/200 | `nu-3027` | ok | row155 ok; last row token 8149; elapsed 77.4s |
| 2026-07-23 15:36:06 CST | WTQ | 156/200 | `nu-3487` | failed | context overflow: input 6145 + max_tokens 2048 > 8192 |
| 2026-07-23 15:36:06 CST | WTQ | 157/200 | `nu-1424` | ok | row157 ok; last row token 12536; elapsed 132.3s |
| 2026-07-23 15:36:06 CST | WTQ | 158/200 | `nu-4318` | ok | row158 ok; last row token 12200; elapsed 43.5s |
| 2026-07-23 15:36:06 CST | WTQ | 159/200 | `nu-2547` | ok | row159 ok; last row token 6919; elapsed 54.6s |
| 2026-07-23 15:36:06 CST | WTQ | 160/200 | `nu-2981` | ok | row160 ok; last row token 6861; elapsed 56.8s |
| 2026-07-23 15:36:06 CST | WTQ | 161/200 | `nu-2032` | ok | row161 ok; last row token 11062; elapsed 191.8s |
| 2026-07-23 15:38:28 CST | WTQ | 162/200 | `nu-1761` | ok | row162 ok; last row token 9027; elapsed 124.9s |
| 2026-07-23 15:40:06 CST | WTQ | 163/200 | `nu-3074` | ok | row163 ok; last row token 6026; elapsed 53.1s |
| 2026-07-23 15:40:06 CST | WTQ | 164/200 | `nu-2506` | ok | row164 ok; last row token 5781; elapsed 44.1s |
| 2026-07-23 15:42:35 CST | WTQ | 165/200 | `nu-65` | ok | row165 ok; last row token 15989; elapsed 114.2s |
| 2026-07-23 15:47:28 CST | WTQ | 166/200 | `nu-1446` | ok | row166 ok; last row token 21356; elapsed 284.3s |
| 2026-07-23 15:48:48 CST | WTQ | 167/200 | `nu-1246` | ok | row167 ok; last row token 8842; elapsed 94.9s |
| 2026-07-23 15:50:28 CST | WTQ | 168/200 | `nu-267` | ok | row168 ok; last row token 7529; elapsed 87.4s |
| 2026-07-23 15:51:30 CST | WTQ | 169/200 | `nu-4092` | ok | row169 ok; last row token 6851; elapsed 73.9s |
| 2026-07-23 15:56:46 CST | WTQ | 170/200 | `nu-107` | ok | row170 ok; last row token 7174; elapsed 48.0s |
| 2026-07-23 15:56:46 CST | WTQ | 171/200 | `nu-543` | ok | row171 ok; last row token 9311; elapsed 102.5s |
| 2026-07-23 15:56:46 CST | WTQ | 172/200 | `nu-3982` | ok | row172 ok; last row token 7084; elapsed 97.7s |
| 2026-07-23 15:56:46 CST | WTQ | 173/200 | `nu-721` | ok | row173 ok; last row token 8239; elapsed 97.7s |
| 2026-07-23 16:03:17 CST | WTQ | 174/200 | `nu-4162` | ok | row174 ok; last row token 15162; elapsed 286.9s |
| 2026-07-23 16:05:22 CST | WTQ | 175/200 | `nu-641` | ok | row175 ok; last row token 16995; elapsed 202.7s |
| 2026-07-23 16:11:12 CST | WTQ | 176/200 | `nu-1615` | ok | row176 ok; last row token 6561; elapsed 68.9s |
| 2026-07-23 16:11:12 CST | WTQ | 177/200 | `nu-1845` | ok | row177 ok; last row token 8050; elapsed 86.1s |
| 2026-07-23 16:11:12 CST | WTQ | 178/200 | `nu-888` | ok | row178 ok; last row token 2259; elapsed 21.3s |
| 2026-07-23 16:12:29 CST | WTQ | 179/200 | `nu-1498` | ok | row179 ok; last row token 17523; elapsed 220.9s |
| 2026-07-23 16:14:02 CST | WTQ | 180/200 | `nu-53` | ok | row180 ok; last row token 10299; elapsed 114.9s |
| 2026-07-23 16:20:50 CST | WTQ | 181/200 | `nu-2144` | ok | row181 ok; last row token 10515; elapsed 108.9s |
| 2026-07-23 16:20:50 CST | WTQ | 182/200 | `nu-717` | ok | row182 ok; last row token 5679; elapsed 28.6s |
| 2026-07-23 16:20:50 CST | WTQ | 183/200 | `nu-1970` | ok | row183 ok; last row token 7539; elapsed 93.1s |
| 2026-07-23 16:20:50 CST | WTQ | 184/200 | `nu-1915` | ok | row184 ok; last row token 8304; elapsed 106.3s |
| 2026-07-23 16:21:56 CST | WTQ | 185/200 | `nu-2183` | ok | row185 ok; last row token 7935; elapsed 100.8s |
| 2026-07-23 16:21:56 CST | WTQ | 186/200 | `nu-889` | ok | row186 ok; last row token 2344; elapsed 14.9s |
| 2026-07-23 16:27:54 CST | WTQ | 187/200 | `nu-3891` | ok | row187 ok; last row token 8200; elapsed 103.5s |
| 2026-07-23 16:27:54 CST | WTQ | 188/200 | `nu-996` | ok | row188 ok; last row token 15058; elapsed 117.3s |
| 2026-07-23 16:27:54 CST | WTQ | 189/200 | `nu-1317` | ok | row189 ok; last row token 6105; elapsed 44.1s |
| 2026-07-23 16:27:54 CST | WTQ | 190/200 | `nu-1421` | ok | row190 ok; last row token 9670; elapsed 66.2s |
| 2026-07-23 16:29:10 CST | WTQ | 191/200 | `nu-2934` | ok | row191 ok; last row token 7751; elapsed 57.6s |
| 2026-07-23 16:34:59 CST | WTQ | 192/200 | `nu-207` | ok | row192 ok; last row token 20731; elapsed 285.9s |
| 2026-07-23 16:34:59 CST | WTQ | 193/200 | `nu-1686` | ok | row193 ok; last row token 6364; elapsed 47.0s |
| 2026-07-23 16:34:59 CST | WTQ | 194/200 | `nu-2172` | ok | row194 ok; last row token 9746; elapsed 62.2s |
| 2026-07-23 16:48:31 CST | WTQ | 195/200 | `nu-2483` | ok | row195 ok; last row token 9850; elapsed 99.2s |
| 2026-07-23 16:48:31 CST | WTQ | 196/200 | `nu-2120` | ok | row196 ok; last row token 16805; elapsed 192.2s |
| 2026-07-23 16:48:31 CST | WTQ | 197/200 | `nu-1657` | ok | row197 ok; last row token 6708; elapsed 56.9s |
| 2026-07-23 16:48:31 CST | WTQ | 198/200 | `nu-983` | ok | row198 ok; last row token 23692; elapsed 138.0s |
| 2026-07-23 16:48:31 CST | WTQ | 199/200 | `nu-3200` | ok | row199 ok; last row token 6841; elapsed 72.4s |
| 2026-07-23 16:48:31 CST | WTQ | 200/200 | `nu-2332` | ok | row200 ok; last row token 10496; elapsed 78.9s; END_WTQ_FULL200 2026-07-23 16:45:33 CST |
| 2026-07-23 16:50:49 CST | WTQ | 200/200 | eval/paired | complete | generated `wtq_mact_full200_eval.json`, `wtq_mact_full200_errors.jsonl`, `wtq_mact_full200_paired.json`; paired myAgent 131/200 vs MACT 148/200; token ratio 0.5926 |
| 2026-07-23 19:02:34 CST | TabFact | 100/200 | started | host-level `setsid -f bash run_tabfact_resume.sh`; stdout `logs/tabfact_full200_resume_stdout.log`; first tail row still processing |
| 2026-07-23 19:03:39 CST | TabFact | 101/200 | `tabfact-test-10886` | ok | row101 ok; token 8623; elapsed 69.6s |
| 2026-07-23 19:04:39 CST | TabFact | 102/200 | `tabfact-test-12180` | ok | row102 ok; token 7743; elapsed 43.9s |
| 2026-07-23 19:14:07 CST | TabFact | 103/200 | `tabfact-test-10698` | ok | row103 ok; token 9185; elapsed 97.3s |
| 2026-07-23 19:14:07 CST | TabFact | 104/200 | `tabfact-test-4220` | ok | row104 ok; token 9609; elapsed 107.4s |
| 2026-07-23 19:14:07 CST | TabFact | 105/200 | `tabfact-test-2040` | ok | row105 ok; token 13215; elapsed 120.6s |
| 2026-07-23 19:14:07 CST | TabFact | 106/200 | `tabfact-test-7269` | ok | row106 ok; token 8081; elapsed 52.9s |
| 2026-07-23 19:14:07 CST | TabFact | 107/200 | `tabfact-test-4644` | ok | row107 ok; token 10471; elapsed 128.2s |
| 2026-07-23 19:14:07 CST | TabFact | 108/200 | `tabfact-test-6095` | ok | row108 ok; token 8952; elapsed 45.8s |
| 2026-07-23 19:15:25 CST | TabFact | 109/200 | `tabfact-test-5452` | ok | row109 ok; token 13127; elapsed 84.7s |
| 2026-07-23 19:23:57 CST | TabFact | 110/200 | `tabfact-test-8573` | ok | row110 ok; token 20668; elapsed 335.4s |
| 2026-07-23 19:23:57 CST | TabFact | 111/200 | `tabfact-test-9431` | ok | row111 ok; token 10267; elapsed 48.1s |
| 2026-07-23 19:23:57 CST | TabFact | 112/200 | `tabfact-test-5677` | ok | row112 ok; token 8563; elapsed 50.9s |
| 2026-07-23 19:23:57 CST | TabFact | 113/200 | `tabfact-test-3499` | ok | row113 ok; token 8431; elapsed 64.2s |
| 2026-07-23 19:25:23 CST | TabFact | 114/200 | `tabfact-test-9074` | ok | row114 ok; token 10162; elapsed 107.3s |
| 2026-07-23 19:25:23 CST | TabFact | 115/200 | `tabfact-test-3580` | ok | row115 ok; token 3141; elapsed 16.4s |
| 2026-07-23 19:36:18 CST | TabFact | 116/200 | `tabfact-test-12699` | ok | row116 ok; token 9102; elapsed 77.5s |
| 2026-07-23 19:36:18 CST | TabFact | 117/200 | `tabfact-test-1988` | ok | row117 ok; token 10138; elapsed 119.1s |
| 2026-07-23 19:36:18 CST | TabFact | 118/200 | `tabfact-test-3835` | ok | row118 ok; token 9649; elapsed 95.4s |
| 2026-07-23 19:36:18 CST | TabFact | 119/200 | `tabfact-test-5093` | ok | row119 ok; token 13539; elapsed 168.0s |
| 2026-07-23 19:36:18 CST | TabFact | 120/200 | `tabfact-test-12773` | ok | row120 ok; token 8836; elapsed 57.1s |
| 2026-07-23 21:55:48 CST | TabFact | 121/200 | `tabfact-test-7962` | ok | row121 ok; token 13109; elapsed 173.4s |
| 2026-07-23 21:55:48 CST | TabFact | 122/200 | `tabfact-test-5029` | ok | row122 ok; token 12451; elapsed 166.6s |
| 2026-07-23 21:55:48 CST | TabFact | 123/200 | `tabfact-test-2308` | ok | row123 ok; token 12563; elapsed 142.1s |
| 2026-07-23 21:55:48 CST | TabFact | 124/200 | `tabfact-test-2203` | ok | row124 ok; token 7949; elapsed 56.0s |
| 2026-07-23 21:55:48 CST | TabFact | 125/200 | `tabfact-test-11144` | ok | row125 ok; token 7823; elapsed 46.7s |
| 2026-07-23 21:55:48 CST | TabFact | 126/200 | `tabfact-test-9825` | ok | row126 ok; token 18529; elapsed 156.4s |
| 2026-07-23 21:55:48 CST | TabFact | 127/200 | `tabfact-test-10218` | ok | row127 ok; token 10426; elapsed 44.9s |
| 2026-07-23 21:55:48 CST | TabFact | 128/200 | `tabfact-test-965` | ok | row128 ok; token 10514; elapsed 115.0s |
| 2026-07-23 21:55:48 CST | TabFact | 129/200 | `tabfact-test-9229` | ok | row129 ok; token 9465; elapsed 95.2s |
| 2026-07-23 21:55:48 CST | TabFact | 130/200 | `tabfact-test-612` | ok | row130 ok; token 11534; elapsed 125.4s |
| 2026-07-23 21:55:48 CST | TabFact | 131/200 | `tabfact-test-6020` | ok | row131 ok; token 8373; elapsed 49.3s |
| 2026-07-23 21:55:48 CST | TabFact | 132/200 | `tabfact-test-7866` | ok | row132 ok; token 18484; elapsed 164.0s |
| 2026-07-23 21:55:48 CST | TabFact | 133/200 | `tabfact-test-6159` | ok | row133 ok; token 10846; elapsed 118.4s |
| 2026-07-23 21:55:48 CST | TabFact | 134/200 | `tabfact-test-10028` | ok | row134 ok; token 9593; elapsed 70.6s |
| 2026-07-23 21:55:48 CST | TabFact | 135/200 | `tabfact-test-10104` | ok | row135 ok; token 8125; elapsed 47.8s |
| 2026-07-23 21:55:48 CST | TabFact | 136/200 | `tabfact-test-9206` | ok | row136 ok; token 8097; elapsed 57.3s |
| 2026-07-23 21:55:48 CST | TabFact | 137/200 | `tabfact-test-6916` | ok | row137 ok; token 11049; elapsed 117.5s |
| 2026-07-23 21:55:48 CST | TabFact | 138/200 | `tabfact-test-9564` | ok | row138 ok; token 12800; elapsed 123.7s |
| 2026-07-23 21:55:48 CST | TabFact | 139/200 | `tabfact-test-7471` | ok | row139 ok; token 11106; elapsed 126.5s |
| 2026-07-23 21:55:48 CST | TabFact | 140/200 | `tabfact-test-778` | ok | row140 ok; token 12331; elapsed 78.9s |
| 2026-07-23 21:55:48 CST | TabFact | 141/200 | `tabfact-test-1570` | ok | row141 ok; token 11305; elapsed 125.9s |
| 2026-07-23 21:55:48 CST | TabFact | 142/200 | `tabfact-test-9674` | ok | row142 ok; token 8324; elapsed 60.0s |
| 2026-07-23 21:55:48 CST | TabFact | 143/200 | `tabfact-test-12466` | ok | row143 ok; token 8576; elapsed 67.9s |
| 2026-07-23 21:55:48 CST | TabFact | 144/200 | `tabfact-test-1259` | ok | row144 ok; token 8860; elapsed 74.9s |
| 2026-07-23 21:55:48 CST | TabFact | 145/200 | `tabfact-test-11246` | ok | row145 ok; token 8890; elapsed 43.5s |
| 2026-07-23 21:55:48 CST | TabFact | 146/200 | `tabfact-test-11589` | ok | row146 ok; token 10506; elapsed 116.1s |
| 2026-07-23 21:55:48 CST | TabFact | 147/200 | `tabfact-test-4166` | ok | row147 ok; token 10094; elapsed 126.1s |
| 2026-07-23 21:55:48 CST | TabFact | 148/200 | `tabfact-test-12708` | ok | row148 ok; token 9824; elapsed 117.6s |
| 2026-07-23 21:55:48 CST | TabFact | 149/200 | `tabfact-test-11520` | ok | row149 ok; token 9564; elapsed 97.6s |
| 2026-07-23 21:55:48 CST | TabFact | 150/200 | `tabfact-test-8166` | ok | row150 ok; token 10945; elapsed 112.5s |
| 2026-07-23 21:55:48 CST | TabFact | 151/200 | `tabfact-test-9469` | ok | row151 ok; token 9083; elapsed 89.7s |
| 2026-07-23 21:55:48 CST | TabFact | 152/200 | `tabfact-test-9313` | ok | row152 ok; token 8472; elapsed 70.0s |
| 2026-07-23 21:55:48 CST | TabFact | 153/200 | `tabfact-test-11386` | ok | row153 ok; token 9801; elapsed 99.4s |
| 2026-07-23 21:55:48 CST | TabFact | 154/200 | `tabfact-test-4143` | ok | row154 ok; token 9318; elapsed 96.7s |
| 2026-07-23 21:55:48 CST | TabFact | 155/200 | `tabfact-test-1121` | ok | row155 ok; token 19736; elapsed 280.8s |
| 2026-07-23 21:55:48 CST | TabFact | 156/200 | `tabfact-test-2850` | ok | row156 ok; token 17415; elapsed 173.1s |
| 2026-07-23 21:55:48 CST | TabFact | 157/200 | `tabfact-test-9981` | ok | row157 ok; token 8559; elapsed 77.9s |
| 2026-07-23 21:55:48 CST | TabFact | 158/200 | `tabfact-test-2013` | ok | row158 ok; token 8618; elapsed 47.8s |
| 2026-07-23 21:55:48 CST | TabFact | 159/200 | `tabfact-test-878` | ok | row159 ok; token 8918; elapsed 74.0s |
| 2026-07-23 21:55:48 CST | TabFact | 160/200 | `tabfact-test-10808` | ok | row160 ok; token 16011; elapsed 138.5s |
| 2026-07-23 21:55:48 CST | TabFact | 161/200 | `tabfact-test-7991` | ok | row161 ok; token 9798; elapsed 95.8s |
| 2026-07-23 21:55:48 CST | TabFact | 162/200 | `tabfact-test-3523` | ok | row162 ok; token 15189; elapsed 161.7s |
| 2026-07-23 21:55:48 CST | TabFact | 163/200 | `tabfact-test-9725` | ok | row163 ok; token 9371; elapsed 47.5s |
| 2026-07-23 21:55:48 CST | TabFact | 164/200 | `tabfact-test-3095` | ok | row164 ok; token 10737; elapsed 115.0s |
| 2026-07-23 21:55:48 CST | TabFact | 165/200 | `tabfact-test-6506` | ok | row165 ok; token 16925; elapsed 138.1s |
| 2026-07-23 21:55:48 CST | TabFact | 166/200 | `tabfact-test-6344` | ok | row166 ok; token 11238; elapsed 144.6s |
| 2026-07-23 21:55:48 CST | TabFact | 167/200 | `tabfact-test-7973` | ok | row167 ok; token 8800; elapsed 72.2s |
| 2026-07-23 21:55:48 CST | TabFact | 168/200 | `tabfact-test-8266` | ok | row168 ok; token 9663; elapsed 102.1s |
| 2026-07-23 21:55:48 CST | TabFact | 169/200 | `tabfact-test-3487` | ok | row169 ok; token 8560; elapsed 59.7s |
| 2026-07-23 21:55:48 CST | TabFact | 170/200 | `tabfact-test-8276` | ok | row170 ok; token 8697; elapsed 86.2s |
| 2026-07-23 21:55:48 CST | TabFact | 171/200 | `tabfact-test-12616` | ok | row171 ok; token 18293; elapsed 113.9s |
| 2026-07-23 21:55:48 CST | TabFact | 172/200 | `tabfact-test-9068` | ok | row172 ok; token 12380; elapsed 110.8s |
| 2026-07-23 21:55:48 CST | TabFact | 173/200 | `tabfact-test-2966` | ok | row173 ok; token 10092; elapsed 117.6s |
| 2026-07-23 21:55:48 CST | TabFact | 174/200 | `tabfact-test-12105` | ok | row174 ok; token 7723; elapsed 47.9s |
| 2026-07-23 21:55:48 CST | TabFact | 175/200 | `tabfact-test-9026` | ok | row175 ok; token 10945; elapsed 68.5s |
| 2026-07-23 21:55:48 CST | TabFact | 176/200 | `tabfact-test-8870` | ok | row176 ok; token 10732; elapsed 96.3s |
| 2026-07-23 21:55:48 CST | TabFact | 177/200 | `tabfact-test-11003` | ok | row177 ok; token 11326; elapsed 111.5s |
| 2026-07-23 21:55:48 CST | TabFact | 178/200 | `tabfact-test-3961` | ok | row178 ok; token 8966; elapsed 71.3s |
| 2026-07-23 21:55:48 CST | TabFact | 179/200 | `tabfact-test-11635` | ok | row179 ok; token 7209; elapsed 36.3s |
| 2026-07-23 21:55:48 CST | TabFact | 180/200 | `tabfact-test-5916` | ok | row180 ok; token 9359; elapsed 98.5s |
| 2026-07-23 21:55:48 CST | TabFact | 181/200 | `tabfact-test-3143` | ok | row181 ok; token 17348; elapsed 211.2s |
| 2026-07-23 21:55:48 CST | TabFact | 182/200 | `tabfact-test-2899` | ok | row182 ok; token 10087; elapsed 53.3s |
| 2026-07-23 21:55:48 CST | TabFact | 183/200 | `tabfact-test-3547` | ok | row183 ok; token 8795; elapsed 67.8s |
| 2026-07-23 21:55:48 CST | TabFact | 184/200 | `tabfact-test-4802` | ok | row184 ok; token 10847; elapsed 99.5s |
| 2026-07-23 21:55:48 CST | TabFact | 185/200 | `tabfact-test-8002` | ok | row185 ok; token 10802; elapsed 146.6s |
| 2026-07-23 21:55:48 CST | TabFact | 186/200 | `tabfact-test-4672` | ok | row186 ok; token 9085; elapsed 63.9s |
| 2026-07-23 21:55:48 CST | TabFact | 187/200 | `tabfact-test-5602` | ok | row187 ok; token 9948; elapsed 105.3s |
| 2026-07-23 21:55:48 CST | TabFact | 188/200 | `tabfact-test-5478` | ok | row188 ok; token 8568; elapsed 56.9s |
| 2026-07-23 21:55:48 CST | TabFact | 189/200 | `tabfact-test-5832` | ok | row189 ok; token 12031; elapsed 122.8s |
| 2026-07-23 21:55:48 CST | TabFact | 190/200 | `tabfact-test-2861` | ok | row190 ok; token 19692; elapsed 239.8s |
| 2026-07-23 21:55:48 CST | TabFact | 191/200 | `tabfact-test-5960` | ok | row191 ok; token 11202; elapsed 127.7s |
| 2026-07-23 21:55:48 CST | TabFact | 192/200 | `tabfact-test-12544` | ok | row192 ok; token 10865; elapsed 62.3s |
| 2026-07-23 21:55:48 CST | TabFact | 193/200 | `tabfact-test-4249` | ok | row193 ok; token 11527; elapsed 171.6s |
| 2026-07-23 21:55:48 CST | TabFact | 194/200 | `tabfact-test-3801` | ok | row194 ok; token 9275; elapsed 65.8s |
| 2026-07-23 21:55:48 CST | TabFact | 195/200 | `tabfact-test-10422` | ok | row195 ok; token 9405; elapsed 95.5s |
| 2026-07-23 21:55:48 CST | TabFact | 196/200 | `tabfact-test-8881` | ok | row196 ok; token 9015; elapsed 79.8s |
| 2026-07-23 21:55:48 CST | TabFact | 197/200 | `tabfact-test-2376` | ok | row197 ok; token 10756; elapsed 127.9s |
| 2026-07-23 21:55:48 CST | TabFact | 198/200 | `tabfact-test-7715` | ok | row198 ok; token 9042; elapsed 61.1s |
| 2026-07-23 21:55:48 CST | TabFact | 199/200 | `tabfact-test-7026` | ok | row199 ok; token 7937; elapsed 62.6s |
| 2026-07-23 21:55:48 CST | TabFact | 200/200 | `tabfact-test-6414` | ok | row200 ok; token 18308; elapsed 254.0s; END_TABFACT_FULL200 2026-07-23 21:55:21 CST |
| 2026-07-23 21:55:48 CST | TabFact | 200/200 | eval/paired | complete | generated `tabfact_mact_full200_eval.json`, `tabfact_mact_full200_errors.jsonl`, `tabfact_mact_full200_paired.json`; paired myAgent 185/200 vs MACT 189/200; token ratio 0.2241; errors 11 |

## 已知 core100 结论

```text
myAgent: 237/300 = 0.7900
MACT:    227/300 = 0.7567
token ratio: 0.5913
```

WTQ 的 `nu-4299` 和 `nu-2633` 在 seed 中保留为 MACT context length failure；full200 tail 新增 `nu-3290`、`nu-3139`、`nu-3487` 同类失败。不能删除或重跑后静默替换；若后续 repair，必须另行标注 repaired 口径。

WTQ full200 paired result:

```text
myAgent: 131/200 = 0.6550
MACT:    148/200 = 0.7400
token ratio: 0.5926
paired disagreement: both_correct=108, myagent_only=23, mact_only=40, neither=29
```

## 运行入口

```bash
setsid -f bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723/run_wtq_resume.sh
setsid -f bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723/run_tabfact_resume.sh
setsid -f bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723/run_crt_resume.sh
```

建议一次只跑一个数据集，避免同一个 Qwen3-32B vLLM 服务被多个 MACT 长任务压垮。

## 恢复规则

1. 先在 MyAgent 仓库确认服务健康：

```bash
cd /home/ubuntu/lzz/MyAgent
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate lzz-agent
source configs/server/qwen3_32b_2gpu_local.env
bash scripts/server/healthcheck_vllm_pool.sh configs/server/qwen3_32b_2gpu_local.env
```

2. 再检查行数：

```bash
wc -l /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723/*_mact_full200.jsonl
```

3. 行数少于 200 时，用对应 `run_*_resume.sh` 继续。

4. 每完成约 10 行或一个数据集，提交并推送 MACT `main`，再更新 MyAgent PRD。
