# Business Objects

## Object Design Principle

Objects should match the way a marketplace operator thinks:

- Who bought?
- What did they buy?
- Who fulfilled it?
- Did it arrive on time?
- Was the customer satisfied?
- Which part of the business needs action?

The raw Olist tables are the source data. The Lark analysis layer supplies calculated state. The ontology turns both into business objects.

## Core Objects

| Object | Meaning | Primary evidence | Why it matters |
|---|---|---|---|
| Customer | A marketplace buyer, grouped by `customer_unique_id` where possible | `raw_customers`, `customer_rfm`, `dormant_high_value` | Retention, winback, value segmentation |
| Order | A purchase event with lifecycle, payment, delivery, and review state | `raw_orders`, `order_facts` | Unit of demand, fulfillment, and customer experience |
| OrderItem | A line item linking product, seller, price, and freight | `raw_order_items`, `order_facts` | Connects revenue to sellers and products |
| Product | A catalog item sold through the marketplace | `raw_products`, `product_performance_top` | Product-level sales and quality signal |
| ProductCategory | A translated product category | `category_performance`, `category_opportunity` | Revenue concentration and category strategy |
| Seller | A seller fulfilling one or more order items | `seller_performance`, `seller_risk_watchlist` | Marketplace reliability and operational risk |
| Payment | Payment facts attached to an order | `raw_order_payments`, `order_facts` | Revenue, AOV, payment behavior |
| Review | Customer feedback attached to an order | `raw_order_reviews`, `review_risk_by_category` | Satisfaction, dissatisfaction, product or fulfillment signal |
| Geography | State, city, or zip-prefix location | `raw_geolocation`, `delivery_risk_by_state` | Delivery risk and regional operating patterns |

## Analytical Objects

Analytical objects are what make the project feel like an operating system instead of a reporting layer.

| Object | Created from | Operational role |
|---|---|---|
| CustomerSegment | `customer_rfm`, `rfm_segment_summary` | Groups customers into value and retention states |
| RetentionOpportunity | `dormant_high_value` | Identifies customers or segments worth winback action |
| SellerRisk | `seller_risk_watchlist` | Captures seller reliability problems and triage priority |
| DeliveryRisk | `delivery_risk_by_state` | Captures geographic delivery delay patterns |
| ReviewRisk | `review_risk_by_category` | Captures dissatisfaction concentration by category |
| ProductOpportunity | `category_opportunity`, `category_performance` | Captures categories to promote, protect, or investigate |
| BusinessRecommendation | Derived from action logic | The action proposal object shown to the operator |

## Object State

Each object should have enough state for the AI analyst to answer and recommend without returning to raw CSV logic every time.

### Customer

Required properties:

- `customer_unique_id`
- `customer_state`
- `first_purchase_date`
- `last_purchase_date`
- `frequency`
- `monetary_value`
- `avg_order_value`
- `recency_days`
- `rfm_segment`
- `churn_risk_score`

Operator questions:

- Which high-value customers are dormant?
- Which customers should be prioritized for winback?
- Which segment contributes the most revenue?

### Seller

Required properties:

- `seller_id`
- `seller_state`
- `orders`
- `items`
- `revenue`
- `avg_review_score`
- `low_review_rate`
- `late_delivery_rate`
- `avg_delivery_delay_days`
- `seller_reliability_score`
- `risk_band`

Operator questions:

- Which sellers create the most operational risk?
- Which sellers have meaningful revenue but poor customer experience?
- Which seller should be investigated first?

### ProductCategory

Required properties:

- `category_name`
- `revenue`
- `revenue_share`
- `cumulative_share`
- `pareto_band`
- `orders`
- `products`
- `low_review_rate`
- `avg_review_score`

Operator questions:

- Which categories drive most revenue?
- Which categories have both high revenue and poor reviews?
- Which categories should be promoted or investigated?

### Geography

Required properties:

- `state`
- `orders`
- `late_delivery_rate`
- `avg_delay_days`
- `risk_band`

Operator questions:

- Which states have elevated delivery risk?
- Is delivery risk concentrated enough to monitor?
- Which regions need operational review?

### BusinessRecommendation

Required properties:

- `recommendation_id`
- `action_type`
- `target_type`
- `target_id`
- `priority`
- `trigger`
- `reason`
- `evidence`
- `status`
- `created_at`
- `source_table`
- `source_view`

Operator questions:

- What should I do this week?
- Why did the AI recommend this?
- What evidence supports it?
- Has this been approved, rejected, executed, or expired?

## First-Version Object Boundary

This ontology should not over-model the world too early. The first version should focus on objects that the current dataset and analysis layer can support:

- Strong: Customer, Order, OrderItem, Product, ProductCategory, Seller, Payment, Review, Geography.
- Strong analytical: CustomerSegment, SellerRisk, DeliveryRisk, ReviewRisk, ProductOpportunity, BusinessRecommendation.
- Future only: Carrier, Coupon, MarketingCampaign, Refund, SupportTicket, Inventory, AdSpend.

Future objects should not be introduced into action logic unless evidence exists.

