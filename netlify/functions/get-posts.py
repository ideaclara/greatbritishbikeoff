import json
import os
from datetime import datetime

def handler(event, context):
    """
    Netlify function to get blog posts, routes, or food posts
    """
    try:
        # Get query parameters
        query_params = event.get('queryStringParameters', {}) or {}
        post_type = query_params.get('type', 'blog')
        
        # Sample data - in a real app, this would come from a database
        sample_data = {
            'blog': [
                {
                    'id': 1,
                    'title': 'Cotswolds Cycling Adventure',
                    'excerpt': 'A perfect weekend exploring the rolling hills and charming villages of the Cotswolds.',
                    'date': '2025-01-15',
                    'category': 'Adventure',
                    'emoji': '🚴‍♂️'
                },
                {
                    'id': 2,
                    'title': 'Best Cake Stops in Yorkshire',
                    'excerpt': 'Discovering the finest tea rooms and bakeries along the Yorkshire Dales cycling routes.',
                    'date': '2025-01-10',
                    'category': 'Food',
                    'emoji': '🍰'
                },
                {
                    'id': 3,
                    'title': 'Winter Cycling Tips',
                    'excerpt': 'Essential gear and techniques for safe and enjoyable winter cycling adventures.',
                    'date': '2025-01-05',
                    'category': 'Tips',
                    'emoji': '❄️'
                }
            ],
            'route': [
                {
                    'id': 1,
                    'title': 'Thames Path Challenge',
                    'description': 'Follow the historic Thames Path from Oxford to Windsor, with plenty of riverside pubs.',
                    'distance': 45,
                    'difficulty': 'Easy',
                    'emoji': '🚴‍♂️'
                },
                {
                    'id': 2,
                    'title': 'Peak District Loop',
                    'description': 'Challenging route through the stunning Peak District with breathtaking views.',
                    'distance': 62,
                    'difficulty': 'Hard',
                    'emoji': '⛰️'
                },
                {
                    'id': 3,
                    'title': 'Cornwall Coastal Ride',
                    'description': 'Spectacular coastal cycling with fresh seafood stops and stunning ocean views.',
                    'distance': 38,
                    'difficulty': 'Medium',
                    'emoji': '🌊'
                }
            ],
            'food': [
                {
                    'id': 1,
                    'title': 'The King\'s Head, Chipping Campden',
                    'description': 'Traditional Cotswolds pub with excellent local ales and hearty portions.',
                    'location': 'Chipping Campden',
                    'rating': 4.5,
                    'emoji': '🍺'
                },
                {
                    'id': 2,
                    'title': 'Betty\'s Tea Rooms',
                    'description': 'Iconic Yorkshire tea room serving the best fat rascals and afternoon tea.',
                    'location': 'Harrogate',
                    'rating': 5.0,
                    'emoji': '🥧'
                },
                {
                    'id': 3,
                    'title': 'The Seafood Restaurant',
                    'description': 'Fresh Cornwall seafood with stunning harbor views - perfect after a coastal ride.',
                    'location': 'Padstow',
                    'rating': 4.8,
                    'emoji': '🦞'
                }
            ]
        }
        
        # Get the requested data
        posts = sample_data.get(post_type, [])
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': json.dumps(posts)
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