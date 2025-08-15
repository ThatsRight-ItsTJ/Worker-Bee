#!/usr/bin/env python3
"""
Basic web automation test script for OpenOperator
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from openoperator.agent.graph import graph

# Load environment variables
load_dotenv()

async def test_basic_automation():
    """Test basic web automation with a simple task"""
    
    # Check required environment variables
    required_vars = ["MODEL", "MODEL_PROVIDER"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("\nPlease set these in your .env file:")
        print("MODEL=gpt-4o")
        print("MODEL_PROVIDER=azure")
        print("AZURE_OPENAI_API_KEY=your_key_here")
        print("AZURE_OPENAI_ENDPOINT=your_endpoint_here")
        return
    
    print("🤖 Starting OpenOperator Web Automation Test")
    print("=" * 50)
    
    # Compile the agent graph
    app = graph.compile()
    config = {"configurable": {"temperature": 0.1}, "recursion_limit": 100}
    
    # Test cases - start with simple ones
    test_cases = [
        {
            "name": "Simple Website Analysis",
            "url": "https://example.com",
            "query": "Tell me what this website is about and what content is displayed"
        },
        {
            "name": "Wikipedia Navigation", 
            "url": "https://en.wikipedia.org/wiki/Main_Page",
            "query": "Navigate to the Wikipedia main page and tell me what the featured article is today"
        },
        {
            "name": "GitHub Repository",
            "url": "https://github.com/microsoft/playwright",
            "query": "Go to the Playwright GitHub repository and tell me what the project is about based on the README"
        }
    ]
    
    # Run a simple test case - start with example.com (simpler)
    test_case = test_cases[0]  # Start with example.com
    
    print(f"🔍 Running test: {test_case['name']}")
    print(f"📍 URL: {test_case['url']}")
    print(f"📝 Task: {test_case['query']}")
    print("-" * 50)
    
    try:
        print("🚀 Starting agent execution...")
        result = await app.ainvoke({
            "url": test_case["url"], 
            "query": test_case["query"]
        }, config=config)
        
        print("✅ Test completed successfully!")
        print("\n📋 Result:")
        print("=" * 30)
        
        final_output = result.get("final_output", "No final output available.")
        if isinstance(final_output, dict):
            print(f"Answer: {final_output.get('answer', 'No answer provided')}")
            print(f"Sources: {final_output.get('sources', [])}")
            if final_output.get('quotes'):
                print("Quotes:")
                for quote in final_output.get('quotes', []):
                    print(f"  - {quote}")
        else:
            print(final_output)
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        print("\n🔍 Debugging info:")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        
        # Suggest solutions
        if "recursion" in str(e).lower():
            print("\n💡 Possible solutions:")
            print("1. The agent might be stuck in a loop")
            print("2. Try a simpler task or different URL")
            print("3. Check if the LLM is properly calling tools")
            print("4. Enable debug logging: BROWSER_USE_LOGGING_LEVEL=debug")

async def test_interactive_mode():
    """Interactive mode for custom testing"""
    print("\n🎮 Interactive Mode")
    print("=" * 30)
    
    app = graph.compile()
    config = {"configurable": {"temperature": 0.5}, "recursion_limit": 25}
    
    while True:
        print("\nEnter a URL and task, or 'quit' to exit:")
        url = input("URL: ").strip()
        
        if url.lower() in ['quit', 'exit', 'q']:
            break
            
        if not url:
            print("Please enter a valid URL")
            continue
            
        query = input("Task: ").strip()
        if not query:
            print("Please enter a task description")
            continue
            
        print(f"\n🚀 Running automation...")
        print(f"URL: {url}")
        print(f"Task: {query}")
        print("-" * 40)
        
        try:
            result = await app.ainvoke({"url": url, "query": query}, config=config)
            
            print("\n✅ Completed!")
            final_output = result.get("final_output", "No output available.")
            if isinstance(final_output, dict):
                print(f"Answer: {final_output.get('answer', 'No answer')}")
            else:
                print(final_output)
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("OpenOperator Web Automation Test Suite")
    print("=====================================")
    
    mode = input("Choose mode:\n1. Basic test\n2. Interactive mode\nEnter choice (1 or 2): ").strip()
    
    if mode == "2":
        asyncio.run(test_interactive_mode())
    else:
        asyncio.run(test_basic_automation())