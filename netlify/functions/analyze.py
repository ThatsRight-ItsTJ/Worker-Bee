import json

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
        
        # For static deployment, return a demo response
        response = {
            'ops_summary': 'Static deployment demo - full automation requires server hosting',
            'answer': f'This is a demo response for URL: {url} with query: {query}. For full web automation capabilities, please deploy to a server environment like Railway, Render, or use the local development server.',
            'sources': [url],
            'quotes': ['Demo: This static deployment shows the UI but cannot perform actual web automation.']
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
                'details': 'This is a static deployment. For full functionality, deploy to a server environment.'
            })
        }