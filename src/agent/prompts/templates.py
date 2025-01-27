CONCLUSIONS_TEMPLATE = """Here are my conclusions about the results of my previous actions:

A few thoughts about what's going on: {current_situation}

Here is my analysis of the situation: {analysis}

Here are my next steps: {next_steps}

Here are the tools I will need to call: {tools_to_call}

I have enough thoughts to avoid calling "Think" tool, and start executing other tools.
"""

LOG_MESSAGE_TEMPLATE = """
Action record:

> You visited page "{title}" at "{url}".

> Description of the page: {browser_state_description}

> Useful information found: {relevant_data}

"""

PUNISHMENT_MESSAGE_TEMPLATE = """
<punishment_message>
System prompt violation detected. Please, use tools. Messages without toolcalls might lead to your termination.
</punishment_message>
"""

USER_INPUT_TEMPLATE = """
I'm looking for the following information:
{query}

The URL of the website I'm looking for information on:
{url}
"""