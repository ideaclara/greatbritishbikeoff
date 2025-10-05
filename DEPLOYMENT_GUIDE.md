# 🚀 Deployment Guide - Fix Database Persistence

## 🔍 Current Issue
Your blog posts reset because you're not using a persistent database in production.

## ✅ Solution: Set Up PostgreSQL on Render

### Step 1: Add PostgreSQL Database
1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Click "New +"** → **"PostgreSQL"**
3. **Configure**:
   - **Name**: `greatbritishbikeoff-db`
   - **Database**: `greatbritishbikeoff`
   - **User**: `greatbritishbikeoff`
   - **Region**: Same as your web service
   - **Plan**: Free (or paid for better performance)
4. **Click "Create Database"**

### Step 2: Connect Database to Web Service
1. **Go to your Web Service** in Render dashboard
2. **Click "Environment"** tab
3. **Render should automatically add**:
   - **Key**: `DATABASE_URL`
   - **Value**: `postgresql://user:pass@host:port/dbname`
   - (If not automatic, copy from PostgreSQL database dashboard)

### Step 3: Set Build Number (Optional)
Add environment variable:
- **Key**: `BUILD_NUMBER`
- **Value**: `v1.0` (or any version you want)

### Step 4: Redeploy
1. **Go to "Deploys"** tab
2. **Click "Trigger Deploy"**
3. **Wait for deployment** to complete
4. **Check logs** - should show "Production database detected"

## 🎯 What This Fixes

### Before (Current Issue):
- **Local**: SQLite file (gets reset when you restart)
- **Production**: No persistent database → posts disappear

### After (Fixed):
- **Local**: SQLite file (persists between restarts)
- **Production**: PostgreSQL database (persists forever)

## 🧪 Test Your Fix

### Local Testing:
```bash
# Run the app
python app.py

# In another terminal, test database
python test_db.py
```

### Production Testing:
1. **Deploy to Render** with PostgreSQL
2. **Create a test post** via admin panel
3. **Trigger a redeploy** 
4. **Check if post still exists** ✅

## 🔧 Environment Variables Needed

Set these in Render dashboard:

```
ADMIN_PASSWORD=your-secure-password
SECRET_KEY=your-random-secret-key
DATABASE_URL=postgresql://... (auto-set by PostgreSQL addon)
```

## 🚨 Important Notes

- **Don't set `INIT_SAMPLE_DATA=true`** in production (only for testing)
- **PostgreSQL is required** for persistent storage on Render
- **Local SQLite works fine** for development
- **Your posts will persist** once PostgreSQL is set up

## ✅ Success Indicators

You'll know it's working when:
- ✅ Render logs show: "Found X existing posts in database"
- ✅ Posts survive redeployments
- ✅ Admin panel shows your actual posts
- ✅ No more "creating sample data" messages