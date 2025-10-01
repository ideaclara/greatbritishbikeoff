from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
import json
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

# Sample blog data (in production, use a database)
BLOG_POSTS = [
    {
        'id': 1,
        'title': 'Cotswolds Cycling Adventure',
        'excerpt': 'A perfect weekend exploring the rolling hills and charming villages of the Cotswolds, discovering hidden gems and sampling local delicacies along the way.',
        'content': 'Full blog post content would go here...',
        'date': '2025-01-15',
        'category': 'cycling',
        'emoji': '🚴‍♂️',
        'youtube_url': None,
        'youtube_id': None
    },
    {
        'id': 2,
        'title': 'Best Cake Stops in Yorkshire',
        'excerpt': 'Discovering the finest tea rooms and bakeries along the Yorkshire Dales cycling routes. From traditional Yorkshire parkin to modern artisan treats.',
        'content': 'Full blog post content would go here...',
        'date': '2025-01-10',
        'category': 'food',
        'emoji': '🍰',
        'youtube_url': None,
        'youtube_id': None
    },
    {
        'id': 3,
        'title': 'Essential Gear for British Weather',
        'excerpt': 'A comprehensive guide to staying comfortable and safe while cycling through Britain\'s unpredictable weather conditions.',
        'content': 'Full blog post content would go here...',
        'date': '2025-01-08',
        'category': 'gear',
        'emoji': '⚙️',
        'youtube_url': None,
        'youtube_id': None
    },
    {
        'id': 4,
        'title': 'Scotland\'s North Coast 500',
        'excerpt': 'An epic journey around Scotland\'s stunning coastline, featuring dramatic landscapes, historic castles, and unforgettable Highland hospitality.',
        'content': 'Full blog post content would go here...',
        'date': '2025-01-05',
        'category': 'travel',
        'emoji': '🗺️',
        'youtube_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'youtube_id': 'dQw4w9WgXcQ'
    }
]

def extract_youtube_id(url):
    """Extract YouTube video ID from URL"""
    if not url:
        return None
    
    pattern = r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_admin_password():
    """Get admin password from environment or use default"""
    return os.environ.get('ADMIN_PASSWORD', 'bikeoff2025')

@app.route('/')
def index():
    """Main blog page"""
    category_filter = request.args.get('category', 'all')
    
    if category_filter == 'all':
        posts = BLOG_POSTS
    else:
        posts = [post for post in BLOG_POSTS if post['category'] == category_filter]
    
    return render_template('index.html', posts=posts, current_category=category_filter)

@app.route('/post/<int:post_id>')
def view_post(post_id):
    """View individual blog post"""
    post = next((p for p in BLOG_POSTS if p['id'] == post_id), None)
    if not post:
        return "Post not found", 404
    
    return render_template('post.html', post=post)

@app.route('/admin')
def admin_login():
    """Admin login page"""
    if session.get('admin_authenticated'):
        return redirect(url_for('admin_panel'))
    
    return render_template('admin_login.html')

@app.route('/admin/login', methods=['POST'])
def admin_authenticate():
    """Handle admin login"""
    password = request.form.get('password')
    
    if password == get_admin_password():
        session['admin_authenticated'] = True
        return redirect(url_for('admin_panel'))
    else:
        return render_template('admin_login.html', error='Incorrect password')

@app.route('/admin/panel')
def admin_panel():
    """Admin panel for managing posts"""
    if not session.get('admin_authenticated'):
        return redirect(url_for('admin_login'))
    
    return render_template('admin_panel.html', posts=BLOG_POSTS)

@app.route('/admin/create', methods=['POST'])
def create_post():
    """Create new blog post"""
    if not session.get('admin_authenticated'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json() if request.is_json else request.form
    
    # Extract YouTube ID if URL provided
    youtube_id = extract_youtube_id(data.get('youtube_url'))
    
    new_post = {
        'id': max([p['id'] for p in BLOG_POSTS], default=0) + 1,
        'title': data.get('title'),
        'excerpt': data.get('excerpt'),
        'content': data.get('content'),
        'category': data.get('category'),
        'emoji': data.get('emoji', '📝'),
        'date': datetime.now().strftime('%Y-%m-%d'),
        'youtube_url': data.get('youtube_url'),
        'youtube_id': youtube_id
    }
    
    BLOG_POSTS.insert(0, new_post)
    
    if request.is_json:
        return jsonify({'success': True, 'post': new_post})
    else:
        return redirect(url_for('admin_panel'))

@app.route('/admin/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    """Delete blog post"""
    if not session.get('admin_authenticated'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    global BLOG_POSTS
    BLOG_POSTS = [p for p in BLOG_POSTS if p['id'] != post_id]
    
    return redirect(url_for('admin_panel'))

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_authenticated', None)
    return redirect(url_for('index'))

@app.route('/contact', methods=['POST'])
def contact():
    """Handle contact form submission"""
    data = request.get_json() if request.is_json else request.form
    
    # In production, you'd send email or save to database
    contact_data = {
        'name': data.get('name'),
        'email': data.get('email'),
        'message': data.get('message'),
        'timestamp': datetime.now().isoformat()
    }
    
    print(f"Contact form submission: {contact_data}")
    
    if request.is_json:
        return jsonify({'success': True, 'message': 'Message sent successfully'})
    else:
        return redirect(url_for('index'))

@app.route('/api/posts')
def api_posts():
    """API endpoint for posts (for JavaScript compatibility)"""
    category_filter = request.args.get('type', 'all')
    
    if category_filter == 'all' or category_filter == 'blog':
        posts = BLOG_POSTS
    else:
        posts = [post for post in BLOG_POSTS if post['category'] == category_filter]
    
    return jsonify(posts)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))