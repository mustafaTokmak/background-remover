# Deployment Guide

This guide explains how to deploy the Background Remover API using GitHub Actions.

## GitHub Actions Setup

### Required Secrets

Configure these secrets in your GitHub repository settings (`Settings` → `Secrets and variables` → `Actions`):

#### For Railway Deployment
- `RAILWAY_TOKEN`: Your Railway API token
  1. Go to [Railway Dashboard](https://railway.app/account/tokens)
  2. Create a new token
  3. Add it as a GitHub secret

#### For Render Deployment
- `RENDER_API_KEY`: Your Render API key
  1. Go to [Render Dashboard](https://dashboard.render.com/u/settings/api-keys)
  2. Create a new API key
  3. Add it as a GitHub secret
- `RENDER_SERVICE_ID`: Your Render service ID
  1. Create a new Web Service on Render
  2. Find the service ID in the service settings
  3. Add it as a GitHub secret

#### For Fly.io Deployment
- `FLY_API_TOKEN`: Your Fly.io API token
  1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
  2. Run `fly auth token`
  3. Add the token as a GitHub secret

#### For Docker Hub (Optional)
- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub password or access token

## Automatic Deployment

### On Push to Main
- **CI Pipeline**: Runs tests and linting
- **Docker Build**: Builds and pushes to GitHub Container Registry
- **Railway Deploy**: Automatically deploys to Railway (if configured)

### Manual Deployment
1. Go to `Actions` tab in your GitHub repository
2. Select `Deploy` workflow
3. Click `Run workflow`
4. Choose deployment target:
   - `railway`: Deploy to Railway only
   - `render`: Deploy to Render only
   - `fly`: Deploy to Fly.io only
   - `all`: Deploy to all platforms

## Platform-Specific Configuration

### Railway
The project includes:
- `railway.json`: Railway configuration
- `nixpacks.toml`: Build configuration for Python 3.12

### Render
The project includes:
- `render.yaml`: Render blueprint configuration

### Fly.io
The project includes:
- `fly.toml`: Fly.io configuration

### Docker
The project includes:
- `Dockerfile`: Multi-stage build optimized for production
- Images are automatically pushed to:
  - GitHub Container Registry: `ghcr.io/yourusername/background-remover`
  - Docker Hub: `yourusername/background-remover` (if configured)

## Local Deployment

Use the deployment script:
```bash
./deploy.sh local    # Run locally
./deploy.sh docker   # Run with Docker
./deploy.sh railway  # Deploy to Railway (requires CLI)
./deploy.sh render   # Generate Render configuration
./deploy.sh fly      # Deploy to Fly.io (requires CLI)
```

## Environment Variables

No environment variables are required for basic operation. The API will:
- Use port 8000 by default (or `$PORT` if set)
- Download AI models on first use
- Store models in the container/instance

## Monitoring

- Railway: Built-in metrics and logs
- Render: Built-in metrics and logs
- Fly.io: `fly logs` and `fly status`
- Docker: Container logs via `docker logs`

## Troubleshooting

### Common Issues

1. **Out of Memory**: The AI models require ~2GB RAM minimum
2. **Slow First Request**: Models are downloaded on first use
3. **Port Issues**: Ensure the app uses `$PORT` environment variable

### Health Check

All deployments include a health check endpoint at `/` that returns:
```json
{
  "message": "Background Remover API",
  "endpoints": {...}
}
```