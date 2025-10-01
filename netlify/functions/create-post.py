import json
import os
from datetime import datetime

def handler(event, context):
    """
    Netlify function to create new blog posts
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
        required_fields = ['title', 'excerpt', 'content', 'category']
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
        
        # Extract post data
        post_data = {
            'id': body.get('id', int(datetime.now().timestamp())),
            'title': body['title'],
            'excerpt': body['excerpt'],
            'content': body['content'],
            'category': body['category'],
            'emoji': body.get('emoji', '📝'),
            'date': body.get('date', datetime.now().isoformat()),
            'youtubeUrl': body.get('youtubeUrl'),
            'youtubeId': body.get('youtubeId')
        }
        
        # In a real application, you would:
        # 1. Save to database (e.g., MongoDB, PostgreSQL)
        # 2. Validate YouTube URL
        # 3. Fetch YouTube video metadata
        # 4. Resize/optimize images
        # 5. Generate SEO-friendly slugs
        # 6. Send notifications
        
        # For now, we'll just log the post creation
        print(f"New blog post created: {json.dumps(post_data)}")
        
        # Simulate successful creation
        return {
            'statusCode': 201,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': json.dumps({
                'success': True,
                'message': 'Blog post created successfully',
                'post': post_data
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