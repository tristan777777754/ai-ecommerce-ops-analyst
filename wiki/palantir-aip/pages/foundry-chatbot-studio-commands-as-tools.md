---
title: "Tools > Use commands as tools in AIP Chatbot Studio"
source_url: "https://www.palantir.com/docs/foundry/chatbot-studio/commands-as-tools/"
scraped_at: "2026-05-16T03:02:37.251Z"
section: "AIP Chatbot Studio / Tools"
canonical_slug: "/foundry/chatbot-studio/commands-as-tools/"
---
# Use commands as tools in AIP Chatbot Studio

You can add [commands](https://www.palantir.com/docs/foundry/cross-app-interactivity/commands-overview/) as [tools to AIP chatbots](foundry-chatbot-studio-tools.md), enabling the chatbot to interact with and act on behalf of a user in Palantir applications. Commands run directly in the user's application, giving them access to the current application state and screen. This enables integrations that traditional backend tools struggle to support. For example, the chatbot can use commands to navigate the user interface, like setting the view to a specific location on a map.

:::callout{theme="success"}
You can also configure Workshop's [Button Group](https://www.palantir.com/docs/foundry/workshop/widgets-button-group/), [Metric Card](https://www.palantir.com/docs/foundry/workshop/widgets-metric-card/), and [App Pairing](https://www.palantir.com/docs/foundry/workshop/widgets-app-pairing/) widgets to trigger operations in any application that produces commands.
:::

## Add command tools to an AIP Chatbot

Chatbots can use commands as tools once an application declares and produces the command. To add commands as tools to a chatbot, select **Add tool > Commands** from the **Chatbot configuration** panel.

![The chatbot configuration panel displays the Tools section.](https://www.palantir.com/docs/resources/foundry/chatbot-studio/add-commands-tool-to-chatbot.png)

Search for and select one or multiple commands from the **Search commands...** modal. You can select a command multiple times if you need to [configure distinct prompts](#configure-command-tools-beta) for each instance of that command. Add the selected commands to your chatbot and apply configurations as needed.

:::callout{theme="neutral"}
AIP Chatbots that use commands as tools have a retention window that is automatically set to expire after 24 hours of inactivity.
:::

## Configure command tools \[Beta]

:::callout{theme="neutral"}
The ability to configure a command used as a chatbot tool is in the [beta](https://www.palantir.com/docs/foundry/platform-overview/development-life-cycle/) phase of development. Its supporting interface may change during active development. Contact Palantir Support with questions about configuring commands as tools in AIP Chatbot Studio.
:::

After you add one or multiple commands as tools to your chatbot, you can select a command to open a modal with additional configurations the chatbot uses to inform its actions. Select **Show more** to render additional documentation to help you learn more about each tool's optional configuration settings, such as its input parameters and expected behavior when invoked.

![The Render ephemeral feature command tool displays its additional configuration documentation.](https://www.palantir.com/docs/resources/foundry/chatbot-studio/configure-command-tool.png)

Review the sections below to learn more about additional configuration options.

### Additional descriptions

Provide command-specific context *in addition to* the default documentation made available to help the chatbot's backing model understand the action it will execute. While each command contains default documentation that helps the chatbot use it as a tool, you can provide more detail in **Additional documentation** to help the chatbot decide precisely *when* and *how* it should call the tool. As an example, you can instruct the **Remove all features** command to remove ephemeral features before drawing a new one if the existing features are not related to the new in a certain manner.

### Input parameters

Some commands accept input parameters when you configure them as a tool. Use **Input parameters** to set input values for command parameters, such as **Fill pattern** or **Stroke width** for the **Draw polygon** command.

By default, the chatbot determines the value of all required parameters based on your **Instructions** and the user's prompt. For optional parameters, the chatbot may optionally determine the value based on your **Instructions** and the user's prompt.

To override the default behavior, select **Add parameter override**, choose the parameter you want to override, and configure it using one of the following override options:

* **Chatbot decides (default):** The chatbot determines the value. This is the default behavior.
* **Preset values:** Hard-code a static value to consistently use the same value as an input parameter.
* **Application variable:** Use a preconfigured string or object set [variable](https://www.palantir.com/docs/foundry/workshop/concepts-variables/#variable-types).
* **Don't pass the parameter to chatbot:** Instruct the chatbot not to provide a value for an optional parameter. This option is available for optional parameters only.

### Asks for user approval before execution

Enabled by default, your chatbot will ask a user to review the command payload data and either **Reject** or **Approve** the command's action or output from their prompt before the command is executed. When disabled, your chatbot will execute commands based on a user's prompt without manual approval intervention.

![An AIP Chatbot prompts a user to Reject or Accept a command output.](https://www.palantir.com/docs/resources/foundry/chatbot-studio/auto-run.png)

## Test an AIP Chatbot's ability to use commands as tools

After you configure your commands in AIP Chatbot Studio, you can follow the instructions below to test your chatbot and validate its configurations *before* you [save and publish](foundry-chatbot-studio-getting-started.md#save-view-and-publish-an-aip-chatbot) to make it available in production applications:

1. In a separate browser window, open the application that produces your chatbot's command tool(s) and arrange it next to a window containing your chatbot in AIP Chatbot Studio.
2. Select **Choose an app to pair with... > Pair** for the application launched in the separate browser window, such as a Gaia map.

![A user pairs their chatbot with a Gaia map.](https://www.palantir.com/docs/resources/foundry/chatbot-studio/pair-agent-with-map.png)

3. Enter prompts in your chatbot's chat input window to test its ability to use the commands you added as tools.

Once you are satisfied with your chatbot's configurations, publish the chatbot for use as an assistant embedded in AIP Assist or through Workshop within the [AIP Chatbot](https://www.palantir.com/docs/foundry/workshop/widgets-aip-chatbot/) widget.

:::callout{theme="neutral"}
A chatbot will ignore commands as tools if you [publish it as a function](foundry-chatbot-studio-chatbots-as-functions.md) and execute it from an environment that does not support commands, such as configuring it to run within an automation built in [Automate](https://www.palantir.com/docs/foundry/automate/overview/). Contact Palantir Support with questions about your environment.
:::

## Pair your chatbot with multiple applications

Through App Pairing, your chatbot will automatically discover other applications you have open in your browser. To pair your chatbot with multiple application instances, select **Add** next to the **Discovered** application to create a pairing **Group**.

![The App Pairing pop-up shows multiple Gaia maps a user can pair.](https://www.palantir.com/docs/resources/foundry/chatbot-studio/pair-with-multiple-applications.png)

If your chatbot is not paired with an application to execute a command, then it will prompt the user to select an application to pair.

## Embed your chatbot in AIP Assist or Workshop

While you can use AIP Chatbot Studio with your paired application to test your chatbot's performance, you should embed the chatbot in a Workshop module or AIP Assist panel for a streamlined user experience. In both cases, the chatbot will automatically pair to the application with which it interacts.

### Publish your chatbot to AIP Assist

To make your chatbot accessible to AIP Assist, choose the rocket icon on the left side of your screen in AIP Chatbot Studio to launch the **Usage** panel before selecting the **AIP Assist** toggle. Next, select **Publish** on the top right of your screen. This will deploy the latest published chatbot version to AIP Assist, after which you will be able to select it from the **Chat with an AIP Chatbot** menu in an AIP Assist chat panel.

![A user toggles on AIP Assist in AIP Chatbot Studio before selecting their chatbot in an AIP Assist chat panel.](https://www.palantir.com/docs/resources/foundry/chatbot-studio/access-agent-in-aip-assist.png)

Once you select the chatbot, AIP Assist will automatically pair with the target application, and all relevant commands configured as tools will target the application. If your chatbot contains tools for multiple applications but is *not* paired with those applications, then AIP Assist will prompt you to choose an application to pair in one of your open browser tabs.

### Add your chatbot to Workshop

Use Workshop's [AIP Chatbot](https://www.palantir.com/docs/foundry/workshop/widgets-aip-chatbot/) widget to embed your chatbot in a module, where you can also use the [Iframe](https://www.palantir.com/docs/foundry/workshop/widgets-iframe/) widget to embed one or more applications within [sections](https://www.palantir.com/docs/foundry/workshop/concepts-layouts/#sections) adjacent to the AIP Chatbot widget. An AIP Chatbot widget and an iframe-embedded application in a Workshop module will automatically pair, and all relevant commands you configure as tools will target the iframe-embedded application.
