# Great British Bike Off

A cycling and food blog built with Python Flask, featuring a complete admin panel and YouTube integration.

## 🚀 Features

- **Python Flask Backend**: Server-side rendering with Jinja2 templates
- **Admin Panel**: Create, view, and delete blog posts
- **YouTube Integration**: Automatic video embedding and thumbnails
- **Category Filtering**: Cycling, Food, Travel, Gear categories
- **Responsive Design**: Works on all devices
- **Secure Authentication**: Environment variable password protection

## 🛠 Local Development

### Prerequisites
- Python 3.9+
- pip

### Setup
1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables** (optional):
   ```bash
   export ADMIN_PASSWORD="your-secure-password"
   export SECRET_KEY="your-secret-key"
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the site**:
   - Main site: http://localhost:5000
   - Admin panel: http://localhost:5000/admin
   - Default password: `bikeoff2025`

## 📁 Project Structure

```
greatbritishbikeoff/
├── app.py                 # Main Flask application
├── templates/             # Jinja2 templates
│   ├── base.html         # Base template
│   ├── index.html        # Main blog page
│   ├── post.html         # Individual post view
│   ├── admin_login.html  # Admin login
│   └── admin_panel.html  # Admin dashboard
├── static/
│   └── css/
│       └── styles.css    # All CSS styles
├── requirements.txt      # Python dependencies
└── Procfile              # For deployment
```

## 🌐 Deployment to Render

This project is configured for easy deployment to Render via GitHub:

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### Step 2: Deploy on Render
1. **Go to [Render.com](https://render.com)** and sign up/login
2. **Connect GitHub** account
3. **Create New Web Service**
4. **Select your repository**: `greatbritishbikeoff`
5. **Configure deployment**:
   - **Name**: `great-british-bike-off`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free` (or paid for better performance)

### Step 3: Add PostgreSQL Database
1. **In Render dashboard**, go to your web service
2. **Click "Environment"** tab
3. **Add PostgreSQL database**:
   - Click **"New PostgreSQL"**
   - Name: `greatbritishbikeoff-db`
   - Render will automatically set `DATABASE_URL`

### Step 4: Set Environment Variables
In Render dashboard, add these environment variables:
- **Key**: `ADMIN_PASSWORD` **Value**: `your-secure-password`
- **Key**: `SECRET_KEY` **Value**: `your-random-secret-key`
- **Key**: `DATABASE_URL` **Value**: `(automatically set by PostgreSQL addon)`

### Step 5: Deploy
- Click **Create Web Service**
- Render will automatically build and deploy your app
- Your blog will be live at: `https://great-british-bike-off.onrender.com`

## 🔧 Environment Variables

Set these in Render dashboard:

- `ADMIN_PASSWORD`: Your secure admin password (required)
- `SECRET_KEY`: Flask secret key for sessions (required)
- `DATABASE_URL`: PostgreSQL connection string (automatically set by Render)
- `INIT_SAMPLE_DATA`: Set to 'true' only if you want sample data (optional)
- `PORT`: Port number (automatically set by Render)

## 🗄️ Database Setup

### Local Development:
- Uses SQLite database file: `instance/blog.db`
- Posts persist between app restarts
- No sample data added automatically

### Production (Render):
- Uses PostgreSQL database
- Must add PostgreSQL addon in Render dashboard
- Posts persist permanently across deployments

## 🚴‍♂️ Usage

1. **Visit the main site** to see blog posts
2. **Filter by category** using the navigation buttons
3. **Click "Read More"** to view full posts
4. **Access admin panel** at `/admin`
5. **Create new posts** with YouTube integration
6. **Manage existing posts** from the admin dashboard

## 🔒 Security

- Password-protected admin panel
- Environment variable configuration
- Session-based authentication
- CSRF protection ready (can be added)
- Input validation and sanitization

## 🎯 Features

### Blog Management
- **Create Posts**: Rich text content with YouTube integration
- **Category System**: Cycling, Food, Travel, Gear categories
- **YouTube Videos**: Automatic thumbnail generation and embedding
- **Responsive Design**: Works perfectly on mobile and desktop

### Admin Panel
- **Secure Login**: Environment variable password protection
- **Post Management**: Create, view, and delete posts
- **YouTube Integration**: Paste YouTube URLs for automatic embedding
- **Session Management**: Secure admin authentication

This Flask blog is production-ready and optimized for Render deployment! 🚀