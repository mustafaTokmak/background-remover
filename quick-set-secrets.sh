#!/bin/bash

# Quick script to set GitHub secrets
# Edit the values below before running

# EDIT THESE VALUES
DOCKER_USERNAME="mustafatokmak"  # Your Docker Hub username
DOCKER_PASSWORD="your-docker-password-here"  # Your Docker Hub password/token

# Set the secrets
echo "Setting DOCKER_USERNAME..."
gh secret set DOCKER_USERNAME --body "$DOCKER_USERNAME"

echo "Setting DOCKER_PASSWORD..."
gh secret set DOCKER_PASSWORD --body "$DOCKER_PASSWORD"

echo "Setting SSH_PRIVATE_KEY..."
gh secret set SSH_PRIVATE_KEY < ~/.ssh/id_ed25519

echo "Done! Listing secrets:"
gh secret list