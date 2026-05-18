# Project Map

This project is an agent-operated prototype for an AI e-commerce operations analyst.

The intended workflow follows the reference video more closely than a local Python analytics project. The first milestone is not to generate more local reports. The first milestone is to let an AI agent use Lark CLI / Lark Base as the working environment for multi-dimensional analysis.

## Core Direction

The project should move through two agent stages:

```text
dataset/
  raw Olist e-commerce CSV files
        ↓
AI Agent 1: data analysis agent
  uses Lark CLI / Lark Base to create a multi-dimensional analysis workspace:
    - raw source tables
    - cleaned or joined views
    - customer RFM segmentation
    - Pareto analysis
    - seller performance views
    - product and category performance views
    - delivery risk views
    - review dissatisfaction views
    - dashboards or Base views
        ↓
important checkpoint
  this is still data warehouse / analytical modeling work.
  It is useful, but it is not ontology yet.
        ↓
AI Agent 2: ontology agent
  reads the Palantir / AIP wiki and learns the method:
    - business objects
    - relationships
    - metrics as object state
    - actions
    - evidence requirements
    - approval and execution rules
        ↓
ontology design
  converts the analyzed business world into:
    - Customer, Order, Seller, ProductCategory, ReviewRisk, DeliveryRisk objects
    - object relationships
    - approved action types
    - BusinessRecommendation records
        ↓
operational layer
  the agent can answer, recommend, ask for approval, and eventually trigger
  Lark cards or approved workflow actions
```

In short:

```text
Dataset comes first.
Agent 1 uses Lark CLI to build the multi-dimensional analysis layer.
That analysis layer is not ontology yet.
Agent 2 uses the Palantir / AIP wiki to turn analysis into ontology.
The ontology then drives recommendations, approvals, and actions.
```

## Mental Model

There are three different knowledge layers in this project:

- `dataset/` is the raw operational data layer.
- Lark Base is the intended multi-dimensional analysis workspace operated by the AI agent.
- `wiki/palantir-aip/` is the methodology layer that teaches the ontology agent how Palantir-style AIP, AI FDE, ontology, logic, actions, and evals work.

The `ontology/` folder is a draft target model for the later ontology stage. It should not be treated as the first step. It becomes useful after the Lark Base analysis layer exists.

## Current Folders

### `dataset/`

Raw Olist Brazilian E-Commerce Public Dataset files.

These are the source-of-truth input tables:

- `olist_customers_dataset.csv`
- `olist_geolocation_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_order_payments_dataset.csv`
- `olist_order_reviews_dataset.csv`
- `olist_orders_dataset.csv`
- `olist_products_dataset.csv`
- `olist_sellers_dataset.csv`
- `product_category_name_translation.csv`

The first AI agent should inspect these files and use Lark CLI / Lark Base to create the first multi-dimensional analysis workspace.

### Lark Base / Lark CLI

This is the intended operational workspace for the first phase.

Agent 1 should use Lark CLI to create or update Base tables and views such as:

- raw tables mirroring the source CSV files
- joined order facts
- customer RFM table
- customer segment summary
- product and category performance views
- seller performance and seller risk views
- delivery risk by state, seller, or category
- review dissatisfaction analysis
- Pareto revenue analysis
- dashboard-style Base views

This layer answers business questions through analysis, but it is still not ontology.

### `wiki/`

Local Palantir AIP documentation wiki.

Important files:

- `wiki/palantir-aip/README.md`
- `wiki/palantir-aip/LEARNING_GUIDE_ZH.md`
- `wiki/palantir-aip/pages/`
- `wiki/ecommerce-ops-ontology/README.md`

Agent 2 should use this wiki after the Lark Base analysis layer exists. Its job is to learn the Palantir / AIP method and then convert the analyzed e-commerce world into objects, relationships, metrics, actions, and guardrails.

The project-specific ontology wiki now lives in `wiki/ecommerce-ops-ontology/`. It translates the Palantir / AIP method into this e-commerce operating model, including business objects, links, metrics, actions, AI analyst behavior, evals, governance, and demo workflow.

### `ontology/`

Draft machine-readable operating model for the later ontology stage.

This folder defines:

- `objects.yml`: business and analytical object types.
- `links.yml`: relationships between object types.
- `actions.yml`: approved action types, triggers, evidence requirements, and approval rules.

These files are useful as a draft target, but they should not replace the first-pass Lark Base analysis workflow.

### `agent/`

Agent operating instructions.

Current file:

- `ops_analyst_agent.md`: defines the intended agent roles, allowed outputs, safety rules, and answer behavior for the AI e-commerce operations analyst.
- `ecommerce_ops_analyst_system_prompt.md`: direct system prompt/spec for the ontology-aware AI analyst that answers from the Lark analysis layer and `BusinessRecommendation` records.

### `outputs/`

Curated reference outputs only.

Current retained files:

- `DATASET_SCHEMA.md`: profiles the raw dataset and maps tables to possible ontology objects and links.
- `AIP_APPLIED_ANALYSIS_BLUEPRINT.md`: describes how the local project maps to a Palantir AIP-style operational application.

These files are context and reference material. They are not the primary execution path.

### `scripts/`

Legacy local prototype scripts.

Current files:

- `build_ops_analysis.py`
- `build_dashboard.py`
- `build_palantir_aip_wiki.mjs`
- `build_business_recommendations.py`
- `publish_business_recommendations_to_lark.py`

The local Python analysis scripts may be useful as reference for metric definitions, but they are not the main project workflow. The main workflow is AI Agent -> Lark CLI -> Lark Base multi-dimensional analysis.

`build_palantir_aip_wiki.mjs` is separate because it supports the methodology wiki.

`build_business_recommendations.py` generates the first ontology/action-layer `BusinessRecommendation` records from the analysis layer. `publish_business_recommendations_to_lark.py` publishes those records to the Lark Analysis Layer Base table `business_recommendations`.

### AI Analyst Demo Artifacts

- `outputs/business_recommendations/WEEKLY_OPS_BRIEF.md`: human-readable weekly operating recommendations.
- `outputs/AI_ANALYST_DEMO_QA.md`: demo questions and expected AI analyst answers.

### `webui/`

Simple local web UI for the ontology-aware AI analyst.

Current files:

- `webui/server.py`: local Python server that calls the OpenAI Responses API.
- `webui/static/index.html`: operator-facing chat UI.
- `webui/static/styles.css`: UI styling.
- `webui/static/app.js`: browser chat behavior.
- `webui/.env.example`: local environment template for `OPENAI_API_KEY`, `OPENAI_MODEL`, and `PORT`.
- `webui/README.md`: run instructions.

The UI reads the local ontology prompt, recommendation artifacts, and action rules, then sends them to the OpenAI API so the analyst can answer questions like "What should I do this week?" using the `BusinessRecommendation` action layer.

### `notes/`

Working notes and learning notes.

Current files:

- `2026-05-16_lark-cli-palantir-fde-video-notes.md`
- `2026-05-16_project-vs-video-gap-analysis.md`

The video notes are important because they define the intended workflow: AI agent uses Lark CLI as its hands, builds an analysis workspace, then uses Palantir methodology to move from data warehouse to ontology.

## What This Project Currently Does

This project currently has:

- Raw Olist e-commerce data.
- Local Palantir / AIP learning context.
- Draft ontology definitions.
- Reference schema and AIP blueprint documents.
- Legacy local scripts that can be used as metric references.

## What This Project Should Do Next

The next step should be:

```text
raw dataset
  -> AI Agent 1
  -> Lark CLI / Lark Base
  -> multi-dimensional analysis workspace
```

The first Lark Base workspace should include:

- raw source tables
- joined order facts
- customer RFM analysis
- product/category revenue analysis
- seller performance analysis
- delivery delay analysis
- review dissatisfaction analysis
- summary dashboards or views

After that checkpoint, the second stage should begin:

```text
Lark Base analysis workspace
  -> AI Agent 2 reads Palantir / AIP wiki
  -> ontology objects, links, metrics, actions
  -> BusinessRecommendation records
  -> approval and execution workflow
```

## Current Boundary

This project should not be positioned as:

- a local Python dashboard project
- a Kaggle-style notebook
- a static report generator

It should be positioned as:

> An AI-agent-operated e-commerce analysis and ontology workflow where Lark CLI creates the multi-dimensional analysis layer, and Palantir / AIP methodology turns that analysis into business objects, relationships, recommendations, and actions.
