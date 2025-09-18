# Render Deployment Guide

## Why Render?
- ✅ **Zero-config** Docker deployment
- ✅ **Built-in PostgreSQL**
- ✅ **Free tier** available
- ✅ **GitHub integration**
- ✅ **Automatic SSL**

## Quick Setup:

### 1. Connect GitHub
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repo

### 2. Configure Service
- **Build Command**: `docker-compose build`
- **Start Command**: `docker-compose up`
- **Environment**: Production

### 3. Add Database
1. Click "New +" → "PostgreSQL"
2. Connect to your web service
3. Environment variables auto-set

## Cost: Free tier available, then ~$7/month
