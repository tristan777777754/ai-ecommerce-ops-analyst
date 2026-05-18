# Demo Operating Workflow

## Demo Purpose

The demo should show that this project is not a Kaggle-style analysis notebook and not just a dashboard.

It is an AI-operated e-commerce ontology workflow:

```text
Raw data
  -> Lark analysis layer
  -> ontology objects and links
  -> object state and risk signals
  -> governed recommendations
  -> human-approved action workflow
```

## Five-Minute Demo Script

### 1. Set the Business Context

Say:

```text
This project simulates a Forward Deployed Engineer engagement for an e-commerce marketplace.
The goal is to turn raw marketplace data into an AI-native operating model that tells the manager who is buying, what is selling, what is going wrong, and what action to take next.
```

Show:

- Raw Olist dataset.
- Lark Base raw data.
- Lark Base analysis layer.

### 2. Show the Evidence Layer

Open the analysis dashboard and show:

- Total revenue.
- Total orders.
- Monthly revenue trend.
- RFM segment revenue.
- Seller risk bands.
- Delivery risk by state.
- Review risk by category.

Say:

```text
This is the analysis checkpoint. It is useful, but it is still not the ontology. It becomes ontology when these tables become business objects, relationships, states, and governed actions.
```

### 3. Introduce the Ontology

Show this wiki and the object model:

- Customer.
- Order.
- ProductCategory.
- Seller.
- DeliveryRisk.
- ReviewRisk.
- BusinessRecommendation.

Say:

```text
The ontology models the business world. A seller is not just a row in a table. It is an operating object with revenue, late delivery rate, low review rate, reliability score, linked orders, linked reviews, and approved action types.
```

### 4. Ask the Operating Question

Ask the AI analyst:

```text
What should the marketplace manager do this week, and why?
```

Expected answer:

- Investigate highest-risk sellers.
- Win back dormant high-value customers.
- Monitor high-risk delivery states.
- Investigate categories with elevated low reviews.
- Promote high-revenue categories only when review risk is acceptable.

Each answer should include:

- Target object.
- Action type.
- Priority.
- Evidence.
- Status.

### 5. Drill Into One Seller

Ask:

```text
Why did you recommend investigating this seller?
```

Expected answer:

- Orders.
- Revenue.
- Low review rate.
- Late delivery rate.
- Reliability score.
- Trigger rule.
- Causal caution.

Good phrasing:

```text
This seller meets the InvestigateSeller trigger because it has meaningful order volume and elevated customer dissatisfaction. The data does not prove the seller caused the dissatisfaction, but it is strong enough to justify an operational investigation.
```

### 6. Drill Into One Customer Segment

Ask:

```text
Which customers should receive winback priority?
```

Expected answer:

- Segment summary first.
- Dormant high value signal.
- Top customer targets only if needed.
- Evidence: monetary value, recency, RFM segment.

### 7. Show Governance

Show:

- `ontology/actions.yml`.
- `BusinessRecommendation` contract.
- Evals and governance page.

Say:

```text
The AI does not execute real operations automatically. It creates proposed recommendations with evidence. Human approval is required before any business action.
```

### 8. Close the Demo

Say:

```text
The important shift is from reporting to operating. The system does not only show what happened. It defines business objects, tracks their state, explains risks, proposes approved actions, and keeps the workflow testable and auditable.
```

## Demo Readiness Checklist

- Lark Base raw data exists.
- Lark Base analysis layer exists.
- Dashboard exists.
- Ontology wiki exists.
- Object model is documented.
- Links are documented.
- Action types are documented.
- Recommendation contract is documented.
- Evals and governance are documented.
- The AI analyst can answer the weekly operating question with evidence.

## Current Build Status

After this wiki, the first `BusinessRecommendation` table was generated from the analysis layer.

The table includes:

- Seller investigation recommendations.
- Customer winback recommendations.
- Delivery monitoring recommendations.
- Review risk investigation recommendations.
- Category opportunity recommendations.

The table uses the contract in [Logic and Actions](05-logic-and-actions.md).

Local outputs:

- `outputs/business_recommendations/business_recommendations.csv`
- `outputs/business_recommendations/BUSINESS_RECOMMENDATIONS.md`

Lark Base:

- table: `business_recommendations`
- table id: `tblkxo9xl31Rfmc8`
- records: `94`
- status: all first-version recommendations are `proposed`

The next build step is to make the AI analyst answer directly from these `BusinessRecommendation` records and explain each recommendation with evidence.
