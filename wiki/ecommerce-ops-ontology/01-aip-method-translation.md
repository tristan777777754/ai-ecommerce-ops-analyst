# AIP Method Translation

## AIP Mental Model for This Project

In the local Palantir AIP wiki, AIP is described as an operating layer that connects AI with data, ontology, governance, applications, evaluations, and observability.

For this project, the translated mental model is:

```text
Lark Base analysis layer = data and evidence foundation
Ontology = business object model
AIP Analyst style = natural-language analysis over trusted context
AIP Logic style = repeatable workflows that compute risk and propose actions
Actions = controlled ontology edits or operational recommendations
Evals = tests that check grounding, policy, and consistency
Governance = approval, auditability, and human control
```

This is why the project should not stop at a dashboard. A dashboard shows metrics. An ontology-backed AI operating model explains what business objects exist, what state they are in, how they relate, and what actions are allowed.

## How the Palantir Concepts Map to E-commerce Ops

| AIP concept | Project translation | E-commerce example |
|---|---|---|
| Ontology | Business objects, properties, links, and actions | Customer, Seller, ProductCategory, DeliveryRisk |
| AIP Analyst context | Tables or objects given to the analyst | `seller_risk_watchlist`, `customer_rfm`, `review_risk_by_category` |
| Analysis provenance | Evidence trail for how an answer was reached | Recommendation cites seller orders, revenue, late rate, low review rate |
| Object query tool | AI can inspect object properties and traverse links | From Seller to OrderItems to Reviews |
| Function tool | AI can call deterministic calculations | Compute reliability score or risk priority |
| Action tool | AI can create or propose an approved edit | Create `BusinessRecommendation` for `InvestigateSeller` |
| AIP Logic | Workflow composed from query, calculation, LLM, conditionals, actions | Daily Ops Brief workflow |
| AIP Evals | Test cases and evaluation criteria | Check that recommendations meet trigger thresholds |
| Governance | Permissions, approval, audit, human oversight | All first-version actions stay `proposed` until approved |
| Observability | Run history, logs, traces, metrics | Track which workflow generated each recommendation |

## Project-Specific Method

The ontology should be built in this order:

1. Start from the Lark analysis layer as evidence.
2. Define the business objects that operators actually reason about.
3. Define links so the AI can move across the business world.
4. Attach metrics and state to objects.
5. Define approved action types with trigger logic and evidence requirements.
6. Define AI analyst behavior so answers are grounded and cautious.
7. Define evals and guardrails before treating the system as production-like.
8. Use the demo workflow to show the operating loop.

## What Counts as Ontology Here

Ontology is not only a schema. In this project, ontology means:

- Object types: Customer, Order, Seller, ProductCategory, ReviewRisk, BusinessRecommendation.
- Properties: revenue, recency, low review rate, delivery delay, reliability score.
- Links: Customer placed Order, Order contains OrderItem, OrderItem fulfilled by Seller.
- Functions: risk scoring, RFM segmentation, Pareto classification, action priority logic.
- Actions: SendReactivationOffer, InvestigateSeller, MonitorDeliveryRisk.
- Guardrails: evidence requirements, approval rules, causal caution, privacy constraints.

## What Is Not Ontology

These are useful, but they are not the ontology by themselves:

- A CSV table.
- A Lark Base table.
- A dashboard chart.
- A one-off SQL or Python analysis.
- A text summary that cannot be traced back to objects and evidence.

The ontology starts when the analysis becomes a structured operating model.

