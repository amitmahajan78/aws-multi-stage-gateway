#!/bin/bash
# Script to initialize and push the project to GitHub
# Usage: ./setup_github_repo.sh [optional commit message]

# Set default commit message
COMMIT_MESSAGE=${1:-"Initial commit: AWS API Gateway with Header-Based and Path-Based Routing"}

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: Git is not installed. Please install git first."
    exit 1
fi

# Initialize git repository (if not already initialized)
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
fi

# Add remote origin (if not already added)
if ! git remote | grep -q "origin"; then
    echo "Adding remote origin..."
    git remote add origin git@github.com:amitmahajan78/aws-multi-stage-gateway.git
fi

# Make sure we have the latest .gitignore
if [ ! -f .gitignore ]; then
    echo "Error: .gitignore file is missing. Please create it first."
    exit 1
fi

# Stage all files except those in .gitignore
echo "Staging files..."
git add .

# Commit changes
echo "Committing with message: '$COMMIT_MESSAGE'"
git commit -m "$COMMIT_MESSAGE"

# Push to GitHub
echo "Pushing to GitHub repository..."
git push -u origin main || git push -u origin master

echo "Done! Your project has been pushed to GitHub: git@github.com:amitmahajan78/aws-multi-stage-gateway.git"
echo "Visit https://github.com/amitmahajan78/aws-multi-stage-gateway to see your repository online." 