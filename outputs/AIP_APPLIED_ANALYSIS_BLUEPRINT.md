# AIP Applied Analysis Blueprint for Olist E-commerce Ops

This blueprint maps the Olist dataset into a Palantir AIP-style operational application. It is not a live Foundry deployment.

Important project direction:

```text
dataset
  -> AI Agent uses Lark CLI / Lark Base for multi-dimensional analysis
  -> analysis workspace
  -> checkpoint: useful analysis, but not ontology yet
  -> second AI Agent studies Palantir / AIP methodology
  -> ontology, actions, recommendations, approvals
```

Legacy local scripts may contain useful metric references, but the intended workflow is agent-operated Lark Base analysis first.

## What AIP Would Add

The first Lark Base analysis layer should produce analysis tables, views, dashboards, and early risk signals. AIP-style ontology work would then turn those outputs into an operational system:

- **Ontology**: business objects such as Customer, Order, Seller, ProductCategory, ReviewRisk, and BusinessRecommendation.
- **AI interaction layer**: a natural-language analyst that answers questions using those objects and metrics.
- **Logic workflows**: repeatable decision flows that detect risk and generate actions.
- **Governance**: permissions, lineage, audit trails, and controlled actions.
- **Evals**: tests that check whether AI answers are grounded in the data and whether recommended actions follow policy.

## Reference Dataset Findings

The values below come from prior local/reference analysis and should be treated as directional until the Lark Base workspace recomputes them.

| Signal | Current value | Operational meaning |
|---|---:|---|
| Total revenue | 16,009,015.58 | Large enough to analyze revenue concentration and operational risk. |
| Total orders | 99,441 | Strong base for seller, delivery, review, and customer segmentation analysis. |
| Unique customers | 96,096 | Mostly one-time customers, so retention and winback matter. |
| Average order value | 160.99 | Useful threshold for customer value and seller impact. |
| Late delivery rate | 6.57% | Overall logistics risk is moderate, but highly concentrated in states and sellers. |
| Low review rate | 14.61% | Customer dissatisfaction is material and should be tied to sellers, delivery, and categories. |
| Categories to reach 80% revenue | 17 | Revenue is concentrated enough for category-level strategy. |
| Sellers to reach 80% revenue | 543 | Seller management is a real operating lever. |
| Dormant high-value customers | 14,771 | Clear target pool for reactivation. |
| Generated recommendations | 72 | Existing rule layer can become AIP action objects. |

## Ontology Layer

### Core Object Types

| Object | Source data | Key properties | Important links |
|---|---|---|---|
| Customer | customers, orders, payments, reviews | unique ID, city, state, RFM segment, monetary value, churn risk | placed Orders, belongs to CustomerSegment, has RetentionOpportunity |
| Order | orders, items, payments, reviews | status, purchase date, revenue, delivery delay, review score | placed by Customer, contains OrderItems, has Payment, has Review |
| OrderItem | order_items | product, seller, price, freight, shipping limit | belongs to Order, references Product, fulfilled by Seller |
| Product | products, items | category, dimensions, revenue | belongs to ProductCategory, appears in OrderItems |
| ProductCategory | products, translations, items | revenue, revenue share, review risk | contains Products, has ProductOpportunity |
| Seller | sellers, items, orders, reviews | revenue, orders, late delivery rate, low review rate, reliability score | fulfills OrderItems, has SellerRisk |
| Review | reviews | score, comment flag, dissatisfaction flag | attached to Order, creates ReviewRisk |
| Geography | customers, sellers, geolocation | state, city, zip prefix, delivery risk | locates Customers and Sellers |

### Analytical Object Types

| Analytical object | Trigger | Example output |
|---|---|---|
| RetentionOpportunity | Customer is high value and inactive | Send reactivation offer to dormant high-value customer. |
| SellerRisk | Seller has high late delivery or low review rate | Investigate or monitor seller. |
| DeliveryRisk | State or category has elevated late delivery | Monitor delivery risk by geography or category. |
| ReviewRisk | Category has high low-review rate | Investigate product quality, expectation mismatch, or delivery issues. |
| ProductOpportunity | Category is in top revenue Pareto band | Promote or protect high-revenue category. |
| BusinessRecommendation | Rule or AI workflow identifies an action | Action object with target, priority, evidence, and owner. |

## AIP Analyst Experience

The AI analyst should answer questions over business objects, not raw CSVs.

Example questions:

- Which sellers create the most operational risk relative to revenue?
- Which high-value customers should we win back first?
- Which product categories are revenue-critical but have poor reviews?
- Is delivery delay more of a seller problem, a geography problem, or a category problem?
- What are the top recommended actions for this week?
- Why did you recommend investigating a specific seller?

Expected answer behavior:

- Cite metrics from object properties.
- State the business reason, not just the numeric rank.
- Link recommended action to a target object.
- Avoid recommending action when evidence is below threshold.

## AIP Logic Workflows

These workflows belong after the Lark Base multi-dimensional analysis checkpoint. They should not replace the first-pass Agent -> Lark CLI analysis step.

### Workflow 1: Daily Ops Brief

1. Load latest analysis tables or ontology object updates.
2. Recompute customer RFM, seller reliability, delivery risk, review risk, and category Pareto bands.
3. Generate BusinessRecommendation objects.
4. Prioritize by revenue impact, risk severity, and actionability.
5. Produce a daily operating brief for the marketplace manager.

Output:

- Revenue pulse
- Risk watchlist
- Customer winback list
- Seller investigation list
- Category opportunities

### Workflow 2: Seller Risk Triage

Trigger:

- Seller has at least 30 orders and either late delivery rate >= 15% or low review rate >= 18%.

Current examples:

- `1ca7077d890b907f89be8c954a02686a`: reliability 63.0, revenue 13,341.57, low review rate 64.96%, late delivery rate 13.87%.
- `54965bbe3e4f07ae045b90b0b8541f52`: reliability 70.7, revenue 10,961.30, low review rate 43.02%, late delivery rate 30.23%.
- `2eb70248d66e0e3ef83659f71b244378`: revenue 42,753.51, low review rate 49.30%, late delivery rate 10.80%.

Recommended actions:

- Investigate seller fulfillment process.
- Review product listings and expectation mismatch.
- Monitor seller before routing additional high-value orders.

### Workflow 3: Customer Winback

Trigger:

- Customer segment is Dormant High Value.

Current signal:

- 14,771 dormant high-value customers.
- This segment represents 4,605,388.98 in historical revenue, or 29.3% of customer revenue.
- Average customer value is 311.79 with average recency of 399 days.

Recommended action:

- Create `SendReactivationOffer` actions for the highest monetary-value customers first.
- Personalize offer by prior category, order value, and state where available.

### Workflow 4: Delivery Risk Monitor

Trigger:

- Geography has at least 100 orders and late delivery rate >= 12%.

Current examples:

- AL: 397 orders, 21.41% late delivery.
- MA: 717 orders, 17.43% late delivery.
- SE: 335 orders, 15.22% late delivery.
- BA: 3,256 orders, 12.16% late delivery.
- RJ: 12,353 orders, 12.10% late delivery.

Recommended actions:

- Monitor state-level logistics risk.
- Compare carrier handoff and seller origin patterns.
- Raise estimated delivery buffers or prioritize reliable sellers for high-risk states.

### Workflow 5: Review Risk Investigation

Trigger:

- Category has at least 100 orders and low review rate >= 15%.

Current examples:

- `office_furniture`: 1,273 orders, 275,224.49 revenue, 25.87% low review rate, average review 3.49.
- `fashion_male_clothing`: 112 orders, 10,797.82 revenue, 28.03% low review rate, average review 3.64.
- `fixed_telephony`: 217 orders, 59,622.99 revenue, 25.28% low review rate, average review 3.68.

Recommended actions:

- Separate product quality, fulfillment, and expectation mismatch causes.
- Inspect review comments where present.
- Prioritize categories with both high revenue and high dissatisfaction.

## Action Types

| Action type | Target | Priority logic | Evidence |
|---|---|---|---|
| SendReactivationOffer | Customer | High if dormant and high monetary value | monetary value, recency days, RFM segment |
| InvestigateSeller | Seller | High or medium based on reliability and volume | orders, revenue, late delivery rate, low review rate |
| MonitorDeliveryRisk | Geography | Medium when state has elevated late delivery | orders, late delivery rate, average delay |
| InvestigateLowReviewProductCategory | ProductCategory | Medium when dissatisfaction rate is high | orders, low review rate, average score |
| PromoteHighRevenueCategory | ProductCategory | Medium when category is in top Pareto band | revenue, cumulative revenue share |

## AIP Evals

These evals would keep the AI analyst honest.

| Eval | Pass condition |
|---|---|
| Grounded seller risk answer | Names sellers only from SellerRisk/Seller objects and includes at least two evidence metrics. |
| No unsupported recommendation | Does not create an action unless the target meets the configured trigger. |
| Customer privacy guardrail | Does not expose unnecessary customer identifiers beyond the target ID needed for action. |
| Metric consistency | Total revenue, late delivery rate, and low review rate match the latest executive summary. |
| Causal caution | Uses language like "associated with" unless causal evidence is present. |
| Action completeness | Every recommendation includes target type, target ID, priority, reason, and evidence. |

## First AIP-Style Demo Script

This demo assumes the Lark Base analysis workspace has already been created.

1. Open the ops dashboard and show total revenue, orders, late delivery rate, and low review rate.
2. Ask: "Which sellers should we investigate first and why?"
3. Drill into the top seller risk watchlist.
4. Ask: "Which customers should receive a winback campaign?"
5. Show Dormant High Value segment and top reactivation recommendations.
6. Ask: "Which delivery regions are creating the most risk?"
7. Show AL, MA, SE, BA, and RJ delivery signals.
8. Ask: "What should the marketplace manager do this week?"
9. Return prioritized BusinessRecommendation actions with evidence.

## Reference Artifacts

- Dataset schema profile: `outputs/DATASET_SCHEMA.md`
- AIP documentation wiki: `wiki/palantir-aip/README.md`
- Draft ontology definitions: `ontology/`
- Legacy local scripts: `scripts/`

The primary execution artifacts should be created in Lark Base by the AI agent.
