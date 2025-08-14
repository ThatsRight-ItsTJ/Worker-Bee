# Pollinations AI Integration for OpenOperator

This directory contains the Pollinations AI integration tools for OpenOperator, providing free, OpenAI-compatible vision and text generation capabilities.

## Features

- **Zero Cost**: Free vision and text APIs with no signup required
- **OpenAI Compatible**: Drop-in replacement for OpenAI Vision API
- **No Rate Limits**: Unlimited usage for vision-heavy workflows
- **Multiple Models**: Access to various vision models (OpenAI, Gemini, Sur AI)

## Tools

### PollinationsVisionTool

Analyzes screenshots and images to understand web page content, UI elements, forms, buttons, text, and layout.

**Usage:**
```python
from openoperator.tools.pollinations.vision_tool import PollinationsVisionTool

vision_tool = PollinationsVisionTool()
result = vision_tool._run(
    image_path="screenshot.png",
    query="What interactive elements are visible on this page?",
    model="openai"
)
```

### PollinationsTextTool

Generates text responses using Pollinations AI models for reasoning, planning, or generating responses.

**Usage:**
```python
from openoperator.tools.pollinations.text_tool import PollinationsTextTool

text_tool = PollinationsTextTool()
result = text_tool._run(
    prompt="Explain how to navigate this webpage",
    model="openai",
    system_prompt="You are a helpful web automation assistant."
)
```

## Model Options

- **openai**: Best overall performance, GPT-4 equivalent
- **sur**: Sur AI Assistant (Mistral-based), supports text and image
- **gemini**: Gemini 2.5 Flash Preview, fast and capable
- **deepseek**: DeepSeek-V3 for specialized tasks

## Integration

The tools are automatically integrated into the OpenOperator agent workflow and are available as LangChain tools. They can be called by the agent during web automation tasks.

## Testing

Run the test script to verify the integration:

```bash
python test_pollinations_integration.py
```

## Error Handling

The tools include built-in error handling and will return descriptive error messages if API calls fail. For production use, consider implement the retry logic from `openoperator.utils.pollinations_helpers.safe_vision_call()`.