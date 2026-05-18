---
title: "AIP Chatbot Studio > Distribute AIP Chatbots using Marketplace"
source_url: "https://www.palantir.com/docs/foundry/chatbot-studio/marketplace/"
scraped_at: "2026-05-16T03:02:37.251Z"
section: "AIP Chatbot Studio"
canonical_slug: "/foundry/chatbot-studio/marketplace/"
---
# Distribute AIP Chatbots using Marketplace

Use [Foundry DevOps](https://www.palantir.com/docs/foundry/devops/overview/) to include your AIP Chatbots in [Marketplace products](https://www.palantir.com/docs/foundry/devops/core-concepts/#product) for other users to install and reuse. [Learn how to create your first product.](https://www.palantir.com/docs/foundry/foundry-devops/create-products/)

## Supported features

All AIP Chatbots features are supported by Marketplace products, with the exception of:

* [Assist agents](foundry-assist-agents-in-aip-assist.md)

## Adding AIP Chatbots to Marketplace products

To add an AIP Chatbot to a product, first [create a product](https://www.palantir.com/docs/foundry/foundry-devops/create-products/). In the **Add resources** step, search for and select your AIP Chatbot from the **Add files** option.

Alternatively, if you have a [Workshop application](https://www.palantir.com/docs/foundry/workshop/overview/) that embeds an AIP Chatbot via the [AIP Chatbot widget](https://www.palantir.com/docs/foundry/workshop/widgets-aip-chatbot/), you can add the Workshop module to the product and the AIP Chatbot will be included automatically.

## AIP Chatbots with document context

When packaging an AIP Chatbot that is configured to use [document context retrieval](foundry-chatbot-studio-retrieval-context.md#document-context), the [media set](https://www.palantir.com/docs/foundry/data-integration/media-sets/) containing the documents will automatically be included in the product. This ensures that the AIP Chatbot has access to the necessary documents when installed.

:::callout{theme="warning" title="Media set content"}
The entire media set, including any items not used by the AIP Chatbot, will be packaged in the product. If you want to limit the content to only the documents used by the AIP Chatbot, you should create a new media set containing only the necessary documents and reconfigure the AIP Chatbot to use it.
:::
