#!/usr/bin/env python3
"""
Production startup script for Bolt Hosting
"""

import os
import sys
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_environment():
    """Set up the production environment"""
    logger.info("🚀 Setting up Worker Bee for production...")
    
    # Set Python path
    os.environ['PYTHONPATH'] = '/app'
    
    # Check if we're in the right directory
    if not os.path.exists('backend_server.py'):
        logger.error("❌ backend_server.py not found. Please check deployment.")
        sys.exit(1)
    
    # Check if frontend is built
    if not os.path.exists('openoperator-ui/dist/index.html'):
        logger.error("❌ Frontend not built. Please check build process.")
        sys.exit(1)
    
    logger.info("✅ Environment setup complete")

def check_requirements():
    """Check if all required environment variables are set"""
    # Only MODEL_PROVIDER is truly required, MODEL has a default
    required_vars = ["MODEL_PROVIDER"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("For Pollinations (recommended free option), set:")
        logger.error("- MODEL_PROVIDER=pollinations")
        logger.error("- MODEL=openai (or gemini, sur, deepseek)")
        logger.error("- POLLINATIONS_REFERRER=worker-bee-bolt-v1")
        sys.exit(1)
    
    model = os.getenv('MODEL', 'openai')
    provider = os.getenv('MODEL_PROVIDER')
    logger.info(f"✅ Using model: {model} with provider: {provider}")
    
    if provider == 'pollinations':
        logger.info("🌸 Using Pollinations AI - Free and unlimited!")
        referrer = os.getenv('POLLINATIONS_REFERRER', 'worker-bee-bolt-v1')
        logger.info(f"📝 Referrer: {referrer}")
        api_key = os.getenv('POLLINATIONS_API_KEY')
        if api_key:
            logger.info("🔑 Using Pollinations API key for enhanced features")
        else:
            logger.info("🆓 Using free Pollinations access (no API key required)")

def main():
    """Main startup function"""
    setup_environment()
    check_requirements()
    
    logger.info("🐝 Starting Worker Bee production server...")
    
    # Start the Flask server
    try:
        from backend_server import app
        port = int(os.environ.get('PORT', 5000))
        host = os.environ.get('HOST', '0.0.0.0')
        
        logger.info(f"🌐 Server starting on {host}:{port}")
        app.run(host=host, port=port, debug=False)
        
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()