# VPS Deployment Guide

This guide explains how to deploy the Background Remover API to your VPS using GitHub Actions.

## Prerequisites

1. A VPS with Ubuntu 20.04+ (your server: 5.189.174.110)
2. SSH access to the server
3. GitHub repository secrets configured

## GitHub Secrets Setup

Add these secrets to your GitHub repository (`Settings` → `Secrets and variables` → `Actions`):

### For VPS Deployment:
1. **VPS_HOST**: `5.189.174.110`
2. **VPS_USERNAME**: `mustafa`
3. **VPS_PORT**: `22` (or your custom SSH port)
4. **VPS_SSH_KEY**: Your private SSH key

### For Docker Hub (Optional):
5. **DOCKER_USERNAME**: Your Docker Hub username
6. **DOCKER_PASSWORD**: Your Docker Hub password or access token

### How to add SSH key:
```bash
# Generate SSH key if you don't have one
ssh-keygen -t ed25519 -C "github-actions"

# Copy the public key to your server
ssh-copy-id mustafa@5.189.174.110

# Copy the private key content
cat ~/.ssh/id_ed25519
```

Copy the entire private key (including `-----BEGIN OPENSSH PRIVATE KEY-----` and `-----END OPENSSH PRIVATE KEY-----`) and add it as `VPS_SSH_KEY` secret.

## Automatic Deployment

Once secrets are configured, the API will automatically deploy when you push to the `main` branch.

## Manual Deployment

1. Go to `Actions` tab in GitHub
2. Select `Deploy to VPS` workflow
3. Click `Run workflow`

## First-Time Server Setup

If deploying for the first time, SSH into your server and run:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install basic dependencies
sudo apt install -y git curl build-essential

# The GitHub Action will handle the rest!
```

## Service Management

After deployment, you can manage the service:

```bash
# Check status
sudo systemctl status background-remover

# View logs
sudo journalctl -u background-remover -f

# Restart service
sudo systemctl restart background-remover

# Stop service
sudo systemctl stop background-remover
```

## Nginx Management

```bash
# Check nginx status
sudo systemctl status nginx

# Test configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

## Access Your API

Once deployed, your API will be available at:
- **Base URL**: http://5.189.174.110/
- **API Docs**: http://5.189.174.110/docs
- **Health Check**: http://5.189.174.110/health

## Troubleshooting

### Check Application Logs
```bash
sudo journalctl -u background-remover -n 100 --no-pager
```

### Check Nginx Logs
```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Manual Deployment
If automatic deployment fails, you can deploy manually:

```bash
# SSH into server
ssh mustafa@5.189.174.110

# Navigate to app directory
cd ~/apps/background-remover

# Pull latest changes
git pull origin main

# Activate virtual environment
source .venv/bin/activate

# Update dependencies
uv sync

# Restart service
sudo systemctl restart background-remover
```

## Security Recommendations

1. **Firewall**: Configure UFW
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

2. **SSL Certificate**: Use Let's Encrypt
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```

3. **Fail2ban**: Protect against brute force
   ```bash
   sudo apt install fail2ban
   sudo systemctl enable fail2ban
   ```

## Performance Tuning

1. **Increase file upload limit** in nginx config if needed
2. **Add swap** if server has limited RAM:
   ```bash
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

## Monitoring

Consider setting up:
- Uptime monitoring (e.g., UptimeRobot)
- Resource monitoring (e.g., htop, netdata)
- Log aggregation (e.g., Papertrail)