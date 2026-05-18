---
title: "AIP Evals > Use intermediate parameters to evaluate block output"
source_url: "https://www.palantir.com/docs/foundry/aip-evals/intermediate-parameters/"
scraped_at: "2026-05-16T03:02:37.251Z"
section: "AIP Evals"
canonical_slug: "/foundry/aip-evals/intermediate-parameters/"
---
# Use intermediate parameters to evaluate block output

LLM-backed functionality often includes multiple complex operations, and only evaluating the end result may be insufficient to determine prompt performance.

With AIP Logic and AIP Evals you can set up intermediate parameters for evaluation. Similar to final function outputs, intermediate outputs can be used for setting up automated [evaluators](foundry-aip-evals-create-suite.md#evaluators), or to simply look at the results. Intermediate parameter output values will be included in the evaluation suite [results dataset](foundry-aip-evals-results-dataset.md) should one be set up.

## Set up intermediate parameters

To set up intermediate parameters for evaluation, follow these steps:

1. Select the flask icon on an AIP Logic block to expose the output as intermediate parameter.
2. Select the new intermediate parameter in the evaluator configuration panel to evaluate the output.

![Set up intermediate parameters for evaluation.](https://www.palantir.com/docs/resources/foundry/aip-evals/aip-evals-set-up-intermediate-parameters.png)
