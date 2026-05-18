---
title: "AIP Evals > Overview"
source_url: "https://www.palantir.com/docs/foundry/aip-evals/overview/"
scraped_at: "2026-05-16T03:02:37.251Z"
section: "AIP Evals"
canonical_slug: "/foundry/aip-evals/overview/"
---
# AIP Evals

AIP Evals is a testing environment to evaluate the performance of your [AIP Logic functions](foundry-logic-overview.md), [AIP Chatbot functions](foundry-chatbot-studio-chatbots-as-functions.md), or [code-authored functions](https://www.palantir.com/docs/foundry/functions/overview/). It is specifically designed to help you deal with the non-deterministic nature of LLMs. AIP Evals allows you to create test cases, define evaluation functions to measure performance, and compare the results against previous versions of your function. It enables you to build the necessary confidence to put LLM-backed functions into production or make changes to an existing implementation.

You can use AIP Evals to:

* Create test cases and define evaluation criteria.
* Debug, iterate, and improve functions and prompts.
* Compare the performance of different models on your functions.
* Examine variance across multiple runs.

AIP Evals is also available as an integrated tool within [AI FDE](foundry-ai-fde-overview.md), allowing you to create and run evaluation suites through conversational commands.

![Evals overview](https://www.palantir.com/docs/resources/foundry/aip-evals/aip-evals-overview.png)

## Core concepts

**Evaluation suite:** The collection of test cases, target functions, and evaluation functions used to benchmark function performance.

**Target function:** The function being evaluated. A suite can be configured to test [multiple target functions](foundry-aip-evals-create-suite.md#additional-target-functions) simultaneously.

**Evaluation function:** The method used when comparing or evaluating the actual output of a target function against the expected output.

**Test cases:** Defined sets of inputs and expected outputs that are passed into evaluation functions during evaluation suite runs.

**Metrics:** The results of evaluation functions. Metrics are produced per test case and can be compared in aggregate or individually between runs.

To get started, create an [evaluation suite for logic functions](foundry-aip-evals-getting-started.md), or create an [evaluation suite for general functions](foundry-aip-evals-create-suite.md), and learn more about [evaluation run configurations](foundry-aip-evals-run-suite.md).
