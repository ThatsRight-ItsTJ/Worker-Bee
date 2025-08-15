# 🚀 Worker Bee Deployment Guide

## Quick Deploy to Bolt Hosting

Worker Bee is optimized for Bolt Hosting with zero-configuration deployment.

### 1. One-Click Deploy

Simply push your code to Bolt - everything is pre-configured!

```bash
# Your project is ready to deploy
# Just connect to Bolt and deploy
```

### 2. Environment Variables

Set these in your Bolt dashboard:

#### Recommended (Free Option):
```env
MODEL_PROVIDER=pollinations
MODEL=openai
POLLINATIONS_REFERRER=worker-bee-bolt-v1
```

#### Optional (Enhanced Features):
```env
POLLINATIONS_API_KEY=your_pollinations_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langchain_key
BROWSER_USE_LOGGING_LEVEL=info
```

### 3. Alternative AI Providers

If you prefer other providers, use these configurations:

#### Azure OpenAI:
```env
MODEL_PROVIDER=azure
MODEL=gpt-4o
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
```

#### OpenAI:
```env
MODEL_PROVIDER=openai
MODEL=gpt-4o
OPENAI_API_KEY=your_openai_key
```

#### Groq (Fast & Often Free):
```env
MODEL_PROVIDER=groq
MODEL=llama-3.1-70b-versatile
GROQ_API_KEY=your_groq_key
```

## What Bolt Handles Automatically

✅ **Python Environment**: Installs all dependencies from requirements.txt
✅ **Playwright Setup**: Installs Chromium browser and system dependencies  
✅ **Frontend Build**: Compiles React UI and serves static files
✅ **Production Server**: Runs Flask backend with proper routing
✅ **SSL & Domains**: Handles HTTPS and custom domain setup
✅ **Health Checks**: Monitors `/api/health` endpoint
✅ **Auto-scaling**: Adjusts resources based on usage

## Post-Deployment Testing

Once deployed, test your Worker Bee instance:

1. **Visit your Bolt URL** - should show the Worker Bee UI
2. **Try the health check**: `https://your-app.bolt.new/api/health`
3. **Test automation**: Use the web interface to analyze a simple website

## Troubleshooting

### Common Issues:

**Build Failures:**
- Check that all environment variables are set
- Verify Python dependencies in requirements.txt
- Ensure Playwright installation completed

**Runtime Errors:**
- Check logs in Bolt dashboard
- Verify AI provider credentials
- Test with simple URLs first (like example.com)

**Performance Issues:**
- Consider upgrading to higher memory/CPU in Bolt
- Use Pollinations for free, unlimited vision analysis
- Enable LangChain tracing to monitor performance

## Monitoring & Maintenance

- **Logs**: Available in Bolt dashboard
- **Health**: Monitor `/api/health` endpoint
- **Usage**: Track via LangChain tracing (optional)
- **Updates**: Push new code to auto-deploy

## Cost Optimization

Worker Bee is designed to be cost-effective:

- **Free Vision**: Uses Pollinations AI (no OpenAI Vision costs)
- **Efficient**: Only uses resources when actively processing
- **Scalable**: Bolt handles scaling automatically
- **No Rate Limits**: Unlimited usage with Pollinations

---

🐝 **Ready to deploy?** Just push to Bolt and start automating the web!