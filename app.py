from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
import os
import json
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

# Build number for tracking deployments
BUILD_NUMBER = os.environ.get('BUILD_NUMBER', f"dev-{datetime.now().strftime('%Y%m%d-%H%M')}")

@app.context_processor
def inject_build_number():
    return {'build_number': BUILD_NUMBER}

# Database configuration
database_url = os.environ.get('DATABASE_URL', 'sqlite:///blog.db')
# Fix for PostgreSQL URL format (Render uses postgresql://, SQLAlchemy expects postgresql+psycopg2://)
if database_url.startswith('postgresql://'):
    database_url = database_url.replace('postgresql://', 'postgresql+psycopg2://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    excerpt = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    emoji = db.Column(db.String(10), default='📝')
    date = db.Column(db.String(20), nullable=False)
    youtube_url = db.Column(db.String(500))
    youtube_id = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'excerpt': self.excerpt,
            'content': self.content,
            'category': self.category,
            'emoji': self.emoji,
            'date': self.date,
            'youtube_url': self.youtube_url,
            'youtube_id': self.youtube_id
        }

# Initialize database and create sample data
def init_db():
    """Initialize database with sample data if empty"""
    try:
        with app.app_context():
            # Check if tables exist first
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            if 'blog_post' not in existing_tables:
                print("Creating database tables for the first time...")
                db.create_all()
                print("Database tables created successfully")
            else:
                print("Database tables already exist")
            
            # Check if we already have posts
            try:
                post_count = BlogPost.query.count()
                print(f"Found {post_count} existing posts in database")
            except Exception as e:
                print(f"Error counting posts: {e}")
                # If there's an error, the table might not exist properly
                db.create_all()
                post_count = 0
                print("Recreated tables and reset post count")
            
            # Only add sample data if database is completely empty
            # AND we explicitly want sample data (controlled by environment variable)
            if post_count == 0:
                # Check if this is production (has DATABASE_URL) and skip sample data
                if os.environ.get('DATABASE_URL'):
                    print("Production database detected - no sample data added")
                    print("Ready for your first blog post via admin panel!")
                elif os.environ.get('INIT_SAMPLE_DATA') == 'true':
                    print("INIT_SAMPLE_DATA=true - creating sample data...")
                    # Add sample posts
                    sample_posts = [
                        BlogPost(
                            title='Cotswolds Cycling Adventure',
                            excerpt='A perfect weekend exploring the rolling hills and charming villages of the Cotswolds, discovering hidden gems and sampling local delicacies along the way.',
                            content='Full blog post content would go here...',
                            category='cycling',
                            emoji='🚴‍♂️',
                            date='2025-01-15'
                        ),
                        BlogPost(
                            title='Best Cake Stops in Yorkshire',
                            excerpt='Discovering the finest tea rooms and bakeries along the Yorkshire Dales cycling routes. From traditional Yorkshire parkin to modern artisan treats.',
                            content='Full blog post content would go here...',
                            category='food',
                            emoji='🍰',
                            date='2025-01-10'
                        ),
                        BlogPost(
                            title='Essential Gear for British Weather',
                            excerpt='A comprehensive guide to staying comfortable and safe while cycling through Britain\'s unpredictable weather conditions.',
                            content='Full blog post content would go here...',
                            category='gear',
                            emoji='⚙️',
                            date='2025-01-08'
                        ),
                        BlogPost(
                            title='Scotland\'s North Coast 500',
                            excerpt='An epic journey around Scotland\'s stunning coastline, featuring dramatic landscapes, historic castles, and unforgettable Highland hospitality.',
                            content='Full blog post content would go here...',
                            category='travel',
                            emoji='🗺️',
                            date='2025-01-05',
                            youtube_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                            youtube_id='dQw4w9WgXcQ'
                        )
                    ]
                    
                    for post in sample_posts:
                        db.session.add(post)
                    
                    db.session.commit()
                    print("Sample data created for development")
                else:
                    print("Local development - no sample data (set INIT_SAMPLE_DATA=true if needed)")
            else:
                print("Existing posts preserved - database has content")
                
    except Exception as e:
        print(f"Error initializing database: {e}")
        # Don't fail the app startup, just log the error
        pass

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
    try:
        # Get all posts from database, ordered by creation date (newest first)
        posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
        posts_dict = [post.to_dict() for post in posts]
        return render_template('index.html', posts=posts_dict)
    except Exception as e:
        print(f"Error loading posts: {e}")
        # Try to initialize database if it fails
        init_db()
        # Return empty posts list as fallback
        return render_template('index.html', posts=[])

@app.route('/post/<int:post_id>')
def view_post(post_id):
    """View individual blog post"""
    post = BlogPost.query.get_or_404(post_id)
    return render_template('post.html', post=post.to_dict())

@app.route('/admin')
@app.route('/secret-admin-access')
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
    
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    posts_dict = [post.to_dict() for post in posts]
    return render_template('admin_panel.html', posts=posts_dict)

@app.route('/admin/create', methods=['POST'])
def create_post():
    """Create new blog post"""
    if not session.get('admin_authenticated'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json() if request.is_json else request.form
    
    # Validate required fields
    if not all([data.get('title'), data.get('excerpt'), data.get('content'), data.get('category')]):
        posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
        posts_dict = [post.to_dict() for post in posts]
        return render_template('admin_panel.html', posts=posts_dict, error='All fields are required')
    
    # Extract YouTube ID if URL provided
    youtube_id = extract_youtube_id(data.get('youtube_url'))
    
    # Create new blog post
    new_post = BlogPost(
        title=data.get('title'),
        excerpt=data.get('excerpt'),
        content=data.get('content'),
        category=data.get('category'),
        emoji=data.get('emoji', '📝'),
        date=datetime.now().strftime('%Y-%m-%d'),
        youtube_url=data.get('youtube_url'),
        youtube_id=youtube_id
    )
    
    # Save to database
    db.session.add(new_post)
    db.session.commit()
    
    if request.is_json:
        return jsonify({'success': True, 'post': new_post.to_dict()})
    else:
        posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
        posts_dict = [post.to_dict() for post in posts]
        return render_template('admin_panel.html', posts=posts_dict, success='Post created successfully!')

@app.route('/admin/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    """Delete blog post"""
    if not session.get('admin_authenticated'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Find and delete the post
    post = BlogPost.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        message = 'Post deleted successfully!'
        success = True
    else:
        message = 'Post not found!'
        success = False
    
    # Get updated posts list
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    posts_dict = [post.to_dict() for post in posts]
    
    if success:
        return render_template('admin_panel.html', posts=posts_dict, success=message)
    else:
        return render_template('admin_panel.html', posts=posts_dict, error=message)

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_authenticated', None)
    return redirect(url_for('index'))



@app.route('/api/posts')
def api_posts():
    """API endpoint for posts (for JavaScript compatibility)"""
    category_filter = request.args.get('type', 'all')
    
    if category_filter == 'all' or category_filter == 'blog':
        posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    else:
        posts = BlogPost.query.filter_by(category=category_filter).order_by(BlogPost.created_at.desc()).all()
    
    posts_dict = [post.to_dict() for post in posts]
    return jsonify(posts_dict)

# Initialize database when app starts
init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))