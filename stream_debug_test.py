#!/usr/bin/env python3
"""
Streaming debug test to see exactly where the agent gets stuck
"""

import asyncio
import os
import logging
from dotenv import load_dotenv

# Set debug logging before importing
os.environ['BROWSER_USE_LOGGING_LEVEL'] = 'debug'

from openoperator.agent.graph import graph

load_dotenv()

async def stream_debug_test():
    """Stream the agent execution to see where it gets stuck"""
    
    # Set up detailed logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    print("🐛 Streaming Debug Test - Pollinations Agent")
    print("=" * 50)
    
    # Check environment
    model = os.getenv("MODEL", "not set")
    provider = os.getenv("MODEL_PROVIDER", "not set")
    print(f"Model: {model}")
    print(f"Provider: {provider}")
    print("-" * 50)
    
    # Compile the agent graph
    app = graph.compile()
    config = {
        "configurable": {"temperature": 0.1},  # Very low temperature
        "recursion_limit": 20  # Lower limit to fail faster
    }
    
    # Very simple test case
    url = "https://example.com"
    query = "What is the title of this page?"
    
    print(f"🔍 Testing with:")
    print(f"URL: {url}")
    print(f"Query: {query}")
    print("-" * 50)
    
    try:
        print("🚀 Starting streaming execution...")
        step_count = 0
        
        async for chunk in app.astream({
            "url": url,
            "query": query
        }, config=config):
            step_count += 1
            print(f"\n📝 Step {step_count}:")
            print(f"Keys: {list(chunk.keys())}")
            
            for key, value in chunk.items():
                if key == "messages":
                    print(f"  {key}: {len(value)} messages")
                    for i, msg in enumerate(value):
                        msg_type = type(msg).__name__
                        content_preview = str(msg.content)[:100] if hasattr(msg, 'content') else "No content"
                        tool_calls = getattr(msg, 'tool_calls', None)
                        print(f"    Message {i}: {msg_type}")
                        print(f"      Content: {content_preview}...")
                        if tool_calls:
                            print(f"      Tool calls: {len(tool_calls)}")
                            for tc in tool_calls:
                                print(f"        - {tc.get('name', 'unknown')}: {tc.get('args', {})}")
                elif key == "final_output":
                    print(f"  {key}: {value}")
                else:
                    print(f"  {key}: {type(value).__name__}")
            
            # Stop if we see too many steps
            if step_count > 15:
                print("\n⚠️  Stopping after 15 steps to prevent infinite loop")
                break
                
        print(f"\n✅ Completed after {step_count} steps!")
        
    except Exception as e:
        print(f"\n❌ Error after {step_count} steps: {e}")
        print(f"Error type: {type(e).__name__}")
        
        # Show the last few steps that led to the error
        print("\n🔍 This helps identify where the loop occurs:")
        print("- Look for repeated patterns in the steps above")
        print("- Check if tools are being called properly")
        print("- See if the agent is getting stuck between specific nodes")

if __name__ == "__main__":
    asyncio.run(stream_debug_test())