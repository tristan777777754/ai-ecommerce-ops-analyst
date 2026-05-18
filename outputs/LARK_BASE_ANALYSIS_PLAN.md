# Lark Base Multi-Dimensional Analysis Plan

This is the first execution milestone for the project.

The goal is to let AI Agent 1 use Lark CLI / Lark Base to turn the raw Olist dataset into a multi-dimensional analysis workspace. This is a data warehouse / analysis layer, not ontology yet.

## Current Readiness

Status:

- Dataset exists locally in `dataset/`.
- `lark-cli` exists at `/Users/tristan/.npm-global/bin/lark-cli`, version `1.0.31`.
- `lark-cli` is not currently available through the default shell PATH, so use the absolute path or add `/Users/tristan/.npm-global/bin` to PATH.
- Current Lark identity is `user` for `tristan`.
- Authentication was refreshed successfully on 2026-05-17.
- Current token status is `valid`.
- Required import and Base write scopes are available:
  - `docs:document:import`
  - `drive:file:upload`
  - `drive:drive.metadata:readonly`
  - `base:app:create`
  - `base:table:create`
  - `base:field:create`
  - `base:record:create`
  - `base:view:write_only`
- A dry run for CSV to bitable import succeeded using `product_category_name_translation.csv`.
- User provided target URL: `https://gjp09unafl8q.jp.larksuite.com/base/workspace/XcnGsbyZOpyj0IcAnQXjsggUpyf`.
- The provided `/base/workspace/...` token is not a Drive folder token:
  - `drive +import --folder-token XcnGsbyZOpyj0IcAnQXjsggUpyf` failed with `folder not exist`.
  - `base +base-get --base-token XcnGsbyZOpyj0IcAnQXjsggUpyf` failed with `NOTEXIST`.
- No Lark Base was created by that failed import attempt.
- Created Drive folder in root:
  - name: `AI E-commerce Ops Analyst`
  - folder_token: `RbBdfI3vElN7nCdOGXdjhLySpec`
  - url: `https://gjp09unafl8q.jp.larksuite.com/drive/folder/RbBdfI3vElN7nCdOGXdjhLySpec`
- Verified CSV-to-bitable import into that folder with the smallest source table:
  - source: `dataset/product_category_name_translation.csv`
  - imported Base name: `raw_category_translation`
  - base_token: `KQx4bnEcUaH6VgsGiy1j4SXTpDR`
  - url: `https://gjp09unafl8q.jp.larksuite.com/base/KQx4bnEcUaH6VgsGiy1j4SXTpDR`
  - table renamed to: `raw_category_translation`
- Verified multi-sheet workbook import behavior:
  - test Base: `https://gjp09unafl8q.jp.larksuite.com/base/BYslbpaVkaF282sWBpOjgIDXp6Q`
  - result: one workbook sheet becomes one Base table
- Created staging workbook for full raw import:
  - local file: `outputs/lark_import_staging/olist_raw_tables_for_lark_base.xlsx`
  - size: 79.3 MB
- Imported the full raw dataset into one Lark Base:
  - name: `AI E-commerce Ops Analyst - Raw Data`
  - base_token: `TARLbZQYXaU1g7syARVjHYf4plc`
  - url: `https://gjp09unafl8q.jp.larksuite.com/base/TARLbZQYXaU1g7syARVjHYf4plc`
  - import ticket: `7640745695749803543`
  - tables:
    - `raw_customers`: `tbl5VsqlbR6cO2dY`
    - `raw_orders`: `tbl6bT6sXZtRUMl8`
    - `raw_order_items`: `tbl7utawCpYwhx2B`
    - `raw_order_payments`: `tbl5wT5GIf3kWT1t`
    - `raw_order_reviews`: `tbl2faX9LB2bbZgK`
    - `raw_products`: `tbl5z4HqUN4JCgB0`
    - `raw_sellers`: `tbl27Pv5yqBsinGE`
    - `raw_geolocation`: `tbl2XwzOqd8XeAC7`
    - `raw_category_translation`: `tbl4RWxRL2yavrAK`
- Field validation notes:
  - `raw_orders`, `raw_order_items`, and `raw_customers` are readable through `base +field-list`.
  - Most imported fields are text fields, with some select fields inferred automatically, so derived analysis tables should use explicitly typed fields rather than relying on raw imported field types.
- Created staging workbook for the analysis layer:
  - local file: `outputs/lark_import_staging/olist_analysis_layer_for_lark_base.xlsx`
  - size: 26.0 MB
- Imported the analysis layer into one Lark Base:
  - name: `AI E-commerce Ops Analyst - Analysis Layer`
  - base_token: `EXkPb3IaUapEgfsYMvKjYGdxpQe`
  - url: `https://gjp09unafl8q.jp.larksuite.com/base/EXkPb3IaUapEgfsYMvKjYGdxpQe`
  - import ticket: `7640748402523541018`
  - tables:
    - `executive_summary`: `tbl7MypbBpP8NbLv`
    - `monthly_revenue_trend`: `tbl6jpMumbFG4piZ`
    - `order_facts`: `tbl3qd57DGtt37et`
    - `customer_rfm`: `tbl4edZKmkhXPNjZ`
    - `rfm_segment_summary`: `tbl74wDBRuC1vJ3r`
    - `dormant_high_value`: `tbl2sCCt6qalLAgv`
    - `seller_performance`: `tblhz455orc0T3jY`
    - `seller_risk_watchlist`: `tbl7HjmwVrDGustt`
    - `category_performance`: `tbl6LZMWhmStjakS`
    - `category_opportunity`: `tbl6io0dezMLrZAr`
    - `product_performance_top`: `tbl4SjU2dPqhm8SD`
    - `delivery_risk_by_state`: `tbl4OfjvVEmTxBcP`
    - `review_risk_by_category`: `tbl1JGPhwed0yq4E`
- Created dashboard:
  - name: `E-commerce Ops Analysis Dashboard`
  - dashboard_id: `blkmMFq4QEHGvpB8`
  - blocks:
    - `Analysis Layer Checkpoint`
    - `Total Revenue`
    - `Total Orders`
    - `Monthly Revenue Trend`
    - `RFM Segment Revenue`
    - `RFM Customer Mix`
    - `Category Revenue Pareto`
    - `Seller Risk Bands`
    - `Delivery Risk by State`
    - `Review Risk by Category`
- Created sorted analysis views:
  - `Winback Priority` on `dormant_high_value`
  - `Seller Risk Triage` on `seller_risk_watchlist`
  - `Category Pareto` on `category_performance`
  - `Delivery Risk Monitor` on `delivery_risk_by_state`
  - `Review Risk Investigation` on `review_risk_by_category`
- Created first ontology/action-layer table:
  - table: `business_recommendations`
  - table_id: `tblkxo9xl31Rfmc8`
  - records: `94`
  - status: all records are `proposed`
  - created_at value: `2026-05-18`
  - local source CSV: `outputs/business_recommendations/business_recommendations.csv`
  - local summary: `outputs/business_recommendations/BUSINESS_RECOMMENDATIONS.md`
  - builder script: `scripts/build_business_recommendations.py`
  - publisher script: `scripts/publish_business_recommendations_to_lark.py`
- Created recommendation views:
  - `High Priority Proposed`: `veweUjCkfO`
  - `Seller Action Triage`: `vewTg7buZI`
  - `Customer Winback`: `vewGOO4oW6`
  - `Review and Delivery Risk`: `vewP6g98Ns`
- No dataset files were modified.

Target raw-data Base and analysis-layer Base are now ready. The first ontology/action-layer `BusinessRecommendation` table has also been generated from the analysis layer and written back to Lark Base.

## Source Dataset

| Source file | Rows including header | Size | Purpose |
|---|---:|---:|---|
| `olist_customers_dataset.csv` | 99,442 | 8.6M | Customer identity and location |
| `olist_geolocation_dataset.csv` | 1,000,164 | 58M | Zip-prefix geography reference |
| `olist_order_items_dataset.csv` | 112,651 | 15M | Order line items, products, sellers, price, freight |
| `olist_order_payments_dataset.csv` | 103,887 | 5.5M | Payment methods, installments, payment values |
| `olist_order_reviews_dataset.csv` | 104,720 | 14M | Review scores and comments |
| `olist_orders_dataset.csv` | 99,442 | 17M | Order lifecycle and delivery timestamps |
| `olist_products_dataset.csv` | 32,952 | 2.3M | Product catalog and physical attributes |
| `olist_sellers_dataset.csv` | 3,096 | 172K | Seller identity and location |
| `product_category_name_translation.csv` | 71 | 4.0K | Category translation |

## Phase 1: Raw Tables

Create one raw Lark Base table per CSV.

Recommended table names:

- `raw_customers`
- `raw_geolocation`
- `raw_order_items`
- `raw_order_payments`
- `raw_order_reviews`
- `raw_orders`
- `raw_products`
- `raw_sellers`
- `raw_category_translation`

Purpose:

- Preserve source data in Lark Base.
- Let the agent inspect fields and build multi-dimensional views.
- Keep raw tables separate from derived analysis tables.

## Raw Table Field Plan

### `raw_customers`

- `customer_id`: text
- `customer_unique_id`: text
- `customer_zip_code_prefix`: number
- `customer_city`: text
- `customer_state`: single select or text

### `raw_orders`

- `order_id`: text
- `customer_id`: text
- `order_status`: single select
- `order_purchase_timestamp`: datetime
- `order_approved_at`: datetime
- `order_delivered_carrier_date`: datetime
- `order_delivered_customer_date`: datetime
- `order_estimated_delivery_date`: datetime

### `raw_order_items`

- `order_id`: text
- `order_item_id`: number
- `product_id`: text
- `seller_id`: text
- `shipping_limit_date`: datetime
- `price`: currency or number
- `freight_value`: currency or number

### `raw_order_payments`

- `order_id`: text
- `payment_sequential`: number
- `payment_type`: single select
- `payment_installments`: number
- `payment_value`: currency or number

### `raw_order_reviews`

- `review_id`: text
- `order_id`: text
- `review_score`: number
- `review_comment_title`: text
- `review_comment_message`: multiline text
- `review_creation_date`: datetime
- `review_answer_timestamp`: datetime

### `raw_products`

- `product_id`: text
- `product_category_name`: text
- `product_name_lenght`: number
- `product_description_lenght`: number
- `product_photos_qty`: number
- `product_weight_g`: number
- `product_length_cm`: number
- `product_height_cm`: number
- `product_width_cm`: number

### `raw_sellers`

- `seller_id`: text
- `seller_zip_code_prefix`: number
- `seller_city`: text
- `seller_state`: single select or text

### `raw_geolocation`

- `geolocation_zip_code_prefix`: number
- `geolocation_lat`: number
- `geolocation_lng`: number
- `geolocation_city`: text
- `geolocation_state`: single select or text

### `raw_category_translation`

- `product_category_name`: text
- `product_category_name_english`: text

## Phase 2: Derived Analysis Tables

These tables should be created after raw import. They are analytical views, not ontology objects yet.

### `order_facts`

Purpose:

One row per order, joining order lifecycle, customer, payment, review, delivery, and item summary signals.

Key fields:

- `order_id`
- `customer_id`
- `customer_unique_id`
- `customer_state`
- `order_status`
- `purchase_date`
- `delivered_customer_date`
- `estimated_delivery_date`
- `payment_value`
- `item_revenue`
- `freight_value`
- `item_count`
- `seller_count`
- `avg_review_score`
- `low_review_flag`
- `delivery_delay_days`
- `late_delivery_flag`

### `customer_rfm`

Purpose:

Segment customers by recency, frequency, and monetary value.

Key fields:

- `customer_unique_id`
- `first_purchase_date`
- `last_purchase_date`
- `recency_days`
- `frequency`
- `monetary_value`
- `avg_order_value`
- `rfm_segment`
- `churn_risk_score`

### `customer_segment_summary`

Purpose:

Aggregate customer segments for winback and retention analysis.

Key fields:

- `segment`
- `customers`
- `revenue`
- `revenue_share`
- `avg_recency_days`
- `avg_frequency`
- `avg_monetary_value`

### `seller_performance`

Purpose:

Rank sellers by revenue, delivery reliability, and review dissatisfaction.

Key fields:

- `seller_id`
- `seller_city`
- `seller_state`
- `orders`
- `items`
- `revenue`
- `freight_value`
- `avg_review_score`
- `low_review_rate`
- `late_delivery_rate`
- `avg_delivery_delay_days`
- `seller_reliability_score`
- `risk_band`

### `category_performance`

Purpose:

Understand revenue concentration and category-level risk.

Key fields:

- `category_name`
- `orders`
- `products`
- `revenue`
- `revenue_share`
- `cumulative_revenue_share`
- `pareto_band`
- `avg_review_score`
- `low_review_rate`
- `late_delivery_rate`

### `delivery_risk`

Purpose:

Detect delivery risk clusters by geography, seller, or category.

Key fields:

- `risk_id`
- `target_type`
- `target_id`
- `orders`
- `late_delivery_rate`
- `avg_delay_days`
- `priority`
- `evidence`

### `review_risk`

Purpose:

Detect dissatisfaction clusters by seller, product, or category.

Key fields:

- `risk_id`
- `target_type`
- `target_id`
- `orders`
- `revenue`
- `low_review_rate`
- `avg_review_score`
- `priority`
- `evidence`

### `pareto_revenue`

Purpose:

Show revenue concentration across sellers, categories, and products.

Key fields:

- `dimension_type`
- `dimension_id`
- `orders`
- `revenue`
- `revenue_share`
- `cumulative_share`
- `pareto_band`

## Phase 3: Base Views / Dashboards

Create views after derived tables exist.

Recommended views:

- `Executive Summary`
- `Customer Segments`
- `Dormant High Value Customers`
- `Seller Risk Watchlist`
- `Category Revenue Pareto`
- `Delivery Risk by State`
- `Review Risk by Category`
- `Top Weekly Signals`

## Phase 4: Checkpoint

At this checkpoint, stop and label the result correctly:

```text
This is a Lark Base multi-dimensional analysis workspace.
It is useful analysis, but it is not ontology yet.
```

Only after this checkpoint should AI Agent 2 use the Palantir / AIP wiki to design ontology objects, links, actions, and BusinessRecommendation records.

## Execution Blocker

`lark-cli` is installed but not available in the default PATH.

Needed before execution:

1. Use `/Users/tristan/.npm-global/bin/lark-cli` directly, or add `/Users/tristan/.npm-global/bin` to PATH.
2. Confirm the target Lark workspace/folder where the Base should be created. If no folder token is provided, imports go to the user's root Drive folder.
3. Confirm import strategy:
   - one bitable per CSV; simplest import path, but splits raw tables across multiple Base files
   - one combined Excel workbook imported as one bitable; better workspace shape, but requires creating an import staging workbook
   - one manually created Base with API record uploads; best control, but slowest because record batch writes are limited
4. Import CSV files or create Base tables according to this plan.

Authentication command already completed:

```bash
/Users/tristan/.npm-global/bin/lark-cli auth login --domain base
```

Dry-run verified import route:

```bash
/Users/tristan/.npm-global/bin/lark-cli drive +import --type bitable --file dataset/olist_customers_dataset.csv --name raw_customers
```

Dry-run result shape:

```text
upload file -> create import task -> poll import task result
```

## Recommended Import Strategy

The ideal Lark Base shape is one Base workspace with multiple raw tables and derived analysis tables.

Because `drive +import --type bitable --file <csv>` imports a CSV as a bitable document, importing every CSV directly may create separate Base files instead of one unified workspace.

Recommended next decision:

1. If speed matters most, import each CSV as its own raw Base first, then use them as source tables.
2. If workspace coherence matters most, create a staging Excel workbook with one sheet per raw CSV and import that workbook as one bitable.
3. If exact table and field control matters most, create one Base with `base +base-create`, create tables with `base +table-create`, then batch-write records. This is slower for the 1,000,163-row geolocation table.

For this project, option 2 is likely the best fit if Lark import supports one worksheet -> one Base table conversion cleanly.
