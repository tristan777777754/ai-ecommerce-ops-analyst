# Weekly Ops Brief

Generated from `business_recommendations` on 2026-05-18.

## What the Marketplace Manager Should Do This Week

### 1. Launch a winback campaign for dormant high-value customers

Recommended action:

- `CreateCustomerWinbackCampaign`

Why:

- The `Dormant High Value` segment has 14,771 customers.
- Historical revenue from this segment is 4,605,388.98.
- This segment represents 29.26% of customer revenue.
- Average recency is 399.3 days.

Interpretation:

These customers used to be valuable but have not returned recently. The first commercial action should be a targeted reactivation campaign, not broad discounting.

### 2. Investigate or deprioritize risky sellers

Recommended actions:

- `DeprioritizeRiskySeller`
- `InvestigateSeller`

Top examples:

- Seller `1ca7077d890b907f89be8c954a02686a`: 115 orders, 13,341.57 revenue, 64.96% low-review rate, reliability score 55.5.
- Seller `54965bbe3e4f07ae045b90b0b8541f52`: 78 orders, 10,961.30 revenue, 30.23% late-delivery rate, 43.02% low-review rate.
- Seller `ad781527c93d00d89a11eecd9dcad7c1`: 44 orders, 6,899.57 revenue, 27.27% late-delivery rate, 40.91% low-review rate.

Interpretation:

These sellers have enough volume to matter and are associated with weak customer experience. The data does not prove they caused dissatisfaction, but they should be reviewed before routing more high-value demand through them.

### 3. Monitor delivery risk in specific states

Recommended action:

- `MonitorDeliveryRisk`

Top examples:

- `MA`: 747 orders, 152,523.02 revenue, 16.73% late-delivery rate.
- `AL`: 413 orders, 96,962.06 revenue, 20.58% late-delivery rate.
- `SE`: 350 orders, 75,246.25 revenue, 14.57% late-delivery rate.

Interpretation:

Delivery risk is geographically concentrated enough to monitor. The next investigation should compare seller origin, customer state, category mix, and delivery promise accuracy.

### 4. Investigate low-review product categories before promoting them

Recommended action:

- `InvestigateLowReviewProductCategory`

Top examples:

- `office_furniture`: 1,273 orders, 273,960.70 revenue, 26.02% low-review rate, average review 3.49.
- `fashion_male_clothing`: 112 orders, 10,797.82 revenue, 28.03% low-review rate.
- `fixed_telephony`: 217 orders, 59,583.00 revenue, 25.38% low-review rate.

Interpretation:

These categories may have product quality, fulfillment, expectation mismatch, or delivery issues. Do not promote them until the review risk is understood.

### 5. Promote high-revenue categories only when review risk is acceptable

Recommended action:

- `PromoteHighRevenueCategory`

Top examples:

- `health_beauty`: 1,258,681.34 revenue, 9.26% revenue share, 13.64% low-review rate.
- `sports_leisure`: 988,048.97 revenue, 7.27% revenue share, 14.51% low-review rate.
- `cool_stuff`: 635,290.85 revenue, 4.67% revenue share, 13.04% low-review rate.

Interpretation:

These categories are revenue-critical and currently stay below the review-risk threshold, so they are better candidates for promotion or protection than categories with high dissatisfaction.

## Recommendation Counts

| Action type | Priority | Count |
|---|---:|---:|
| CreateCustomerWinbackCampaign | High | 2 |
| SendReactivationOffer | High | 30 |
| DeprioritizeRiskySeller | High | 21 |
| InvestigateSeller | High/Medium | 9 |
| MonitorDeliveryRisk | High/Medium | 5 |
| InvestigateLowReviewProductCategory | High/Medium | 20 |
| PromoteHighRevenueCategory | High/Medium | 7 |

## How to Read This in Lark

Open the `business_recommendations` table and use these views:

- `High Priority Proposed`: best first screen for the demo.
- `Seller Action Triage`: seller investigation and deprioritization candidates.
- `Customer Winback`: customer and segment reactivation recommendations.
- `Review and Delivery Risk`: delivery states and low-review categories.

The important columns are:

- `action_type`: what the AI recommends.
- `target_type` and `target_id`: what object the action targets.
- `priority`: how urgent it is.
- `reason`: business explanation.
- `evidence_summary`: metric evidence.
- `status`: all first-version actions are `proposed`, meaning human approval is required.

