export default {
  // Build configuration
  build: {
    command: "npm run build",
    output: "openoperator-ui/dist"
  },
  
  // Development configuration
  dev: {
    command: "cd openoperator-ui && npm run dev",
    port: 5173,
    env: {
      NODE_ENV: "development"
    }
  },
  
  // Environment variables that should be available
  env: {
    // Required environment variables
    MODEL: {
      description: "AI model to use (e.g., gpt-4o)",
      required: true
    },
    MODEL_PROVIDER: {
      description: "AI model provider (e.g., azure, openai, pollinations)",
      required: true
    },
    
    // Optional environment variables
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
    POLLINATIONS_API_KEY: {
      description: "Pollinations API key (optional)",
      required: false
    },
    POLLINATIONS_REFERRER: {
      description: "Pollinations referrer",
      default: "openoperator-v1"
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
      default: "openoperator"
    },
    BROWSER_USE_LOGGING_LEVEL: {
      description: "Logging level",
      default: "info"
    }
  },
  
  // Deployment settings
  deploy: {
    // Health check endpoint
    healthCheck: "/api/health",
    
    // Startup timeout (web automation can take time to initialize)
    timeout: 300,
    
    // Memory and CPU requirements
    resources: {
      memory: "1GB",
      cpu: "1"
    }
  }
}