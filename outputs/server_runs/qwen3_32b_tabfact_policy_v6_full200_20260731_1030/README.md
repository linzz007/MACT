# Qwen3-32B TabFact policy v6 full200

- Purpose: full TabFact 200 validation after deterministic fact shortcuts for country pairs, zero-gold counts, before-date results, venue/date/competition, score-but-lose, second-smallest metric, and retirement thresholds.
- Model: qwen3-32b-local via vLLM on GPU 6,7, port 8000.
- Input source: canonical MyAgent TabFact full200 artifact, reduced to table/question/gold fields.
- Rows: 200.
