"""
Simple test to verify Vercel can run Python functions
"""

def handler(event, context):
    return {
        'statusCode': 200,
        'body': 'Hello from Vercel Python! Django app is loading...'
    }

app = handler
