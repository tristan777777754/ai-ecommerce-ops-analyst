# BusinessRecommendation Records

Generated from the Olist analysis layer and the e-commerce ontology action rules.

## Summary

- Total recommendations: 94
- Generated at: 2026-06-02
- Status: all records are `proposed` and require human approval before execution.

## Counts by Action and Priority

| Action type | Priority | Count |
|---|---:|---:|
| CreateCustomerWinbackCampaign | High | 2 |
| DeprioritizeRiskySeller | High | 21 |
| InvestigateLowReviewProductCategory | High | 2 |
| InvestigateLowReviewProductCategory | Medium | 18 |
| InvestigateSeller | High | 7 |
| InvestigateSeller | Medium | 2 |
| MonitorDeliveryRisk | High | 1 |
| MonitorDeliveryRisk | Medium | 4 |
| PromoteHighRevenueCategory | High | 2 |
| PromoteHighRevenueCategory | Medium | 5 |
| SendReactivationOffer | High | 30 |

## Top Recommendations

- `REC-0001` `CreateCustomerWinbackCampaign` -> `CustomerSegment:Dormant High Value` [High]: Customer segment has enough dormant or at-risk value to justify a winback campaign proposal. Evidence: customers=14771; revenue=4,605,388.98; revenue_share=29.26%; avg_recency_days=399.3
- `REC-0002` `CreateCustomerWinbackCampaign` -> `CustomerSegment:At Risk` [High]: Customer segment has enough dormant or at-risk value to justify a winback campaign proposal. Evidence: customers=13781; revenue=1,009,412.34; revenue_share=6.41%; avg_recency_days=400.8
- `REC-0003` `SendReactivationOffer` -> `Customer:0a0a92112bd4c708ca5fde585afaa872` [High]: High historical value and long inactivity signal a winback opportunity. Evidence: monetary_value=13,664.08; recency_days=339; rfm_segment=Dormant High Value
- `REC-0004` `SendReactivationOffer` -> `Customer:da122df9eeddfedc1dc1f5349a1a690c` [High]: High historical value and long inactivity signal a winback opportunity. Evidence: monetary_value=7,571.63; recency_days=520; rfm_segment=Dormant High Value
- `REC-0005` `SendReactivationOffer` -> `Customer:dc4802a71eae9be1dd28f5d788ceb526` [High]: High historical value and long inactivity signal a winback opportunity. Evidence: monetary_value=6,929.31; recency_days=568; rfm_segment=Dormant High Value
- `REC-0006` `SendReactivationOffer` -> `Customer:ff4159b92c40ebe40454e3e6a7c35ed6` [High]: High historical value and long inactivity signal a winback opportunity. Evidence: monetary_value=6,726.66; recency_days=467; rfm_segment=Dormant High Value
- `REC-0007` `SendReactivationOffer` -> `Customer:4007669dec559734d6f53e029e360987` [High]: High historical value and long inactivity signal a winback opportunity. Evidence: monetary_value=6,081.54; recency_days=283; rfm_segment=Dormant High Value
- `REC-0008` `SendReactivationOffer` -> `Customer:eebb5dda148d3893cdaf5b5ca3040ccb` [High]: High historical value and long inactivity signal a winback opportunity. Evidence: monetary_value=4,764.34; recency_days=503; rfm_segment=Dormant High Value
- `REC-0009` `SendReactivationOffer` -> `Customer:edf81e1f3070b9dac83ec83dacdbb9bc` [High]: High historical value and long inactivity signal a winback opportunity. Evidence: monetary_value=4,194.76; recency_days=503; rfm_segment=Dormant High Value
- `REC-0010` `SendReactivationOffer` -> `Customer:5e713be0853d8986528d7869a0811d2b` [High]: High historical value and long inactivity signal a winback opportunity. Evidence: monetary_value=4,042.74; recency_days=576; rfm_segment=Dormant High Value
- `REC-0011` `SendReactivationOffer` -> `Customer:011875f0176909c5cf0b14a9138bb691` [High]: High historical value and long inactivity signal a winback opportunity. Evidence: monetary_value=4,016.91; recency_days=534; rfm_segment=Dormant High Value
- `REC-0012` `SendReactivationOffer` -> `Customer:5d09b0d82126457e2a8ebfb9c9a1ffc4` [High]: High historical value and long inactivity signal a winback opportunity. Evidence: monetary_value=3,736.22; recency_days=570; rfm_segment=Dormant High Value
- `REC-0013` `SendReactivationOffer` -> `Customer:931eabdf0636b8fd60369a8d759917d6` [High]: High historical value and long inactivity signal a winback opportunity. Evidence: monetary_value=3,666.42; recency_days=481; rfm_segment=Dormant High Value
- `REC-0014` `SendReactivationOffer` -> `Customer:03796b63235e0e0a299084988c662c7e` [High]: High historical value and long inactivity signal a winback opportunity. Evidence: monetary_value=3,602.47; recency_days=559; rfm_segment=Dormant High Value
- `REC-0015` `SendReactivationOffer` -> `Customer:59d66d72939bc9497e19d89c61a96d5f` [High]: High historical value and long inactivity signal a winback opportunity. Evidence: monetary_value=3,559.99; recency_days=389; rfm_segment=Dormant High Value
- `REC-0016` `SendReactivationOffer` -> `Customer:6f00d356a4be20527662aaf12116baab` [High]: High historical value and long inactivity signal a winback opportunity. Evidence: monetary_value=3,184.55; recency_days=287; rfm_segment=Dormant High Value
- `REC-0017` `SendReactivationOffer` -> `Customer:895617ab63a9ad8881d9470f7427cd25` [High]: High historical value and long inactivity signal a winback opportunity. Evidence: monetary_value=3,126.50; recency_days=333; rfm_segment=Dormant High Value
- `REC-0018` `SendReactivationOffer` -> `Customer:c6111f70f40b3420e387493c627c27fa` [High]: High historical value and long inactivity signal a winback opportunity. Evidence: monetary_value=3,126.50; recency_days=328; rfm_segment=Dormant High Value
- `REC-0019` `SendReactivationOffer` -> `Customer:58c1b085b54c03a1f1ab5f13d64c2b1c` [High]: High historical value and long inactivity signal a winback opportunity. Evidence: monetary_value=3,064.72; recency_days=352; rfm_segment=Dormant High Value
- `REC-0020` `SendReactivationOffer` -> `Customer:ff0ae98646e7bbb41cf0f0d3991fef98` [High]: High historical value and long inactivity signal a winback opportunity. Evidence: monetary_value=3,048.27; recency_days=455; rfm_segment=Dormant High Value

## Files

- CSV: `outputs/business_recommendations/business_recommendations.csv`
- Lark batch JSON: `outputs/business_recommendations/business_recommendations_lark_batch.json`
