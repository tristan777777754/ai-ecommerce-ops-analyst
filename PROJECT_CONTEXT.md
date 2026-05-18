# AI E-commerce Ops Ontology - Project Context

This is a portfolio project that simulates a Forward Deployed Engineer engagement for an e-commerce marketplace.

The project uses the Olist Brazilian E-Commerce Public Dataset to build a small-scale, Palantir-style operational ontology for e-commerce decision-making. The goal is not to make a generic dashboard or school-style data science notebook. The goal is to show how raw business data can be mapped into real-world business objects, relationships, metrics, risks, and recommended actions.

In plain language:

> This project turns messy e-commerce data into an AI-native operating model that tells a business owner who is buying, what is selling, what is going wrong, and what to do next.

## Project Goal

Build an AI-powered e-commerce operations analyst through an agent-operated workflow.

The intended build sequence is:

```text
Dataset
  -> AI Agent uses Lark CLI / Lark Base for multi-dimensional analysis
  -> analytical workspace and business signals
  -> checkpoint: this is useful analysis, but not ontology yet
  -> another AI Agent studies the Palantir / AIP wiki
  -> ontology objects, relationships, action types, and recommendations
```

The project should not start by extending a local Python dashboard pipeline. Local scripts can be kept as reference, but the main project direction is AI Agent + Lark CLI + Lark Base first.

The demo should help a small e-commerce brand owner or marketplace operator understand:

- Which customers are valuable or at risk of churn
- Which products and categories are driving revenue
- Which sellers, orders, or delivery patterns create operational risk
- Which reviews signal customer dissatisfaction
- What actions the business should take next

The final project should feel like a practical business tool built by an FDE: part data model, part analytics layer, part AI decision assistant.

## FDE / Ontology Framing

The central idea is to model the business world, not just query tables.

The raw dataset contains CSV files such as orders, customers, products, sellers, payments, reviews, and geolocation data. The ontology turns those files into operational concepts that a human operator or AI agent can reason over.

This means the project should define:

- Object types: the core business entities
- Properties: the important attributes and calculated metrics on each entity
- Link types: the relationships between entities
- Functions: the business logic used to calculate risk, value, and performance
- Action types: the operational steps a business could take in response to insights

This is the difference between a dashboard and an operational system:

- A dashboard shows what happened.
- An ontology explains what the business objects are, how they relate, what state they are in, and what actions are available.

## Target Audience

The imagined customer is a small or medium e-commerce business owner, Shopify/DTC brand, marketplace seller, or agency serving e-commerce brands.

They probably care less about technical terms and more about:

- Revenue opportunities
- Customer retention
- Product performance
- Delivery and review problems
- Seller reliability
- Clear daily action recommendations

The portfolio audience is slightly different. It should also show that the builder understands the FDE mindset:

- Translate messy business operations into a clear data model
- Connect data engineering to real operational workflows
- Build useful abstractions without hiding the business reality
- Use AI to recommend decisions, not just summarize charts

## Dataset

Use the Olist Brazilian E-Commerce Public Dataset.

It includes anonymized e-commerce data such as:

- Orders
- Customers
- Order items
- Products
- Sellers
- Payments
- Reviews
- Delivery timestamps
- Geolocation data

This dataset is useful because it resembles a real marketplace business and has enough tables to demonstrate relationships between customers, orders, products, sellers, payments, reviews, and logistics.

The local dataset files are:

- `olist_customers_dataset.csv`
- `olist_geolocation_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_order_payments_dataset.csv`
- `olist_order_reviews_dataset.csv`
- `olist_orders_dataset.csv`
- `olist_products_dataset.csv`
- `olist_sellers_dataset.csv`
- `product_category_name_translation.csv`

## Ontology Design

The first version should model the following object types.

### Core Object Types

- `Customer`
- `Order`
- `OrderItem`
- `Product`
- `ProductCategory`
- `Seller`
- `Payment`
- `Review`
- `Delivery`
- `Geography`

### Analytical Object Types

- `CustomerSegment`
- `RetentionOpportunity`
- `ProductOpportunity`
- `SellerRisk`
- `DeliveryRisk`
- `ReviewRisk`
- `BusinessRecommendation`

These analytical objects are important because they make the project feel like an operational system instead of a set of charts. They represent business states that an operator can act on.

## Link Types

The ontology should make relationships explicit.

Examples:

- `Customer` placed `Order`
- `Order` contains `OrderItem`
- `OrderItem` references `Product`
- `OrderItem` is fulfilled by `Seller`
- `Product` belongs to `ProductCategory`
- `Order` has `Payment`
- `Order` received `Review`
- `Order` has `Delivery`
- `Customer` belongs to `CustomerSegment`
- `Seller` has `SellerRisk`
- `ProductCategory` has `ProductOpportunity`
- `BusinessRecommendation` targets `Customer`, `Seller`, `Product`, `Category`, or `Order`

These links are the backbone of the demo. They allow the AI analyst to answer questions across business concepts instead of isolated tables.

## Metrics / Functions Layer

The project should calculate business logic that can be attached to ontology objects.

Useful first-version metrics:

- Total revenue
- Revenue by product category
- Revenue by seller
- Order volume by time period
- Average order value
- Customer recency, frequency, and monetary value
- Customer lifetime value proxy
- Churn or inactivity risk
- Late delivery rate
- Average delivery delay
- Review dissatisfaction rate
- Seller reliability score
- Product review risk score
- Category performance score

Example object-level properties:

- `Customer.rfm_segment`
- `Customer.churn_risk_score`
- `Customer.lifetime_value`
- `Seller.late_delivery_rate`
- `Seller.average_review_score`
- `Seller.reliability_score`
- `Product.total_revenue`
- `Product.review_risk_score`
- `ProductCategory.revenue_share`
- `Order.delivery_delay_days`
- `Review.dissatisfaction_flag`

## Action Layer

The action layer is what makes the project feel closer to a Palantir-style operational workflow.

The AI analyst should not only describe problems. It should recommend actions that a business owner could realistically take.

Example action types:

- `SendReactivationOffer`
- `PrioritizeHighValueCustomer`
- `InvestigateLowReviewProduct`
- `InvestigateSeller`
- `DeprioritizeRiskySeller`
- `FixDeliveryProcess`
- `PromoteHighRevenueCategory`
- `MonitorDeliveryRisk`
- `CreateCustomerWinbackCampaign`

Example recommendations:

> These high-value customers used to buy often but have not returned recently. Send them a reactivation offer.

> This product category has strong revenue but poor review scores. Investigate delivery time, product quality, or seller reliability.

> This seller has frequent late deliveries and low review scores. Consider warning, monitoring, or deprioritizing them for high-value orders.

## Suggested Demo Direction

The first version can focus on a few high-impact workflows:

- Sales and revenue overview
- Customer segmentation using RFM analysis
- High-value customers who may be inactive
- Product and category performance
- Seller reliability analysis
- Delivery delay analysis
- Review score and dissatisfaction patterns
- AI-generated next best actions for the business owner

The demo should show both the business surface and the ontology underneath it.

Suggested screens or report sections:

- Business overview
- Customer intelligence
- Product and category performance
- Seller and delivery risk
- Review dissatisfaction analysis
- AI recommendations
- Ontology map or object relationship view

## Positioning

Do not position this as just a dashboard, notebook, or Kaggle project.

Position it as:

> A Palantir-style AI operations ontology for small e-commerce brands that turns order, product, customer, seller, delivery, and review data into operational recommendations.

Simpler version:

> It tells an e-commerce owner who is buying, what is selling, what is going wrong, and what to do next.

Portfolio version:

> I simulated a Forward Deployed Engineer engagement by turning a messy marketplace dataset into an operational ontology with business objects, links, metrics, risks, and AI-recommended actions.

## Short-Term Success

A good first milestone is:

- Load and clean the Olist dataset
- Join the key tables into analysis-ready views
- Define the first ontology object types and link types
- Build 5-8 useful business metrics
- Generate business risks and opportunities from those metrics
- Add an AI summary that explains the insights in plain business language
- Produce a simple dashboard, report, or app surface that demonstrates the operating model

The first version does not need to recreate Palantir Foundry. It should demonstrate the thinking: business objects, relationships, decision logic, and actions.

## Content / Portfolio Angle

This project can later be shared online with content like:

- "I simulated a Forward Deployed Engineer engagement for an e-commerce marketplace."
- "I built a small operational ontology over 100k e-commerce orders."
- "The system maps customers, orders, products, sellers, reviews, and deliveries into business objects and recommended actions."
- "It finds delayed delivery patterns, unhappy customers, risky sellers, and product opportunities."
- "The goal is to help small e-commerce brands make better daily decisions from messy operational data."

The project should produce screenshots, short demo videos, an ontology diagram, and simple business explanations that potential clients or hiring managers can understand quickly.
