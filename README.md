# Worker-Bee 🐝

A powerful web automation agent that combines browser automation with AI-powered vision and text generation capabilities. Worker-Bee can navigate websites, analyze visual content, and perform complex web tasks using multiple AI models.

## Features

- 🤖 **AI-Powered Web Automation** - Intelligent browser control with natural language commands
- 👁️ **Free Vision Analysis** - Analyze screenshots and web content using Pollinations AI (no OpenAI costs!)
- 📝 **Multi-Model Text Generation** - Support for OpenAI, Gemini, Sur AI, and DeepSeek models
- 🔄 **LangChain Integration** - Built on LangChain/LangGraph for robust AI workflows
- 💰 **Cost-Effective** - Free alternatives to expensive OpenAI Vision API calls
- 🚫 **No Rate Limits** - Unlimited usage with Pollinations AI
- 🛠️ **Extensible** - Easy to add new tools and capabilities

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js (for browser automation)
- Git

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/ThatsRight-ItsTJ/Worker-Bee.git
cd Worker-Bee
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
```

4. **Configure your `.env` file:**
```env
# Required: Your AI model configuration
MODEL=gpt-4o
MODEL_PROVIDER=azure  # or openai, anthropic, etc.
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=your_endpoint_here

# Optional: Pollinations AI (for free vision and text)
POLLINATIONS_API_KEY=your_pollinations_key  # Optional
POLLINATIONS_REFERRER=worker-bee-v1

# Optional: LangChain tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langchain_key
LANGCHAIN_PROJECT=worker-bee

# Logging level
BROWSER_USE_LOGGING_LEVEL=info
```

## Setup Instructions

### Setting up Pollinations AI (Free Vision & Text)

1. **Get a Pollinations API key** (optional but recommended):
   - Visit [Pollinations AI](https://pollinations.ai/)
   - Sign up for an account
   - Generate an API key
   - Add it to your `.env` file as `POLLINATIONS_API_KEY`

2. **Pollinations provides:**
   - Free image analysis and vision capabilities
   - Multiple AI models (OpenAI, Gemini, Sur AI, DeepSeek)
   - No rate limits
   - Cost-effective alternative to OpenAI Vision API

### Setting up LangChain (Optional Tracing)

1. **Create a LangChain account:**
   - Visit [LangSmith](https://smith.langchain.com/)
   - Sign up for an account
   - Create a new project
   - Get your API key

2. **Add to your `.env` file:**
```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langchain_key
LANGCHAIN_PROJECT=your_project_name
```

3. **Benefits of LangChain tracing:**
   - Monitor AI agent performance
   - Debug complex workflows
   - Track token usage and costs
   - Analyze conversation flows

## Usage

### Basic Web Automation

```python
from openoperator import OpenOperator

# Initialize the agent
agent = OpenOperator()

# Perform web automation tasks
result = agent.run("Navigate to example.com and take a screenshot")
print(result)
```

### Using Vision Analysis

```python
from openoperator.tools.pollinations import PollinationsVisionTool

# Initialize vision tool
vision_tool = PollinationsVisionTool()

# Analyze an image
result = vision_tool._run(
    image_url="/images/image.jpg",
    query="What do you see in this image?"
)
print(result)
```

### Using Text Generation

```python
from openoperator.tools.pollinations import PollinationsTextTool

# Initialize text tool
text_tool = PollinationsTextTool()

# Generate text
result = text_tool._run(
    prompt="Write a summary of web automation benefits",
    model="openai"  # or "gemini", "sur-ai", "deepseek"
)
print(result)
```

### Advanced Usage with Custom Workflows

```python
from openoperator.examples.pollinations_integration_example import run_example

# Run the comprehensive example
await run_example()
```

## Testing

Run the integration test to verify everything is working:

```bash
python test_pollinations_integration.py
```

This will test:
- Pollinations vision analysis
- Text generation capabilities
- Error handling
- Multiple AI model support

## Project Structure

```
Worker-Bee/
├── openoperator/
│   ├── agent/              # Core agent logic
│   ├── tools/
│   │   └── pollinations/   # Pollinations AI tools
│   ├── utils/              # Helper utilities
│   └── examples/           # Usage examples
├── tests/                  # Test files
├── .env.example           # Environment template
└── README.md              # This file
```

## Key Components

- **PollinationsVisionTool**: Free image analysis and visual understanding
- **PollinationsTextTool**: Multi-model text generation
- **Vision Queries**: Predefined templates for common vision tasks
- **Helper Utilities**: Retry logic and error handling for API calls

## Cost Savings

Worker-Bee can significantly reduce your AI automation costs:

- **OpenAI Vision API**: ~$0.00765 per image
- **Pollinations Vision**: FREE
- **Estimated savings**: 100% on vision-related tasks

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Troubleshooting

### Common Issues

1. **Authentication errors**: Check your API keys in `.env`
2. **Browser automation fails**: Ensure Node.js is installed
3. **Vision analysis errors**: Verify Pollinations API key (optional) or check internet connection
4. **Model not responding**: Verify your MODEL_PROVIDER configuration

### Getting Help

- Check the [examples](openoperator/examples/) directory
- Run the test script: `python test_pollinations_integration.py`
- Review error logs with `BROWSER_USE_LOGGING_LEVEL=debug`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **Fork of OpenOperator by NickSherrow** - Original LangChain implementation
- **Pollinations AI** - Free vision and text generation capabilities
- **LangChain** - AI workflow orchestration framework
- **Browser Use** - Original browser automation foundation

This project is a fork of [BrowserUse](https://github.com/browser-use/browser-use). It is a great project, and I'm grateful for the work done by the original authors. I hope this fork will help the original project with inspiration, ideas, and adoption.

Playwright and Chromium are a killer combination for web automation.

LangGraph and LangChain are a great way to build LLM agents.

LangSmith is a great way to observability.

MyPyPDF2 is a great way to handle PDF files.

---

Made with ❤️ for the open source community. Star ⭐ this repo if you find it useful!
