export default {
  // Build configuration
  build: {
    command: "python -m pip install --no-cache-dir -r requirements.txt && python -m playwright install chromium && python -m playwright install-deps && cd openoperator-ui && npm install && npm run build",
    output: "openoperator-ui/dist",
    env: {
      PYTHONPATH: "/app",
      NODE_ENV: "production"
    }
  },
  
  // Development configuration
  dev: {
    command: "python backend_server.py",
    port: 5000,
    env: {
      NODE_ENV: "development"
    }
  },
  
  // Environment variables that should be available
  env: {
    // Required environment variables
    MODEL: {
      description: "AI model to use (e.g., openai, gemini, sur, deepseek)",
      default: "openai"
    },
    MODEL_PROVIDER: {
      description: "AI model provider (pollinations recommended for free usage)",
      default: "pollinations"
    },
    
    // Pollinations configuration (recommended)
    POLLINATIONS_REFERRER: {
      description: "Pollinations referrer for authentication",
      default: "worker-bee-bolt-v1"
    },
    
    // Alternative providers (optional)
    AZURE_OPENAI_API_KEY: {
      description: "Azure OpenAI API key",
      required: false
    },
    AZURE_OPENAI_ENDPOINT: {
      description: "Azure OpenAI endpoint",
      required: false
    },
    OPENAI_API_KEY: {
      description: "OpenAI API key",
      required: false
    },
    ANTHROPIC_API_KEY: {
      description: "Anthropic API key",
      required: false
    },
    GROQ_API_KEY: {
      description: "Groq API key for fast inference",
      required: false
    },
    POLLINATIONS_API_KEY: {
      description: "Pollinations API key (optional)",
      required: false
    },
    LANGCHAIN_TRACING_V2: {
      description: "Enable LangChain tracing",
      default: "false"
    },
    LANGCHAIN_API_KEY: {
      description: "LangChain API key for tracing",
      required: false
    },
    LANGCHAIN_PROJECT: {
      description: "LangChain project name",
      default: "worker-bee"
    },
    BROWSER_USE_LOGGING_LEVEL: {
      description: "Logging level",
      default: "info"
    },
    PORT: {
      description: "Server port",
      default: "5000"
    },
    HOST: {
      description: "Server host",
      default: "0.0.0.0"
    }
  },
  
  // Deployment settings
  deploy: {
    // Health check endpoint
    healthCheck: "/api/health",
    
    // Startup timeout (web automation can take time to initialize)
    timeout: 600,
    
    // Memory and CPU requirements
    resources: {
      memory: "2GB",
      cpu: "2"
    }
  }
}