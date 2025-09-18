#!/usr/bin/env python3
"""
Railway deployment entry point for Tesla Bitcoin Dashboard
This file imports and runs the FastAPI application from apps/api
"""

import sys
import os

# Add the apps/api directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'apps', 'api'))

# Import and run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    from app.main import app
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
