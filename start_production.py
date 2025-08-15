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
    required_vars = ["MODEL", "MODEL_PROVIDER"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please set these in your Bolt environment variables:")
        logger.error("- MODEL=gpt-4o")
        logger.error("- MODEL_PROVIDER=azure")
        logger.error("- AZURE_OPENAI_API_KEY=your_key")
        logger.error("- AZURE_OPENAI_ENDPOINT=your_endpoint")
        sys.exit(1)
    
    logger.info(f"✅ Using model: {os.getenv('MODEL')} with provider: {os.getenv('MODEL_PROVIDER')}")

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