import json
import os

def handler(event, context):
    """
    Netlify function to get configuration (like admin password)
    """
    try:
        # Handle OPTIONS request for CORS
        if event['httpMethod'] == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'GET, OPTIONS'
                },
                'body': ''
            }
        
        # Get admin password from environment variable
        admin_password = os.environ.get('ADMIN_PASSWORD')
        
        # Debug logging (will show in Netlify function logs)
        print(f"Environment variable ADMIN_PASSWORD exists: {admin_password is not None}")
        print(f"All environment variables: {list(os.environ.keys())}")
        
        # Use fallback only if environment variable is not set
        if admin_password is None:
            admin_password = 'bikeoff2025'
            print("Using fallback password")
        else:
            print("Using environment variable password")
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, OPTIONS'
            },
            'body': json.dumps({
                'adminPassword': admin_password,
                'usingEnvVar': admin_password != 'bikeoff2025'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }