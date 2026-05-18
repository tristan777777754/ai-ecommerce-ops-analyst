# E-commerce Ops Analyst Web UI

Simple local web UI for the ontology-aware AI analyst.

## Run

Option A: environment variable:

```bash
OPENAI_API_KEY=your_key python3 webui/server.py
```

Option B: local `.env` file:

```bash
cp webui/.env.example .env
```

Edit `.env`, then run:

```bash
python3 webui/server.py
```

Then open:

```text
http://127.0.0.1:8787
```

Optional:

```bash
OPENAI_MODEL=gpt-5-mini PORT=8787 OPENAI_API_KEY=your_key python3 webui/server.py
```

## What It Uses

The server sends the analyst prompt and local project context to the OpenAI Responses API:

- `agent/ecommerce_ops_analyst_system_prompt.md`
- `outputs/business_recommendations/WEEKLY_OPS_BRIEF.md`
- `outputs/business_recommendations/BUSINESS_RECOMMENDATIONS.md`
- `outputs/business_recommendations/business_recommendations.csv`
- `outputs/AI_ANALYST_DEMO_QA.md`
- `ontology/actions.yml`
- `ontology/objects.yml`
- `ontology/links.yml`
- `wiki/ecommerce-ops-ontology/06-ai-analyst-behavior.md`
- `wiki/ecommerce-ops-ontology/07-evals-and-governance.md`

The API key is read only by the local Python server. It is not sent to the browser.
