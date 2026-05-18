---
title: "AIP Chatbot Studio > Overview"
source_url: "https://www.palantir.com/docs/foundry/chatbot-studio/overview/"
scraped_at: "2026-05-16T03:02:37.251Z"
section: "AIP Chatbot Studio"
canonical_slug: "/foundry/chatbot-studio/overview/"
---
# AIP Chatbot Studio

:::callout{theme="informational"}
AIP Chatbot Studio was previously known as AIP Agent Studio, and AIP Chatbots were previously known as AIP Agents.
:::

**AIP Chatbot Studio** allows users to build interactive assistants, known as AIP Chatbots, that are equipped with enterprise-specific information and tools, deployable internally in the platform and externally through the [Ontology SDK](https://www.palantir.com/docs/foundry/ontology-sdk/overview/) and [platform APIs](https://www.palantir.com/docs/foundry/api/aip-agents-v2-resources/agents/agent-basics/).

Chatbots built in AIP Chatbot Studio are powered by large language models (LLMs), the Ontology, documents, and custom tools. AIP Chatbots can be integrated into applications to facilitate dynamic, context-aware read and write workflows that enable you to automate tasks and reduce manual application interactions.

The following example shows an AIP Chatbot that uses an application variable to take a filtered object set of video transcripts as context when answering user questions about the recent press conference from the Federal Reserve.

![A screenshot of AIP Chatbot Studio edit page with the AIP Chatbot described above.](https://www.palantir.com/docs/resources/foundry/chatbot-studio/agent-studio-edit-view.png)

The above AIP Chatbot can also be deployed in a [Workshop application](https://www.palantir.com/docs/foundry/workshop/widgets-aip-chatbot/) that enables users to interact with the selected video.

![A screenshot of the AIP Chatbot described above deployed in a Workshop application.](https://www.palantir.com/docs/resources/foundry/chatbot-studio/workshop-agent.png)

AIP Chatbot Studio is built on the same rigorous [security](https://www.palantir.com/docs/foundry/security/overview/) model that governs the rest of the Palantir platform. These platform security controls grant an LLM access only to what is necessary to complete a task.
