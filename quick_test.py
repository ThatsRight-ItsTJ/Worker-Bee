#!/usr/bin/env python3
"""
Quick test script for OpenOperator - minimal example
"""

import asyncio
import os
from dotenv import load_dotenv
from openoperator.main import main

load_dotenv()

async def quick_test():
    """Run a quick test of the web automation"""
    
    # Simple test case
    url = "https://example.com"
    query = "Tell me what this website is about and what content is displayed"
    
    print("🚀 Quick OpenOperator Test")
    print(f"URL: {url}")
    print(f"Task: {query}")
    print("-" * 40)
    
    await main(url, query)

if __name__ == "__main__":
    asyncio.run(quick_test())