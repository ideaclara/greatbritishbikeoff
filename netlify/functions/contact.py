import json
import os
from datetime import datetime

def handler(event, context):
    """
    Netlify function to handle contact form submissions
    """
    try:
        # Only allow POST requests
        if event['httpMethod'] != 'POST':
            return {
                'statusCode': 405,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Method not allowed'})
            }
        
        # Parse the request body
        body = json.loads(event['body'])
        
        # Validate required fields
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if not body.get(field):
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'error': 'Missing required field',
                        'field': field
                    })
                }
        
        # Extract form data
        name = body['name']
        email = body['email']
        message = body['message']
        timestamp = datetime.now().isoformat()
        
        # In a real application, you would:
        # 1. Save to database
        # 2. Send email notification
        # 3. Validate email format
        # 4. Implement rate limiting
        
        # For now, we'll just log the submission (in production, use proper logging)
        contact_data = {
            'name': name,
            'email': email,
            'message': message,
            'timestamp': timestamp,
            'ip': event.get('headers', {}).get('x-forwarded-for', 'unknown')
        }
        
        # Simulate processing
        print(f"Contact form submission: {json.dumps(contact_data)}")
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': json.dumps({
                'success': True,
                'message': 'Contact form submitted successfully',
                'timestamp': timestamp
            })
        }
        
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Invalid JSON in request body'
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