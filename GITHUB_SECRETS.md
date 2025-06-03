# GitHub Secrets Setup

To deploy using the GitHub Actions workflow, you need to set the following secrets in your repository:

## Required Secrets

1. **DOCKER_USERNAME**
   - Your Docker Hub username
   - Example: `yourdockerhubusername`

2. **DOCKER_PASSWORD**
   - Your Docker Hub password or access token
   - Recommended: Use a Docker Hub access token instead of password
   - Create token at: https://hub.docker.com/settings/security

3. **SSH_PRIVATE_KEY**
   - Your SSH private key for accessing the server
   - This should be the private key that pairs with the public key on your server
   - Example: Contents of your `~/.ssh/id_rsa` or `~/.ssh/id_ed25519` file

## How to Add Secrets

1. Go to your GitHub repository
2. Click on **Settings** tab
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Add each secret with the exact names above

## Getting Your SSH Private Key

If you need to get your SSH private key:

```bash
# For RSA key
cat ~/.ssh/id_rsa

# For ED25519 key
cat ~/.ssh/id_ed25519
```

Copy the entire output including the BEGIN and END lines.

## Server Setup Requirements

Make sure your server (5.189.174.110) has:
- Docker installed
- Your SSH public key in `/home/mustafa/.ssh/authorized_keys`
- Port 3002 open in firewall