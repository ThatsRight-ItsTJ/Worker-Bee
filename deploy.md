# OpenOperator Deployment Guide

## 🚀 Bolt Hosting Deployment (Recommended)

### Prerequisites
1. Ensure your `.env` file is configured with your AI model settings
2. Test the application locally first: `python start_ui.py`

### Deployment Steps

1. **Push to Bolt:**
   ```bash
   # Your code is ready for Bolt deployment!
   # Just deploy directly from this directory
   ```

2. **Set Environment Variables in Bolt:**
   - `MODEL=gpt-4o` (or your preferred model)
   - `MODEL_PROVIDER=azure` (or openai, pollinations, etc.)
   - `AZURE_OPENAI_API_KEY=your_key_here`
   - `AZURE_OPENAI_ENDPOINT=your_endpoint_here`
   - `POLLINATIONS_REFERRER=openoperator-v1`
   - `BROWSER_USE_LOGGING_LEVEL=info`

3. **Bolt will automatically:**
   - Install Python dependencies
   - Install Node.js dependencies
   - Install Playwright browsers
   - Build the React frontend
   - Start the Flask backend
   - Handle routing between frontend and API

### Configuration Files Added:
- `bolt.config.js` - Bolt-specific configuration
- `package.json` - Root package file for Bolt
- `Dockerfile` - Container configuration
- Updated `backend_server.py` - Production-ready server

## 🌐 Alternative Deployment Options

### Netlify (Frontend Only)
- Use `netlify.toml` configuration
- Deploy frontend only, backend needs separate hosting

### Vercel (Full-Stack)
- Use `vercel.json` configuration
- Supports both frontend and Python backend

### Heroku
- Use `Procfile` and `runtime.txt`
- Set environment variables in Heroku dashboard

### Docker
- Use the provided `Dockerfile`
- Build: `docker build -t openoperator .`
- Run: `docker run -p 5000:5000 openoperator`

## 🔧 Environment Variables Required

### Required:
- `MODEL` - AI model name
- `MODEL_PROVIDER` - Provider (azure, openai, pollinations, etc.)

### Provider-Specific:
- **Azure OpenAI:** `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`
- **OpenAI:** `OPENAI_API_KEY`
- **Anthropic:** `ANTHROPIC_API_KEY`
- **Pollinations:** `POLLINATIONS_API_KEY` (optional)

### Optional:
- `LANGCHAIN_TRACING_V2=true`
- `LANGCHAIN_API_KEY`
- `LANGCHAIN_PROJECT=openoperator`
- `BROWSER_USE_LOGGING_LEVEL=info`

## 🎯 Post-Deployment

1. **Test the deployment:**
   - Visit your deployed URL
   - Try the example queries
   - Check that both frontend and API are working

2. **Monitor logs:**
   - Check for any Playwright installation issues
   - Verify AI model connections
   - Monitor response times

3. **Custom Domain (Optional):**
   - Configure your custom domain in Bolt
   - Update CORS settings if needed

## 🐛 Troubleshooting

### Common Issues:
1. **Playwright not working:** Ensure system dependencies are installed
2. **AI model errors:** Check API keys and endpoints
3. **CORS issues:** Verify frontend/backend URLs match
4. **Timeout errors:** Increase timeout settings for long-running tasks

### Debug Mode:
Set `BROWSER_USE_LOGGING_LEVEL=debug` for detailed logs.