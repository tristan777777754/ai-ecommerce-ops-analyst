# AI Analyst Demo Q&A

Use this script to demo the AI E-commerce Ops Analyst after the ontology and `BusinessRecommendation` action layer are built.

## 1. What should I do this week?

Expected answer:

```text
This week I would focus on customer winback, seller risk, and review/delivery risk.

1. Create a winback campaign for the Dormant High Value segment.
   Evidence: 14,771 customers, 4,605,388.98 historical revenue, 29.26% revenue share, average recency 399.3 days.
   Action: CreateCustomerWinbackCampaign.
   Status: proposed.

2. Review the highest-risk sellers before routing more high-value orders through them.
   Example: seller 1ca7077d890b907f89be8c954a02686a has 115 orders, 13,341.57 revenue, 64.96% low-review rate, and reliability score 55.5.
   Action: DeprioritizeRiskySeller.
   Status: proposed.

3. Investigate product categories with elevated low-review rates before promoting them.
   Example: office_furniture has 1,273 orders, 273,960.70 revenue, 26.02% low-review rate, and average review score 3.49.
   Action: InvestigateLowReviewProductCategory.
   Status: proposed.

These are proposed actions for human review, not executed actions.
```

## 2. Which sellers should I investigate first?

Expected answer:

```text
Start with sellers that combine meaningful order volume, revenue impact, and poor customer experience signals.

1. Seller 1ca7077d890b907f89be8c954a02686a
   Evidence: 115 orders, 13,341.57 revenue, 64.96% low-review rate, 13.87% late-delivery rate, reliability score 55.5.
   Recommended action: DeprioritizeRiskySeller.

2. Seller 54965bbe3e4f07ae045b90b0b8541f52
   Evidence: 78 orders, 10,961.30 revenue, 30.23% late-delivery rate, 43.02% low-review rate, reliability score 61.7.
   Recommended action: DeprioritizeRiskySeller.

3. Seller ad781527c93d00d89a11eecd9dcad7c1
   Evidence: 44 orders, 6,899.57 revenue, 27.27% late-delivery rate, 40.91% low-review rate, reliability score 64.7.
   Recommended action: InvestigateSeller.

The data does not prove these sellers caused dissatisfaction, but they are associated with enough risk to justify review.
```

## 3. Which customers should I win back?

Expected answer:

```text
Use a two-level winback strategy.

First, create a campaign for the Dormant High Value segment:
- 14,771 customers.
- 4,605,388.98 historical revenue.
- 29.26% revenue share.
- Average recency: 399.3 days.

Then prioritize individual customers by monetary value and recency.
Top examples:
- Customer 0a0a92112bd4c708ca5fde585afaa872: 13,664.08 monetary value, 339 recency days.
- Customer da122df9eeddfedc1dc1f5349a1a690c: 7,571.63 monetary value, 520 recency days.
- Customer dc4802a71eae9be1dd28f5d788ceb526: 6,929.31 monetary value, 568 recency days.

Recommended actions: CreateCustomerWinbackCampaign and SendReactivationOffer.
Status: proposed.
```

## 4. Which categories should I promote?

Expected answer:

```text
Promote categories that are revenue-critical and stay below the review-risk threshold.

1. health_beauty
   Evidence: 1,258,681.34 revenue, 9.26% revenue share, 13.64% low-review rate.
   Action: PromoteHighRevenueCategory.

2. sports_leisure
   Evidence: 988,048.97 revenue, 7.27% revenue share, 14.51% low-review rate.
   Action: PromoteHighRevenueCategory.

3. cool_stuff
   Evidence: 635,290.85 revenue, 4.67% revenue share, 13.04% low-review rate.
   Action: PromoteHighRevenueCategory.

Do not blindly promote categories with high dissatisfaction. Those should go through review-risk investigation first.
```

## 5. Which categories should I investigate before promotion?

Expected answer:

```text
Investigate categories with enough volume and elevated low-review rates.

1. office_furniture
   Evidence: 1,273 orders, 273,960.70 revenue, 26.02% low-review rate, average review score 3.49.
   Action: InvestigateLowReviewProductCategory.

2. fashion_male_clothing
   Evidence: 112 orders, 10,797.82 revenue, 28.03% low-review rate.
   Action: InvestigateLowReviewProductCategory.

3. fixed_telephony
   Evidence: 217 orders, 59,583.00 revenue, 25.38% low-review rate.
   Action: InvestigateLowReviewProductCategory.

The issue may be product quality, fulfillment, expectation mismatch, or delivery. The current data supports investigation, not a causal claim.
```

## 6. Which regions have delivery risk?

Expected answer:

```text
The delivery-risk watchlist is concentrated in a few customer states.

1. MA
   Evidence: 747 orders, 152,523.02 revenue, 16.73% late-delivery rate.
   Action: MonitorDeliveryRisk.

2. AL
   Evidence: 413 orders, 96,962.06 revenue, 20.58% late-delivery rate.
   Action: MonitorDeliveryRisk.

3. SE
   Evidence: 350 orders, 75,246.25 revenue, 14.57% late-delivery rate.
   Action: MonitorDeliveryRisk.

The next step is to compare seller origin, category mix, and delivery promise accuracy before changing delivery commitments.
```

## 7. Why did you recommend this seller?

Example user question:

```text
Why did you recommend seller 1ca7077d890b907f89be8c954a02686a?
```

Expected answer:

```text
I recommended seller 1ca7077d890b907f89be8c954a02686a because it meets the seller risk trigger.

Evidence:
- Orders: 115
- Revenue: 13,341.57
- Low-review rate: 64.96%
- Late-delivery rate: 13.87%
- Seller reliability score: 55.5

Recommended action: DeprioritizeRiskySeller.
Status: proposed.

The data does not prove the seller caused the dissatisfaction, but the seller is associated with enough negative customer experience to justify review before routing additional high-value demand through it.
```

## 8. Can you execute these actions?

Expected answer:

```text
No. In the first version, I can only propose actions.

All BusinessRecommendation records are status=proposed and require human approval. I cannot send coupons, suspend sellers, change delivery promises, alter listings, or spend ad budget.

I can help explain, prioritize, or draft approval notes for a human operator.
```

