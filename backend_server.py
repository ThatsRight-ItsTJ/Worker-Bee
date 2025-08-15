#!/usr/bin/env python3
"""
Simple Flask backend server for OpenOperator UI
"""

import asyncio
import json
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_from_directory
import sys
import os

# Get port from environment variable (for deployment)
PORT = int(os.environ.get('PORT', 5000))
HOST = os.environ.get('HOST', '0.0.0.0')

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from openoperator.agent.graph import graph
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Health check endpoint (for Bolt monitoring)
@app.route('/health', methods=['GET'])
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for deployment monitoring"""
    try:
        # Quick check that core components are working
        model = os.getenv("MODEL", "not set")
        provider = os.getenv("MODEL_PROVIDER", "not set")
        
        return jsonify({
            'status': 'healthy',
            'service': 'Worker Bee API',
            'version': '1.0.0',
            'model': model,
            'provider': provider,
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

# Serve static files from the built frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """Serve the React frontend"""
    frontend_dir = os.path.join(os.path.dirname(__file__), 'openoperator-ui', 'dist')
    
    # Handle static assets
    if path and os.path.exists(os.path.join(frontend_dir, path)):
        return send_from_directory(frontend_dir, path)
    
    # Serve index.html for all other routes (SPA routing)
    if os.path.exists(os.path.join(frontend_dir, 'index.html')):
        return send_from_directory(frontend_dir, 'index.html')
    else:
        return jsonify({'error': 'Frontend not built. Please run build process.'}), 500

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import time for health check
import time

# Compile the agent graph once at startup
agent_app = graph.compile()
config = {"configurable": {"temperature": 0.1}, "recursion_limit": 50}

@app.route('/api/analyze', methods=['POST'])
def analyze_website():
    """Analyze a website with the given query"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        url = data.get('url')
        query = data.get('query')
        
        if not url or not query:
            return jsonify({'error': 'Both URL and query are required'}), 400
        
        logger.info(f"Analyzing URL: {url} with query: {query}")
        
        # Run the agent asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                agent_app.ainvoke({"url": url, "query": query}, config=config)
            )
            
            final_output = result.get("final_output", "No output available.")
            
            # Handle different output formats
            if isinstance(final_output, dict):
                response = {
                    'ops_summary': final_output.get('ops_summary', 'Analysis completed'),
                    'answer': final_output.get('answer', 'No answer provided'),
                    'sources': final_output.get('sources', [url]),
                    'quotes': final_output.get('quotes', [])
                }
            else:
                # Handle string output (error cases)
                response = {
                    'ops_summary': 'Analysis completed with basic output',
                    'answer': str(final_output),
                    'sources': [url],
                    'quotes': []
                }
            
            logger.info("Analysis completed successfully")
            return jsonify(response)
            
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        return jsonify({
            'error': f'Analysis failed: {str(e)}',
        'details': 'Please check if the URL is accessible and try again.',
        'suggestion': 'Try with a simpler URL like https://example.com first'
        }), 500

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API info"""
    return jsonify({
        'service': 'Worker Bee API',
        'version': '1.0.0',
        'description': 'AI-powered web automation and information extraction',
        'endpoints': {
            'analyze': '/api/analyze (POST)',
            'health': '/api/health (GET)',
            'frontend': '/ (GET)'
        },
        'status': 'ready'
    })

if __name__ == '__main__':
    # Check required environment variables
    required_vars = ["MODEL_PROVIDER"]  # MODEL has a default
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please set MODEL_PROVIDER in your environment variables")
        logger.error("Recommended: MODEL_PROVIDER=pollinations (free)")
        sys.exit(1)
    
    logger.info("🐝 Starting Worker Bee API server...")
    logger.info(f"Model: {os.getenv('MODEL', 'openai')}")
    logger.info(f"Provider: {os.getenv('MODEL_PROVIDER')}")
    logger.info(f"Server: http://{HOST}:{PORT}")
    
    app.run(host=HOST, port=PORT, debug=False)