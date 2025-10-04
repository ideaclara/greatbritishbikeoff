#!/usr/bin/env python3
"""
Simple script to test database connection and show current posts
"""
import os
from app import app, db, BlogPost

def test_database():
    with app.app_context():
        try:
            # Test database connection
            posts = BlogPost.query.all()
            print(f"✅ Database connection successful!")
            print(f"📊 Found {len(posts)} posts in database")
            
            if posts:
                print("\n📝 Current posts:")
                for i, post in enumerate(posts, 1):
                    print(f"  {i}. {post.title} ({post.category}) - {post.date}")
            else:
                print("📭 No posts found in database")
                
            # Show database URL (without sensitive info)
            db_url = app.config['SQLALCHEMY_DATABASE_URI']
            if 'sqlite' in db_url:
                print(f"🗄️  Using SQLite: {db_url}")
            else:
                print(f"🗄️  Using PostgreSQL: {db_url.split('@')[0]}@[HIDDEN]")
                
        except Exception as e:
            print(f"❌ Database error: {e}")

if __name__ == '__main__':
    test_database()