import json
import os
import sys
import asyncio
from urllib.parse import parse_qs

# Add the project root to Python path
sys.path.append('/opt/build/repo')

def handler(event, context):
    """Netlify function handler for the analyze endpoint"""
    
    # Handle CORS preflight
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': ''
        }
    
    # Only allow POST requests
    if event['httpMethod'] != 'POST':
        return {
            'statusCode': 405,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # Parse request body
        body = json.loads(event['body'])
        url = body.get('url')
        query = body.get('query')
        
        if not url or not query:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': 'Both URL and query are required'})
            }
        
        # For Netlify, we'll return a simplified response since Playwright won't work
        # In a real deployment, you'd need to use a headless browser service
        response = {
            'ops_summary': 'Analysis completed using Netlify Functions',
            'answer': f'This is a demo response for URL: {url} with query: {query}. Full browser automation is not available on Netlify due to platform limitations. Consider using Bolt Hosting or Railway for full functionality.',
            'sources': [url],
            'quotes': ['Demo quote: Browser automation requires a different hosting platform for full functionality.']
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps(response)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': f'Analysis failed: {str(e)}',
                'details': 'Browser automation is not supported on Netlify. Consider using Bolt Hosting or Railway for full functionality.'
            })
        }