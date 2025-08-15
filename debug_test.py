#!/usr/bin/env python3
"""
Debug test script for OpenOperator - with detailed logging
"""

import asyncio
import os
import logging
from dotenv import load_dotenv

# Set debug logging before importing
os.environ['BROWSER_USE_LOGGING_LEVEL'] = 'debug'

from openoperator.agent.graph import graph

load_dotenv()

async def debug_test():
    """Run a debug test with detailed logging"""
    
    # Set up detailed logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    print("🐛 Debug OpenOperator Test")
    print("=" * 40)
    
    # Check environment
    model = os.getenv("MODEL", "not set")
    provider = os.getenv("MODEL_PROVIDER", "not set")
    print(f"Model: {model}")
    print(f"Provider: {provider}")
    print("-" * 40)
    
    # Compile the agent graph
    app = graph.compile()
    config = {
        "configurable": {"temperature": 0.1},  # Lower temperature for more deterministic behavior
        "recursion_limit": 100  # Higher limit
    }
    
    # Very simple test case
    url = "https://httpbin.org/html"  # Simple HTML page
    query = "What is the title of this page?"
    
    print(f"🔍 Testing with:")
    print(f"URL: {url}")
    print(f"Query: {query}")
    print("-" * 40)
    
    try:
        print("🚀 Starting execution...")
        
        # Use astream to see intermediate steps
        async for chunk in app.astream({
            "url": url,
            "query": query
        }, config=config):
            print(f"📝 Step: {chunk}")
            
        print("✅ Test completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_test())