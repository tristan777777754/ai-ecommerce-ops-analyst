# E-commerce Ops Ontology Wiki

This wiki converts the local Palantir AIP learning material into an ontology design for the Olist e-commerce operations project.

The purpose is not to copy Palantir documentation. The purpose is to translate the AIP method into this project's business world:

```text
Raw Olist data
  -> Lark Base analysis layer
  -> business objects and links
  -> object-level metrics and risk state
  -> governed action types
  -> AI analyst behavior
  -> evals, guardrails, and demo workflow
```

The central operating question is:

> What should the marketplace manager do this week, and why?

## Current Evidence Layer

The first analysis checkpoint already exists in Lark Base:

- Raw data Base: `AI E-commerce Ops Analyst - Raw Data`
- Analysis layer Base: `AI E-commerce Ops Analyst - Analysis Layer`
- Dashboard: `E-commerce Ops Analysis Dashboard`
- Analysis tables:
  - `executive_summary`
  - `monthly_revenue_trend`
  - `order_facts`
  - `customer_rfm`
  - `rfm_segment_summary`
  - `dormant_high_value`
  - `seller_performance`
  - `seller_risk_watchlist`
  - `category_performance`
  - `category_opportunity`
  - `product_performance_top`
  - `delivery_risk_by_state`
  - `review_risk_by_category`

This means the project is ready to move from analysis tables to an ontology-backed operating model.

## Wiki Structure

1. [AIP Method Translation](01-aip-method-translation.md)
2. [Business Objects](02-business-objects.md)
3. [Object Links](03-object-links.md)
4. [Metrics and Signals](04-metrics-and-signals.md)
5. [Logic and Actions](05-logic-and-actions.md)
6. [AI Analyst Behavior](06-ai-analyst-behavior.md)
7. [Evals and Governance](07-evals-and-governance.md)
8. [Demo Operating Workflow](08-demo-operating-workflow.md)

## Local Method Sources

This wiki is based on the local Palantir AIP wiki in `wiki/palantir-aip/`, especially:

- `LEARNING_GUIDE_ZH.md`
- `pages/foundry-aip-overview.md`
- `pages/foundry-aip-aip-features.md`
- `pages/foundry-aip-analyst-core-concepts.md`
- `pages/foundry-chatbot-studio-tools.md`
- `pages/foundry-logic-overview.md`
- `pages/foundry-logic-core-concepts.md`
- `pages/foundry-logic-blocks.md`
- `pages/foundry-logic-execution-mode-settings.md`
- `pages/foundry-aip-evals-overview.md`
- `pages/foundry-aip-evals-ontology-edits.md`
- `pages/foundry-aip-ethics-governance.md`
- `pages/foundry-aip-aip-security.md`
- `pages/foundry-aip-aip-observability.md`
- `pages/foundry-ai-fde-best-practices.md`

## Design Rule

The ontology should model the business, not the tables.

Tables are evidence. Objects are the operating concepts. Actions are the approved moves that an operator can take after reviewing evidence.

