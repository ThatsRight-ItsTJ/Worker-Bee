import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import shutil
import argparse
import logging

from dotenv import load_dotenv

from openoperator.agent.graph import graph

load_dotenv()

logger = logging.getLogger(__name__)
app = graph.compile()
config = {"configurable": {"temperature": 0.5}, "recursion_limit": 25}


required_vars = ["MODEL", "MODEL_PROVIDER"]
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
    sys.exit(1)

async def main(url: str, query: str):
    try:
        result = await app.ainvoke({"url": url, "query": query}, config=config) # type: ignore
    except Exception as e:
        logger.error(f"An error occurred during invocation: {e}")
        return None

    # Clean up downloads folder
    downloads_dir = os.path.join(os.getcwd(), "downloads")
    if os.path.exists(downloads_dir):
        try:
            shutil.rmtree(downloads_dir)
            os.makedirs(downloads_dir)
        except Exception as e:
            logger.error(f"Failed to clean downloads directory: {e}")

    print(result.get("final_output", "No final output available."))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run browser agent with URL and query')
    parser.add_argument('url', type=str, help='The URL to navigate to')
    parser.add_argument('query', type=str, help='The query/task to perform')
    
    args = parser.parse_args()
    asyncio.run(main(args.url, args.query))