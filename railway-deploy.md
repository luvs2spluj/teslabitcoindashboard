# Railway Deployment Guide

## Why Railway?
- ✅ **Docker-native** - runs your containers directly
- ✅ **Built-in PostgreSQL** - no external database needed
- ✅ **Automatic deployments** from GitHub
- ✅ **Free tier**: $5/month credit (usually covers small apps)
- ✅ **Simple setup** - just connect GitHub repo

## Quick Setup:

### 1. Install Railway CLI
```bash
npm install -g @railway/cli
```

### 2. Login and Deploy
```bash
# Login to Railway
railway login

# Initialize project
railway init

# Add PostgreSQL database
railway add postgresql

# Deploy
railway up
```

### 3. Environment Variables
Railway will automatically set:
- `DATABASE_URL` (PostgreSQL)
- `REDIS_URL` (if you add Redis)
- `PORT` (automatically assigned)

### 4. Connect GitHub (Auto-deploy)
1. Go to Railway dashboard
2. Connect your GitHub repo
3. Enable auto-deploy on push

## Cost: ~$0-5/month for small apps
