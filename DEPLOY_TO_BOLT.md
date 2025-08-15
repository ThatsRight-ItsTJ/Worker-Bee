# 🚀 How to Deploy Worker Bee to Bolt Hosting

## You're Already in Bolt! 

Since you're working in this Bolt environment, your code is already here. Here's how to deploy it:

## Method 1: Deploy Current Project (Recommended)

If you're working in Bolt already, you can deploy directly:

1. **Click the Deploy Button** in the Bolt interface (usually in the top-right corner)
2. **Choose your deployment settings**:
   - Project name: `worker-bee` or your preferred name
   - Environment: Production
3. **Set Environment Variables** (see below)
4. **Click Deploy**

## Method 2: Create New Bolt Project

If you want to create a fresh deployment:

1. **Go to [bolt.new](https://bolt.new)**
2. **Create a new project**
3. **Upload/copy your code** to the new project
4. **Follow the deployment steps**

## 🔧 Required Environment Variables

Set these in your Bolt project settings:

### Minimum Required (Free Option):
```env
MODEL_PROVIDER=pollinations
MODEL=openai
POLLINATIONS_REFERRER=worker-bee-bolt-v1
```

### Optional Enhancements:
```env
# For higher rate limits (optional)
POLLINATIONS_API_KEY=your_pollinations_key

# For monitoring and debugging (optional)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langchain_key
LANGCHAIN_PROJECT=worker-bee

# Logging level
BROWSER_USE_LOGGING_LEVEL=info
```

### Alternative AI Providers (if you prefer):
```env
# Azure OpenAI
MODEL_PROVIDER=azure
MODEL=gpt-4o
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_ENDPOINT=your_azure_endpoint

# OpenAI
MODEL_PROVIDER=openai
MODEL=gpt-4o
OPENAI_API_KEY=your_openai_key

# Groq (fast and often free)
MODEL_PROVIDER=groq
MODEL=llama-3.1-70b-versatile
GROQ_API_KEY=your_groq_key
```

## 🎯 Deployment Process

1. **Bolt automatically runs the build command**:
   ```bash
   pip install -r requirements.txt && 
   python -m playwright install chromium && 
   python -m playwright install-deps && 
   cd openoperator-ui && 
   npm install && 
   npm run build
   ```

2. **Starts the production server**:
   ```bash
   python backend_server.py
   ```

3. **Serves your app** at the provided Bolt URL

## 🔍 What to Expect

- **Build time**: 3-5 minutes (installing browsers takes time)
- **Health check**: Available at `/api/health`
- **Frontend**: Served at your Bolt URL
- **API**: Available at `/api/analyze`

## 🧪 Testing Your Deployment

Once deployed, test with these examples:

1. **Basic test**: 
   - URL: `https://example.com`
   - Query: "What is the title and main content of this page?"

2. **Advanced test**:
   - URL: `https://github.com/microsoft/playwright`
   - Query: "What is this project about and what are its main features?"

## 🐛 Troubleshooting

### Build Fails?
- Check that all environment variables are set
- Verify the build logs in Bolt dashboard
- Ensure Python dependencies are compatible

### Runtime Errors?
- Check the application logs
- Verify AI provider credentials
- Test with simple URLs first

### Performance Issues?
- Consider upgrading resources in Bolt settings
- Use Pollinations for free, unlimited processing
- Enable monitoring with LangChain tracing

## 💡 Pro Tips

1. **Use Pollinations** for free AI processing (no OpenAI costs!)
2. **Set up monitoring** with LangChain for debugging
3. **Test locally first** with `python start_ui.py`
4. **Check health endpoint** at `/api/health` after deployment

## 🎉 Success!

Once deployed, your Worker Bee will be buzzing around the web, ready to:
- 🌐 Analyze any website
- 🔍 Extract specific information
- 📊 Generate detailed reports
- 🤖 Automate web tasks with AI

Your Bolt URL will be something like: `https://your-project-name.bolt.new`

---

Need help? Check the Bolt documentation or the project's troubleshooting guide!