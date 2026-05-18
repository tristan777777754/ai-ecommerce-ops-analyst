---
title: "AIP Analyst > Core concepts"
source_url: "https://www.palantir.com/docs/foundry/aip-analyst/core-concepts/"
scraped_at: "2026-05-16T03:02:37.251Z"
section: "AIP Analyst"
canonical_slug: "/foundry/aip-analyst/core-concepts/"
---
# Core concepts

We recommend reviewing the following concepts before using AIP Analyst.

## Context

Context allows you to provide additional information to an analysis, and reduces the time needed for AIP Analyst to produce an answer. Adding a dataset to context enables AIP Analyst to analyze datasets, as opposed to object types, and can be used for exploratory data analysis before constructing an ontology.

## Analysis provenance

To improve confidence in AIP Analyst output, you can trace the provenance of the analysis by reviewing a directed graph showing each step of the analysis process. AIP Analyst's provenance view allows you to do the following:

* Trace how the agent arrived at its conclusions and check the logic of each step.
* Audit data transformations applied during analysis and ensure reproducibility of results.
* Verify that results are grounded in actual data rather than hallucinations. With AIP Analyst, you can see the Ontology data that is used at each step and ensure that all conclusions are based in reality.

![A sample AIP Analyst graph.](https://www.palantir.com/docs/resources/foundry/aip-analyst/aip-analyst-graph.png)

## Analysis outline

The analysis outline provides a structured summary of your session, displaying your questions alongside the agent's tool usage. Your messages appear with circle icons, while tool calls are marked with icons corresponding to their function.

You can use the outline to:

* Navigate quickly through prior analysis steps
* Review token usage for each tool call
* Hide specific tool results by clicking the eye icon that appears when hovering over outline items

![An AIP Analyst outline.](https://www.palantir.com/docs/resources/foundry/aip-analyst/aip-analyst-outline.png)
