# Object Links

## Link Design Principle

Links are what let the AI analyst reason across the business instead of answering from isolated tables.

For example, seller risk is not a property of the seller table alone. It emerges from seller -> order items -> orders -> delivery dates -> reviews.

## Core Links

| Link | From | To | Source join | Business question enabled |
|---|---|---|---|---|
| CustomerPlacedOrder | Customer | Order | `customers.customer_id = orders.customer_id` | Which orders did this customer place? |
| OrderContainsOrderItem | Order | OrderItem | `orders.order_id = order_items.order_id` | What products and sellers were in this order? |
| OrderItemReferencesProduct | OrderItem | Product | `order_items.product_id = products.product_id` | Which product was sold? |
| OrderItemFulfilledBySeller | OrderItem | Seller | `order_items.seller_id = sellers.seller_id` | Which seller fulfilled the item? |
| ProductBelongsToCategory | Product | ProductCategory | `products.product_category_name = category_translation.product_category_name` | Which category does this product belong to? |
| OrderHasPayment | Order | Payment | `orders.order_id = order_payments.order_id` | How much revenue did this order create? |
| OrderReceivedReview | Order | Review | `orders.order_id = order_reviews.order_id` | What feedback did the order receive? |
| CustomerLocatedInGeography | Customer | Geography | zip prefix or state | Where is this customer located? |
| SellerLocatedInGeography | Seller | Geography | zip prefix or state | Where is this seller located? |

## Analytical Links

| Link | From | To | Evidence table | Business question enabled |
|---|---|---|---|---|
| CustomerBelongsToSegment | Customer | CustomerSegment | `customer_rfm` | What value or retention state is this customer in? |
| CustomerHasRetentionOpportunity | Customer | RetentionOpportunity | `dormant_high_value` | Is this customer worth winback? |
| SellerHasRisk | Seller | SellerRisk | `seller_risk_watchlist` | Why is this seller risky? |
| ProductCategoryHasReviewRisk | ProductCategory | ReviewRisk | `review_risk_by_category` | Which categories have elevated dissatisfaction? |
| GeographyHasDeliveryRisk | Geography | DeliveryRisk | `delivery_risk_by_state` | Which regions create delivery risk? |
| ProductCategoryHasProductOpportunity | ProductCategory | ProductOpportunity | `category_opportunity` | Which categories should be promoted, protected, or investigated? |
| BusinessRecommendationTargetsObject | BusinessRecommendation | Any target object | derived recommendation table | What object does this recommendation act on? |

## Traversal Patterns

The AI analyst should use links to answer multi-hop business questions.

### Seller Risk Traversal

```text
Seller
  -> OrderItem
  -> Order
  -> Review
  -> SellerRisk
  -> BusinessRecommendation
```

Use when the operator asks:

- Which sellers should we investigate?
- Are poor reviews associated with certain sellers?
- Which risky sellers also have meaningful revenue?

### Customer Winback Traversal

```text
Customer
  -> Order
  -> Payment
  -> CustomerSegment
  -> RetentionOpportunity
  -> BusinessRecommendation
```

Use when the operator asks:

- Which customers should receive a winback offer?
- Which segment has high historical value but poor recent activity?

### Category Opportunity Traversal

```text
ProductCategory
  -> Product
  -> OrderItem
  -> Order
  -> Review
  -> ProductOpportunity or ReviewRisk
```

Use when the operator asks:

- Which categories are revenue-critical?
- Which categories have high revenue but elevated dissatisfaction?
- Should a category be promoted or investigated?

### Delivery Risk Traversal

```text
Geography
  -> Customer or Seller
  -> Order
  -> DeliveryRisk
  -> BusinessRecommendation
```

Use when the operator asks:

- Which states are creating delivery risk?
- Should we monitor or adjust delivery expectations in a region?

## Link Confidence

Not all links have the same reliability.

| Confidence | Meaning | Example |
|---|---|---|
| High | Stable identifier join with near-complete match | `order_id`, `customer_id`, `product_id`, `seller_id` |
| Medium | Reference join, aggregation, or non-unique geographic mapping | zip prefix to geolocation |
| Low | Inferred relationship without direct data | carrier behavior, coupon response, supplier cause |

The AI analyst should state uncertainty when using medium or low confidence links.

## Link Guardrails

- Do not imply cause from a link alone.
- Use "associated with" when the data shows correlation but not causal proof.
- Do not traverse to future objects that are not supported by current data.
- Do not expose unnecessary customer identifiers in business summaries.
- Every recommendation must point to a target object through a valid link.

