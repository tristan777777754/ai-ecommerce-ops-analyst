# Logic and Actions

## Logic Design Principle

AIP Logic turns ontology state into repeatable workflows.

For this project, a Logic function is represented as a documented workflow that:

1. Accepts objects or text input.
2. Queries the relevant evidence tables or object views.
3. Calculates or verifies metrics.
4. Applies threshold logic.
5. Uses an LLM only where interpretation or prioritization is needed.
6. Creates proposed `BusinessRecommendation` records.
7. Leaves execution under human approval.

## First Logic Functions

### Daily Ops Brief

Purpose:

Generate the top operating actions for the marketplace manager.

Inputs:

- `executive_summary`
- `seller_risk_watchlist`
- `dormant_high_value`
- `delivery_risk_by_state`
- `review_risk_by_category`
- `category_opportunity`

Steps:

1. Load executive metrics.
2. Pull top seller, customer, delivery, review, and category signals.
3. Filter each candidate against action trigger rules.
4. Rank by priority, revenue impact, risk severity, and actionability.
5. Return a short operating brief.
6. Create proposed `BusinessRecommendation` records if the operator asks for action records.

Output:

- Revenue pulse.
- Top risks.
- Top opportunities.
- Recommended actions with evidence.

### Seller Risk Triage

Purpose:

Identify sellers that need investigation or monitoring.

Inputs:

- Seller object or `seller_risk_watchlist`.

Trigger:

```text
orders >= 30
and one of:
  late_delivery_rate >= 0.15
  low_review_rate >= 0.18
  seller_reliability_score <= 75
```

Allowed actions:

- `InvestigateSeller`
- `DeprioritizeRiskySeller`, only for severe cases.

Required evidence:

- `seller_id`
- `orders`
- `revenue`
- `late_delivery_rate`
- `low_review_rate`
- `seller_reliability_score`

### Customer Winback

Purpose:

Identify customers or segments worth a retention action.

Inputs:

- Customer object, `customer_rfm`, `dormant_high_value`, `rfm_segment_summary`.

Trigger:

```text
rfm_segment == "Dormant High Value"
and monetary_value is present
and recency_days is present
```

Allowed actions:

- `SendReactivationOffer`
- `CreateCustomerWinbackCampaign`

Required evidence:

- `customer_unique_id` or segment name.
- `monetary_value`.
- `recency_days`.
- `rfm_segment`.
- Segment-level customers, revenue, and revenue share when campaign-level.

### Delivery Risk Monitor

Purpose:

Identify geographic delivery risk that should be monitored.

Inputs:

- `delivery_risk_by_state`.

Trigger:

```text
orders >= 100
and late_delivery_rate >= 0.12
```

Allowed actions:

- `MonitorDeliveryRisk`
- `FixDeliveryProcess`, only when severity is higher and evidence supports process review.

Required evidence:

- `state` or risk target ID.
- `orders`.
- `late_delivery_rate`.
- `avg_delay_days`.

### Review Risk Investigation

Purpose:

Identify categories where customer dissatisfaction deserves investigation.

Inputs:

- `review_risk_by_category`.

Trigger:

```text
orders >= 100
and low_review_rate >= 0.15
```

Allowed action:

- `InvestigateLowReviewProductCategory`

Required evidence:

- `category_name`.
- `orders`.
- `revenue`.
- `low_review_rate`.
- `avg_review_score`.

### Category Opportunity

Purpose:

Identify categories to promote, protect, or monitor.

Inputs:

- `category_performance`
- `category_opportunity`

Trigger:

```text
pareto_band == "top_80_percent_revenue"
and revenue_share is present
```

Allowed action:

- `PromoteHighRevenueCategory`

Guardrail:

If review risk is high, the recommendation must say "investigate before promotion" or choose the review investigation action instead.

## Action Model

All first-version actions are proposed actions. They do not execute real-world changes.

| Action | Target | First-version behavior |
|---|---|---|
| SendReactivationOffer | Customer | Propose winback target, no coupon sent |
| CreateCustomerWinbackCampaign | CustomerSegment | Propose campaign brief, no campaign launched |
| InvestigateSeller | Seller | Propose investigation, no penalty applied |
| DeprioritizeRiskySeller | Seller | Propose risk review, no routing change applied |
| MonitorDeliveryRisk | Geography | Propose monitoring, no delivery promise changed |
| FixDeliveryProcess | DeliveryRisk | Propose process investigation, no provider changed |
| InvestigateLowReviewProductCategory | ProductCategory | Propose investigation, no listing changed |
| PromoteHighRevenueCategory | ProductCategory | Propose growth opportunity, no budget changed |
| PrioritizeHighValueCustomer | Customer | Propose support priority, no operational SLA changed |

## BusinessRecommendation Contract

Every action should be represented as:

```yaml
recommendation_id: REC-0001
action_type: InvestigateSeller
target_type: Seller
target_id: seller_id_here
priority: High
trigger: orders >= 30 and low_review_rate >= 0.18
reason: Seller has meaningful order volume and elevated customer dissatisfaction.
evidence:
  orders: 123
  revenue: 12345.67
  low_review_rate: 0.25
  late_delivery_rate: 0.12
status: proposed
created_at: YYYY-MM-DD
source_view: seller_risk_watchlist
```

Allowed statuses:

- `proposed`
- `approved`
- `rejected`
- `executed`
- `expired`

## Human Approval Rule

The first version requires human approval for every action.

The AI analyst may:

- Recommend.
- Explain.
- Rank.
- Draft action records.
- Ask for approval.

The AI analyst may not:

- Send real coupons.
- Suspend or deprioritize sellers automatically.
- Change delivery promises.
- Modify listings.
- Spend ad budget.
- Claim root cause without evidence.

