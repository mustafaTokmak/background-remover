#!/bin/bash

# Script to set GitHub secrets for deployment

echo "Setting GitHub secrets for background-remover deployment..."

# Docker Hub Username
echo -n "Enter your Docker Hub username: "
read DOCKER_USERNAME
gh secret set DOCKER_USERNAME --body "$DOCKER_USERNAME"

# Docker Hub Password/Token
echo -n "Enter your Docker Hub password or access token: "
read -s DOCKER_PASSWORD
echo
gh secret set DOCKER_PASSWORD --body "$DOCKER_PASSWORD"

# SSH Private Key
echo "Enter path to your SSH private key (default: ~/.ssh/id_rsa): "
read SSH_KEY_PATH
SSH_KEY_PATH=${SSH_KEY_PATH:-~/.ssh/id_rsa}

if [ -f "$SSH_KEY_PATH" ]; then
    gh secret set SSH_PRIVATE_KEY < "$SSH_KEY_PATH"
    echo "SSH_PRIVATE_KEY set successfully"
else
    echo "SSH key file not found at $SSH_KEY_PATH"
    exit 1
fi

echo "All secrets have been set successfully!"
echo "You can verify them at: https://github.com/mustafaTokmak/background-remover/settings/secrets/actions"