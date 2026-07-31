# Qwen3-32B WTQ verifier override target27

- Purpose: validate WTQ answer-shape/risk-gated verifier override and existing-total-row shortcut on projected gain and harm cases.
- Model: qwen3-32b-local via vLLM on GPU 6,7, port 8000.
- Input: 18 projected gain IDs plus 9 historical high-confidence-verifier harm guard IDs from canonical WTQ full200 artifact.
- Rows: 27.
