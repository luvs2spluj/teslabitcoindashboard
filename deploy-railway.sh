#!/bin/bash

# Railway Deployment Script
echo "🚀 Deploying Tesla Financial App to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Login to Railway
echo "🔐 Logging into Railway..."
railway login

# Initialize project
echo "🏗️ Initializing Railway project..."
railway init

# Add PostgreSQL database
echo "🗄️ Adding PostgreSQL database..."
railway add postgresql

# Add Redis cache
echo "⚡ Adding Redis cache..."
railway add redis

# Set environment variables
echo "🔧 Setting environment variables..."
railway variables set NODE_ENV=production
railway variables set PYTHON_ENV=production

# Deploy
echo "🚀 Deploying to Railway..."
railway up

echo "✅ Deployment complete!"
echo "🌐 Your app will be available at: https://your-app-name.railway.app"
echo "📊 Database: PostgreSQL (managed by Railway)"
echo "⚡ Cache: Redis (managed by Railway)"
echo "💰 Cost: ~$0-5/month (Railway free tier)"
