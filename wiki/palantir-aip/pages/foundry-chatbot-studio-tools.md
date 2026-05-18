---
title: "Tools > Overview"
source_url: "https://www.palantir.com/docs/foundry/chatbot-studio/tools/"
scraped_at: "2026-05-16T03:02:37.251Z"
section: "AIP Chatbot Studio / Tools"
canonical_slug: "/foundry/chatbot-studio/tools/"
---
# Tools

Tools are external functionalities or APIs that can be used by a large language model (LLM) to perform specific actions or retrieve information beyond its inherent capabilities. Tools are especially useful for allowing the LLM to determine control flow and construct inputs.

![A screenshot of edit mode in AIP Chatbot Studio, with a chatbot configured with an Action, the Object Query tool, and an Ontology Semantic Search tool.](https://www.palantir.com/docs/resources/foundry/chatbot-studio/tools-demo.png)

## Types of tools

There are six types of tools available:

* **Action:** Gives your chatbot the ability to execute an ontology edit. This can be configured to run automatically or to run after confirmation from the user.
* **Object query:** This tool specifies the object types that the LLM can access. You can add multiple object types and specify accessible properties to make queries more token-efficient. The object query tool supports filtering, aggregation, inspection, and traversal of links for configured objects.
* **Function:** This allows the LLM to call any [Foundry function](https://www.palantir.com/docs/foundry/functions/overview/), including published [AIP Logic](foundry-logic-overview.md) functions. The latest version of the function is automatically used, but you can also specify a published version for more granular control.
* **Update application variable:** This tool is used to update the value of an application variable configured in the [Application state](foundry-chatbot-studio-application-state.md#update-application-variables-with-chatbots) tab.
* **Command:** These tools enable your chatbot to trigger operations in other Palantir applications using one or multiple [commands](foundry-chatbot-studio-commands-as-tools.md).
* **Request clarification:** This tool allows the chatbot to pause its execution and request clarification from the user.
* **(Legacy) Ontology semantic search:** This tool can use a vector property to retrieve relevant Ontology context. This tool is legacy and does not include citations or input/output variables, and it does not return the resulting object set to the LLM. We recommend using [Ontology context](foundry-chatbot-studio-retrieval-context.md#ontology-context) instead.

## Tool mode

Use the tool mode setting to control how configured tools are provided to the LLM, and how the LLM is able to call these tools. The available tool mode settings are:

* **Prompted tool calling:** This mode inserts instructions into the prompt to provide tools and allows the LLM to use these tools. Chatbots in this tool mode can only call a single tool at a time, so they may take longer to answer complex queries that require multiple tool calls. This mode is supported for all tool types and all [available models](foundry-chatbot-studio-getting-started.md#choose-a-large-language-model-llm).
* **Native tool calling:** This mode uses the built-in capabilities of supported models to provide tools and allow the LLM to call these tools directly. This offers improved speed and performance over prompted tool calling, due to greater token efficiency and the ability for chatbots in this mode to call multiple tools in parallel. This mode can currently only be used with a subset of Palantir-provided models and with the following tool types: actions, object query, function, and update application variable. If you require use of a model or tool type not supported by native tool calling mode, use prompted tool calling mode instead.

![Tool mode selection in edit mode in AIP Chatbot Studio, with prompted tool calling and native tool calling modes available for selection.](https://www.palantir.com/docs/resources/foundry/chatbot-studio/chatbot-studio-tool-mode-setting.png)

## View reasoning

When deployed in edit mode, view mode, Workshop, or AIP Threads, you can select **View reasoning** below a response to investigate the LLM reasoning process used to generate the response.

![Edit mode in AIP Chatbot Studio, with the LLM reasoning for the given response displayed to the right.](https://www.palantir.com/docs/resources/foundry/chatbot-studio/inspect-reasoning.png)
