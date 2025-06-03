#!/bin/bash

# Background Remover Deployment Script
# This script helps deploy the background remover API to various platforms

set -e

echo "🚀 Background Remover Deployment Script"
echo "======================================"

# Function to display usage
usage() {
    echo "Usage: $0 [OPTION]"
    echo "Options:"
    echo "  local       - Run locally with uvicorn"
    echo "  docker      - Build and run with Docker"
    echo "  railway     - Deploy to Railway"
    echo "  render      - Deploy to Render"
    echo "  fly         - Deploy to Fly.io"
    echo "  help        - Show this help message"
    exit 1
}

# Check if command provided
if [ $# -eq 0 ]; then
    usage
fi

# Parse command
case "$1" in
    local)
        echo "📍 Starting local server..."
        echo "Installing dependencies..."
        uv sync
        echo "Starting FastAPI server..."
        uvicorn api:app --host 0.0.0.0 --port 8000 --reload
        ;;
        
    docker)
        echo "🐳 Building Docker image..."
        docker build -t background-remover .
        echo "Running Docker container..."
        docker run -p 8000:8000 background-remover
        ;;
        
    railway)
        echo "🚂 Deploying to Railway..."
        if ! command -v railway &> /dev/null; then
            echo "Railway CLI not found. Install it with: npm install -g @railway/cli"
            exit 1
        fi
        
        # Create railway.json if not exists
        if [ ! -f "railway.json" ]; then
            cat > railway.json << 'EOF'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn api:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF
        fi
        
        # Create nixpacks.toml for Python 3.12
        if [ ! -f "nixpacks.toml" ]; then
            cat > nixpacks.toml << 'EOF'
[phases.setup]
nixPkgs = ["python312", "gcc", "zlib", "libjpeg", "libpng"]

[phases.install]
cmds = ["pip install uv", "uv sync"]

[start]
cmd = "uvicorn api:app --host 0.0.0.0 --port $PORT"
EOF
        fi
        
        railway login
        railway link
        railway up
        ;;
        
    render)
        echo "🎨 Deploying to Render..."
        
        # Create render.yaml if not exists
        if [ ! -f "render.yaml" ]; then
            cat > render.yaml << 'EOF'
services:
  - type: web
    name: background-remover
    runtime: python
    buildCommand: "pip install uv && uv sync"
    startCommand: "uvicorn api:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.12.0
EOF
        fi
        
        echo "render.yaml created. Please:"
        echo "1. Go to https://render.com/dashboard"
        echo "2. Create a new Web Service"
        echo "3. Connect your GitHub repository"
        echo "4. Render will automatically detect render.yaml"
        ;;
        
    fly)
        echo "✈️ Deploying to Fly.io..."
        if ! command -v flyctl &> /dev/null; then
            echo "Fly CLI not found. Install it from: https://fly.io/docs/hands-on/install-flyctl/"
            exit 1
        fi
        
        # Create fly.toml if not exists
        if [ ! -f "fly.toml" ]; then
            flyctl launch --no-deploy --name background-remover
        fi
        
        # Update fly.toml with proper configuration
        cat > fly.toml << 'EOF'
app = "background-remover"
primary_region = "sjc"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8080"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[services]]
  protocol = "tcp"
  internal_port = 8080
  
  [[services.ports]]
    port = 80
    handlers = ["http"]
    
  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]
EOF
        
        flyctl deploy
        ;;
        
    help)
        usage
        ;;
        
    *)
        echo "Unknown option: $1"
        usage
        ;;
esac