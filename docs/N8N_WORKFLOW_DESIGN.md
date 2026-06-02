# n8n Workflow Design: AI E-commerce Ops Analyst

# n8n local host

http://localhost:5678/home/workflows

## Purpose

This document defines the n8n workflow design for the AI E-commerce Ops Analyst project.

The goal is not to replace the existing web UI chatbox. The existing `webui` already provides the assistant interface:

```text
User question
  -> webui /api/chat
  -> assistant answers using ontology + BusinessRecommendation records
```

n8n should act as the orchestration layer around the assistant:

```text
Dataset
  -> build Lark-ready analysis layer
  -> generate BusinessRecommendation records
  -> optionally sync records to Lark Base
  -> webui assistant answers user questions from those records
  -> n8n handles approval / status update / notifications / downstream actions
```

In simple terms:

```text
webui = assistant and chat experience
n8n = workflow orchestration and operational action layer
Lark Base = shared analysis / recommendation tracking workspace
```

## Current Project Capabilities

The repository already includes:

- Local dataset under `dataset/`
- Lark-ready workbook builders under `scripts/`
- Business recommendation generator under `scripts/build_business_recommendations.py`
- Optional Lark publishing script under `scripts/publish_business_recommendations_to_lark.py`
- Web chat assistant under `webui/server.py`
- Assistant context loaded from:
  - `agent/ecommerce_ops_analyst_system_prompt.md`
  - `ontology/actions.yml`
  - `ontology/objects.yml`
  - `ontology/links.yml`
  - `outputs/business_recommendations/WEEKLY_OPS_BRIEF.md`
  - `outputs/business_recommendations/BUSINESS_RECOMMENDATIONS.md`
  - `outputs/business_recommendations/business_recommendations.csv`

The local assistant endpoint is:

```text
POST http://127.0.0.1:8787/api/chat
```

If n8n runs in Docker, use:

```text
POST http://host.docker.internal:8787/api/chat
```

Example request body:

```json
{
  "message": "What should I do this week?",
  "history": []
}
```

## Target End-to-End Workflow

The full system should be split into three workflows.

## Workflow 1: Dataset To Analysis Layer

### Goal

Turn the raw e-commerce dataset into a real Lark Base multi-dimensional analysis workspace.

Python is only used to create staging workbooks from the local CSV dataset. The actual analysis workspace must be created or refreshed through Lark CLI / Lark Base. This keeps the project aligned with the intended agent-operated workflow:

```text
raw dataset
  -> Python staging workbook builders
  -> Lark CLI imports the workbooks as Base documents
  -> Lark Base becomes the shared multi-dimensional analysis layer
```

This workflow should prepare and publish analysis tables such as:

- Customer RFM segments
- Seller risk watchlist
- Product category performance
- Delivery risk
- Review dissatisfaction risk
- Revenue concentration / Pareto signals

### n8n Nodes

```text
Manual Trigger
  -> Set Run Context
  -> Execute Command: build raw import workbook
  -> Execute Command: import raw workbook to Lark Base
  -> Execute Command: build analysis workbook
  -> Execute Command: import analysis workbook to Lark Base
  -> Optional: create / refresh Lark Base views and dashboard
  -> Notify operator that Lark analysis layer is ready
```

### Runtime Requirement

Because n8n runs in Docker, the Execute Command nodes must run in an environment that can access:

```text
/Users/tristan/AI E-commerce Ops Analyst
/Users/tristan/.npm-global/bin/lark-cli
Lark CLI auth/config for the current user
```

If those paths are not mounted into the n8n container, use a host runner pattern instead, such as SSH to the host machine or a small local service that runs the commands on the host. Do not treat local Excel generation as success unless the Lark Base import also completes.

Current implementation:

```text
n8n Docker container
  -> HTTP Request nodes call http://host.docker.internal:8788/run
  -> macOS LaunchAgent runs scripts/n8n_workflow1_runner.py
  -> host runner uses local Python and authenticated Lark CLI
```

### Node Details

#### 1. Manual Trigger

Use Manual Trigger for the first version.

Later this can become:

```text
Schedule Trigger
```

for daily or weekly rebuilds.

#### 2. Set Run Context

Fields:

```json
{
  "run_id": "manual_{{$now}}",
  "dataset_source": "local_dataset",
  "project_root": "/Users/tristan/AI E-commerce Ops Analyst",
  "lark_cli": "/Users/tristan/.npm-global/bin/lark-cli",
  "lark_folder_token": "RbBdfI3vElN7nCdOGXdjhLySpec"
}
```

#### 3. Execute Command: Build Raw Import Workbook

Command:

```bash
cd "/Users/tristan/AI E-commerce Ops Analyst" && python3 scripts/build_lark_import_workbook.py
```

Expected output:

```text
outputs/lark_import_staging/olist_raw_tables_for_lark_base.xlsx
```

#### 4. Execute Command: Import Raw Workbook To Lark Base

Command:

```bash
cd "/Users/tristan/AI E-commerce Ops Analyst" && /Users/tristan/.npm-global/bin/lark-cli drive +import --type bitable --file outputs/lark_import_staging/olist_raw_tables_for_lark_base.xlsx --name "AI E-commerce Ops Analyst - Raw Data {{$json.run_id}}" --folder-token RbBdfI3vElN7nCdOGXdjhLySpec --as user
```

Expected result:

```text
A Lark Base is created or refreshed for raw source tables.
The import result returns a Base URL / token and an import ticket.
```

Known existing raw-data Base:

```text
https://gjp09unafl8q.jp.larksuite.com/base/TARLbZQYXaU1g7syARVjHYf4plc
```

Latest Workflow 1 raw-data Base:

```text
https://gjp09unafl8q.jp.larksuite.com/base/DVQabiT22adhQnsSBjijlJySpHc
```

#### 5. Execute Command: Build Analysis Workbook

Command:

```bash
cd "/Users/tristan/AI E-commerce Ops Analyst" && python3 scripts/build_lark_analysis_workbook.py
```

Expected output:

```text
outputs/lark_import_staging/olist_analysis_layer_for_lark_base.xlsx
```

#### 6. Execute Command: Import Analysis Workbook To Lark Base

Command:

```bash
cd "/Users/tristan/AI E-commerce Ops Analyst" && /Users/tristan/.npm-global/bin/lark-cli drive +import --type bitable --file outputs/lark_import_staging/olist_analysis_layer_compact_for_lark_base.xlsx --name "AI E-commerce Ops Analyst - Analysis Layer {{$json.run_id}}" --folder-token RbBdfI3vElN7nCdOGXdjhLySpec --as user
```

Expected result:

```text
A Lark Base is created or refreshed for the analysis layer.
The import result returns a Base URL / token and an import ticket.
```

The full workbook remains available locally at:

```text
outputs/lark_import_staging/olist_analysis_layer_for_lark_base.xlsx
```

The compact Lark import workbook excludes oversized detail sheets such as full `order_facts` and full `customer_rfm`, while retaining the operator-facing analysis tables needed for the first workflow.

Known existing analysis-layer Base:

```text
https://gjp09unafl8q.jp.larksuite.com/base/EXkPb3IaUapEgfsYMvKjYGdxpQe
```

Latest Workflow 1 analysis-layer Base:

```text
https://gjp09unafl8q.jp.larksuite.com/base/NSswboSyUamlCVsrKyzjQLqWpze
```

#### 7. Optional Execute Command: Refresh Views And Dashboard

After the analysis Base import succeeds, use Lark CLI Base commands to recreate or refresh operator-facing views such as:

```text
Winback Priority
Seller Risk Triage
Category Pareto
Delivery Risk Monitor
Review Risk Investigation
E-commerce Ops Analysis Dashboard
```

Use `lark-cli base +view-create`, `base +view-set-sort`, `base +view-set-filter`, and dashboard commands only after the imported Base token and table IDs are known.

### Success Criteria

- Raw import workbook exists
- Analysis workbook exists
- Raw dataset is imported into Lark Base
- Analysis layer is imported into Lark Base
- n8n execution shows the Python staging commands and Lark CLI import commands completed successfully
- The operator can open the Lark Base analysis workspace and see the raw tables plus derived analysis tables

## Workflow 2: Analysis Layer To BusinessRecommendation

### Goal

Convert the analysis layer into structured `BusinessRecommendation` records.

These records are the assistant's action memory. The webui assistant should answer from these records instead of improvising.

### n8n Nodes

```text
Manual Trigger
  -> Set Run Context
  -> HTTP Request: build business recommendations through host runner
  -> HTTP Request: publish recommendations to Lark Base through host runner
  -> HTTP Request: ask assistant to summarize latest recommendations
  -> Set: workflow completion payload
```

Current implementation:

```text
n8n workflow id: jTn8aUJ8YtoVK7Ic
n8n URL: http://localhost:5678/workflow/jTn8aUJ8YtoVK7Ic
analysis Base: https://gjp09unafl8q.jp.larksuite.com/base/NSswboSyUamlCVsrKyzjQLqWpze
business_recommendations table id: tblX5L0laIRjYrwv
host runner: http://host.docker.internal:8788/run
assistant API: http://host.docker.internal:8787/api/chat
```

### Node Details

#### 1. Set Run Context

Fields:

```json
{
  "run_id": "manual_{{$now}}",
  "analysis_base_token": "NSswboSyUamlCVsrKyzjQLqWpze",
  "business_recommendations_table": "business_recommendations",
  "runner_url": "http://host.docker.internal:8788",
  "assistant_url": "http://host.docker.internal:8787/api/chat"
}
```

#### 2. HTTP Request: Build Business Recommendations

Method:

```text
POST
```

URL:

```text
http://host.docker.internal:8788/run
```

Body:

```json
{
  "step": "build_business_recommendations",
  "run_id": "{{$json.run_id}}"
}
```

Expected outputs:

```text
outputs/business_recommendations/business_recommendations.csv
outputs/business_recommendations/BUSINESS_RECOMMENDATIONS.md
outputs/business_recommendations/business_recommendations_lark_batch.json
```

#### 3. HTTP Request: Publish To Lark Base

The host runner executes `scripts/publish_business_recommendations_to_lark.py` with the authenticated local Lark CLI user.

Method:

```text
POST
```

URL:

```text
http://host.docker.internal:8788/run
```

Body:

```json
{
  "step": "publish_business_recommendations",
  "run_id": "{{$json.run_id}}"
}
```

Expected result:

```text
BusinessRecommendation records exist in the configured Lark Base table.
The publish script is idempotent: when the table already has the expected record count, it skips creating duplicates.
```

#### 4. HTTP Request: Ask Local Assistant For Summary

Method:

```text
POST
```

URL:

```text
http://host.docker.internal:8787/api/chat
```

Body:

```json
{
  "message": "Summarize the latest BusinessRecommendation records as an operator-facing weekly ops brief. Include the top 3 proposed actions, evidence, recommendation IDs, and approval note. Do not claim actions have been executed.",
  "history": []
}
```

Expected response:

```json
{
  "ok": true,
  "answer": "...",
  "model": "gpt-5-mini"
}
```

### Success Criteria

- `business_recommendations.csv` is regenerated
- `BUSINESS_RECOMMENDATIONS.md` is regenerated
- `business_recommendations_lark_batch.json` is regenerated
- Lark Base table `business_recommendations` exists in the analysis Base
- Lark publish is idempotent and does not duplicate existing recommendation records
- Assistant can answer from the latest recommendation records

Latest verified execution:

```text
n8n execution id: 10
status: success
records generated: 94
existing Lark records: 94
created Lark records on rerun: 0
```

## Workflow 3: Assistant Action Workflow

### Goal

Let the assistant turn user intent into operational workflow actions.

The webui remains the chatbox. n8n receives action requests only when the user wants to approve, reject, assign, or execute a recommendation workflow.

### Example User Flow

```text
User asks in webui:
  "What should I do this week?"

Assistant answers:
  "Approve REC-0001 for Dormant High Value winback.
   Investigate seller REC-0033.
   Investigate category REC-0069."

User says:
  "Approve REC-0001."

webui calls n8n webhook:
  recommendation_id = REC-0001
  action = approve

n8n:
  -> updates Lark Base status to approved
  -> creates task for owner
  -> sends Lark notification
  -> returns success to webui
```

### n8n Nodes

```text
Webhook Trigger
  -> Validate Input
  -> Lookup Recommendation
  -> Update Lark Base Status
  -> Optional: Create Lark Task
  -> Optional: Send Lark Message
  -> Respond To Webhook
```

### Webhook Input Contract

Endpoint:

```text
POST /webhook/recommendation-action
```

Body:

```json
{
  "recommendation_id": "REC-0001",
  "action": "approve",
  "actor": "operator",
  "comment": "Approved for campaign brief creation."
}
```

Allowed actions:

```text
approve
reject
assign
create_task
notify_owner
```

### Validation Rules

n8n should reject the request if:

- `recommendation_id` is missing
- `action` is missing
- `action` is not in the allowed action list
- recommendation ID cannot be found
- the recommendation is already executed or expired

### Status Mapping

```text
approve -> status = approved
reject -> status = rejected
create_task -> status remains approved or proposed depending on approval state
notify_owner -> status unchanged
```

### Respond To Webhook

Success response:

```json
{
  "ok": true,
  "recommendation_id": "REC-0001",
  "status": "approved",
  "message": "Recommendation REC-0001 was approved and routed for follow-up."
}
```

Failure response:

```json
{
  "ok": false,
  "error": "Recommendation ID was not found."
}
```

## Recommended First Implementation

Build this minimal workflow first:

```text
Manual Trigger
  -> Execute Command: python3 scripts/build_lark_analysis_workbook.py
  -> Execute Command: python3 scripts/build_business_recommendations.py
  -> HTTP Request: POST /api/chat summarize latest recommendations
```

This proves the core loop:

```text
Dataset
  -> analysis layer
  -> business recommendations
  -> assistant answer
```

Do not start with email. Email is only useful as a temporary test output, not the main product workflow.

## Later Implementation

After the minimal workflow works, add:

```text
Publish to Lark Base
  -> recommendation status tracking
  -> approval webhook
  -> task creation
  -> owner notification
```

At that point the product story becomes:

```text
The system does not just answer business questions.
It turns marketplace data into structured recommendations and routes approved actions into an operations workflow.
```

## AI Builder Prompt

Use this prompt when asking an AI agent to build the n8n workflow:

```text
You are building an n8n workflow for the repository:
/Users/tristan/AI E-commerce Ops Analyst

The existing webui chatbox is already complete and should not be replaced.

Design n8n as the orchestration layer for the AI E-commerce Ops Analyst system.

Build the first workflow:

Manual Trigger
  -> Execute Command:
     cd "/Users/tristan/AI E-commerce Ops Analyst" && python3 scripts/build_lark_analysis_workbook.py
  -> Execute Command:
     cd "/Users/tristan/AI E-commerce Ops Analyst" && python3 scripts/build_business_recommendations.py
  -> HTTP Request:
     POST http://host.docker.internal:8787/api/chat
     JSON body:
     {
       "message": "Summarize the latest BusinessRecommendation records as an operator-facing weekly ops brief. Include the top 3 proposed actions, evidence, recommendation IDs, and approval note. Do not claim actions have been executed.",
       "history": []
     }

The workflow should prove this loop:
Dataset -> analysis layer -> BusinessRecommendation records -> assistant answer.

Do not add email as the final product output.
Email may only be used as a temporary debug sink if needed.

After the first workflow works, propose a second workflow:
Webhook Trigger -> validate recommendation action -> update Lark Base status -> create task or notify owner -> respond to webhook.
```

## Demo Talk Track

Use this short explanation when presenting the system:

```text
The chatbox is not the whole system. The chatbox is the interface.

n8n runs the operational pipeline behind it:
it rebuilds the analysis layer from the dataset, generates BusinessRecommendation records, syncs them to the operating workspace, and later handles approval or task-routing actions.

The assistant answers from this recommendation memory, so the user gets grounded operational advice instead of generic chatbot output.
```
