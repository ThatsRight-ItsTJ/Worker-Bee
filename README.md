# OpenOperator - Open-Source LLM Agent for Web Operations in Browser

**OpenOperator** is an LLM agent that uses web browser to complete tasks, originally based on [BrowserUse](https://github.com/browser-use/browser-use). This fork is mainly focused on moving the agent backend to [LangGraph](https://github.com/langgraph/langgraph) and [LangChain](https://github.com/langchain/langchain).

## Key Features

1. **Vision-Based Navigation**: The agent fully relies on vision inputs to navigate web pages. Vision-first approach gives predictable results even with JS-heavy websites.

2. **File Handling**: Introduced file handling capabilities, currently supporting PDF files. With vision-driven reasoning, the agent uses universal workflow to access and read data with any layout.

3. **Use with your favorite LLM**: Supports any LLM that can handle tool calling and multimodal inputs.

## Changes from [BrowserUse](https://github.com/browser-use/browser-use)

1. **Refactored Agent Backbone**: Transitioned from vanilla Python to [LangGraph](https://github.com/langgraph/langgraph) and [LangChain](https://github.com/langchain/langchain).

2. **Moved to Full-Page Viewport**: Implements full-page screenshots to minimize the need for scrolling tools.

4. **Added File Handling**: Currently supports only PDF, but adding handlers is easy.

5. **Adjustable Focus**: Agent architecture lets you adjust prompts for task categories (i.e. "shopping", "searching", "applying", etc.). Current version is focused on finding answers on given websites, generalist mode is coming soon.

## Why LangGraph and LangChain?

Some developers say LangChain introduces unnecessary abstractions that add complexity to the project. However, each LLM-driven project that is built in vanilla Python eventually brings the same abstractions. It all starts with "Well, I'll just add this tiny little object to handle messages," and then you end up with some hardcore system design.

LangGraph was picked as a backbone for this fork because:
- It scales well. LangGraph is really good at parallelizing tasks and completely solves race condition problems.
- The LangGraph Server is a really good way to deploy your agent both for users and as a subagent for other LLM agents.
- They have a huge community, they ship fast, and their documentation is good.

## Prerequisites
- LLM API compatible with LangChain
- LangSmith account if you want observability (free for small projects)

## Installation

1. Clone the repository
2. Install Playwright
3. Create a `.env` file based on the provided `.env.example`, setting necessary configurations like API keys, model parameters, etc.

## Usage

The current usage is limited to a single URL and a single data extraction task. However, all other tools are available to the agent, and just require you to modify the prompt and graph.

After installation, you can start using OpenOperator by running the main agent script:

```bash
uv run src/main.py --url <URL> --query <QUERY>
```

This will initialize the agent, set up the browser context, and begin the workflow to extract data from specified websites.

## Acknowledgements

This project is a fork of [BrowserUse](https://github.com/browser-use/browser-use). It is a great project, and I'm grateful for the work done by the original authors. I hope this fork will help the original project with inspiration, ideas, and adoption.

Playwright and Chromium are a killer combination for web automation.

LangGraph and LangChain are a great way to build LLM agents.

LangSmith is a great way to observability.

MyPyPDF2 is a great way to handle PDF files.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements.

## License

This project is licensed under the [MIT License](LICENSE).
