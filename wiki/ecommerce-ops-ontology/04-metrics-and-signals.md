# Metrics and Signals

## Metric Design Principle

Metrics are object state. They are not only chart values.

Each metric should answer:

- Which object owns this metric?
- How is it calculated?
- What business state does it represent?
- Which action can it trigger?
- What evidence should be shown to the operator?

## Executive Signals

| Metric | Owner | Meaning |
|---|---|---|
| Total revenue | Marketplace summary | Size of business represented in the dataset |
| Total orders | Marketplace summary | Demand volume |
| Average order value | Marketplace summary, Customer, Order | Customer value and order economics |
| Late delivery rate | Marketplace summary, Seller, Geography, Order | Fulfillment reliability |
| Low review rate | Marketplace summary, Seller, ProductCategory, Review | Customer dissatisfaction |
| Revenue Pareto band | ProductCategory, Seller | Concentration of business value |

## Customer Signals

| Signal | Object | Evidence table | Operational meaning |
|---|---|---|---|
| Recency days | Customer | `customer_rfm` | How long since last purchase |
| Frequency | Customer | `customer_rfm` | Repeat purchase behavior |
| Monetary value | Customer | `customer_rfm` | Historical customer value |
| RFM segment | Customer, CustomerSegment | `customer_rfm`, `rfm_segment_summary` | Retention or growth state |
| Dormant high value flag | Customer, RetentionOpportunity | `dormant_high_value` | Candidate for winback |

Suggested thresholds:

- Dormant high value customer: `rfm_segment = "Dormant High Value"`.
- High priority winback: `monetary_value >= 300` and `recency_days >= 180`.
- Segment campaign candidate: segment has at least 100 customers and meaningful revenue share.

## Seller Signals

| Signal | Object | Evidence table | Operational meaning |
|---|---|---|---|
| Orders | Seller | `seller_performance` | Volume threshold for reliable judgment |
| Revenue | Seller | `seller_performance` | Business impact |
| Late delivery rate | Seller, SellerRisk | `seller_performance`, `seller_risk_watchlist` | Fulfillment risk |
| Low review rate | Seller, SellerRisk | `seller_performance`, `seller_risk_watchlist` | Customer dissatisfaction risk |
| Seller reliability score | Seller, SellerRisk | `seller_risk_watchlist` | Composite seller operating state |
| Risk band | SellerRisk | `seller_risk_watchlist` | Triage category |

Suggested thresholds:

- Investigate seller: `orders >= 30` and at least one of:
  - `late_delivery_rate >= 0.15`
  - `low_review_rate >= 0.18`
  - `seller_reliability_score <= 75`
- Deprioritize risky seller: stricter threshold, such as `orders >= 50` and severe reliability issue.

## Product and Category Signals

| Signal | Object | Evidence table | Operational meaning |
|---|---|---|---|
| Revenue | Product, ProductCategory | `category_performance`, `product_performance_top` | Demand concentration |
| Revenue share | ProductCategory | `category_performance` | Category importance |
| Cumulative share | ProductCategory | `category_performance` | Pareto contribution |
| Pareto band | ProductCategory, ProductOpportunity | `category_performance`, `category_opportunity` | Promote or protect high-value categories |
| Low review rate | ProductCategory, ReviewRisk | `review_risk_by_category` | Dissatisfaction concentration |
| Average review score | ProductCategory, ReviewRisk | `review_risk_by_category` | Customer experience signal |

Suggested thresholds:

- Review risk category: `orders >= 100` and `low_review_rate >= 0.15`.
- High priority review investigation: `revenue >= 100000` and `low_review_rate >= 0.20`.
- Promote high revenue category: `pareto_band = "top_80_percent_revenue"` and low review risk.

## Delivery Signals

| Signal | Object | Evidence table | Operational meaning |
|---|---|---|---|
| Delivery delay days | Order | `order_facts` | Difference between delivered and estimated delivery date |
| Late delivery flag | Order | `order_facts` | Whether order missed the expected delivery date |
| Late delivery rate | Geography, DeliveryRisk, Seller | `delivery_risk_by_state`, `seller_performance` | Concentrated logistics risk |
| Average delay days | Geography, DeliveryRisk | `delivery_risk_by_state` | Severity of late delivery |

Suggested thresholds:

- Monitor delivery risk: `orders >= 100` and `late_delivery_rate >= 0.12`.
- High priority delivery risk: `orders >= 500` and `late_delivery_rate >= 0.15`.

## Signal to Action Mapping

| Signal pattern | Candidate action | Target object |
|---|---|---|
| Dormant high value customer | `SendReactivationOffer` | Customer |
| Dormant or at-risk customer segment | `CreateCustomerWinbackCampaign` | CustomerSegment |
| Seller with high low-review rate or late-delivery rate | `InvestigateSeller` | Seller |
| Severe seller risk with meaningful volume | `DeprioritizeRiskySeller` | Seller |
| State with elevated late delivery | `MonitorDeliveryRisk` | Geography |
| Delivery cluster with severe delay | `FixDeliveryProcess` | DeliveryRisk |
| Category with elevated low reviews | `InvestigateLowReviewProductCategory` | ProductCategory |
| Top Pareto category with acceptable risk | `PromoteHighRevenueCategory` | ProductCategory |

## Evidence Standard

Every metric-backed recommendation must include:

- Target object type and ID.
- At least two supporting metrics.
- Trigger condition.
- Source table or view.
- Cautious language if cause is not proven.

Example:

```yaml
target_type: Seller
target_id: seller_id_here
action_type: InvestigateSeller
trigger: orders >= 30 and low_review_rate >= 0.18
evidence:
  orders: 123
  revenue: 12345.67
  low_review_rate: 0.25
  late_delivery_rate: 0.12
source_view: seller_risk_watchlist
```

