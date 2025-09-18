#!/bin/bash

# Development Setup Script (without Docker)
echo "🚀 Setting up Financial App Development Environment"

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed"
    exit 1
fi

echo "✅ Python 3: $(python3 --version)"
echo "✅ Node.js: $(node --version)"

# Install pnpm if not available
if ! command -v pnpm &> /dev/null; then
    echo "📦 Installing pnpm..."
    npm install -g pnpm
fi

# Install dependencies
echo "📦 Installing dependencies..."
pnpm install

# Set up Python virtual environment
echo "🐍 Setting up Python virtual environment..."
cd apps/api
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ../..

# Create environment file
echo "⚙️ Setting up environment variables..."
if [ ! -f .env.local ]; then
    cp .env.example .env.local
    echo "📝 Created .env.local - please edit with your API keys"
fi

echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Edit .env.local with your API keys"
echo "2. Start the API server:"
echo "   cd apps/api && source venv/bin/activate && python -m uvicorn app.main:app --reload"
echo "3. Start the web server (in another terminal):"
echo "   cd apps/web && npm run dev"
echo ""
echo "🌐 Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"