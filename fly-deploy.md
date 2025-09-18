# Fly.io Deployment Guide

## Why Fly.io?
- ✅ **Docker-first** platform
- ✅ **Built-in PostgreSQL** and Redis
- ✅ **Global edge deployment**
- ✅ **Free tier**: 3 shared-cpu VMs, 160GB bandwidth
- ✅ **Great for Docker** containers

## Quick Setup:

### 1. Install Fly CLI
```bash
curl -L https://fly.io/install.sh | sh
```

### 2. Login and Deploy
```bash
# Login to Fly.io
fly auth login

# Launch your app
fly launch

# Add PostgreSQL
fly postgres create

# Add Redis
fly redis create
```

### 3. Deploy
```bash
fly deploy
```

## Cost: Free tier available, then ~$5-10/month
