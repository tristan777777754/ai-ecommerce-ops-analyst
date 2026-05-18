---
title: "AIP Chatbot Studio > Core concepts"
source_url: "https://www.palantir.com/docs/foundry/chatbot-studio/core-concepts/"
scraped_at: "2026-05-16T03:02:37.251Z"
section: "AIP Chatbot Studio"
canonical_slug: "/foundry/chatbot-studio/core-concepts/"
---
# Core concepts

The following core concepts are essential to understanding and getting the most out of AIP Chatbot Studio (previously known as AIP Agent Studio). You can learn more about applying these concepts in the [Getting started](foundry-chatbot-studio-getting-started.md) tutorial.

## AIP Chatbots

AIP Chatbots (previously known as AIP Agents) are interactive assistants equipped with enterprise-specific information and tools.

## Application state

The [**application state**](foundry-chatbot-studio-application-state.md), previously known as *parameters*, are application variables within prompts that customize and control the LLM's behavior. They allow for dynamic input and can be adjusted based on the task requirements.

## Instructions and descriptions

Instructions, tool descriptions, and variable descriptions are compiled into the raw system prompt for the LLM. This teaches the LLM how to complete a task using the available context.

For the instructions, begin with the most important information, such as an overview of the task. Follow this with the necessary data and guidance on using the [application state](#application-state) and [tools](#tools).

For each tool and variable description, provide the LLM with concrete steps on how and when to use that specific piece of context. Keep in mind that an LLM only has access to the information you explicitly provide.

## Retrieval-augmented generation (RAG)

Retrieval-augmented generation leverages external data sources to provide the LLM with relevant information dynamically. This method enhances the LLM's responses by ensuring they are based on the most current and contextually appropriate data.

## Retrieval context

Retrieval context refers to the specific information retrieved in response to each message, which is used to generate a response. The process is as follows:

1. User sends a new message.
2. Based on the user's message, fetch relevant content from configured data sources.
3. Include the relevant content along with the user's message to the LLM.

For more details, review the [retrieval context](foundry-chatbot-studio-retrieval-context.md) documentation.

## Tools

[Tools](foundry-chatbot-studio-tools.md) are external functionalities or APIs that the LLM can use to perform specific actions or retrieve information beyond its base capabilities.

For more details, review the [tools](foundry-chatbot-studio-tools.md) documentation.

## Vector embeddings

Embeddings are numerical representations of text that capture semantic meaning. They are used to compare and retrieve similar pieces of text efficiently. In AIP Chatbot Studio, embeddings help identify relevant documents and context to provide accurate responses.

## Context window

The context window refers to the amount of text (usually measured in tokens) that an LLM can process at one time. In AIP Chatbot Studio, the context window includes the system prompt, conversation history, and the information injected to assist the LLM (including retrieval context, application state, and tools). Exceeding the context window will result in an error, prompting users to create a new session to continue their interaction.

## Chatbots as Functions

Chatbots can be published as [Functions](https://www.palantir.com/docs/foundry/functions/overview/), which allows them to be used anywhere in the platform where Functions can be executed. For example, builders can publish AIP Chatbots as Functions to evaluate them in [AIP Evals](foundry-aip-evals-overview.md), to automate chatbot workflows with [Automate](https://www.palantir.com/docs/foundry/automate/overview/), or to use chatbots in [Code Repositories](https://www.palantir.com/docs/foundry/code-repositories/overview/). For more information, refer to the [chatbots as Functions](foundry-chatbot-studio-chatbots-as-functions.md) documentation.
