#!/bin/bash
# Script to initialize and push the project to GitHub
# Usage: ./setup_github_repo.sh [optional commit message]

# Set default commit message
COMMIT_MESSAGE=${1:-"Initial commit: AWS API Gateway with Header-Based and Path-Based Routing"}

# GitHub repository information
GITHUB_USER="amitmahajan78"
REPO_NAME="aws-multi-stage-gateway"
# Use the special SSH host format to ensure the correct SSH key is used
GITHUB_REPO="git@github.com-${GITHUB_USER}:${GITHUB_USER}/${REPO_NAME}.git"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: Git is not installed. Please install git first."
    exit 1
fi

# Display current Git configuration
echo "Current Git configuration:"
git config user.name
git config user.email

# Ask if user wants to configure Git for this repository
read -p "Do you want to configure Git user name and email for this repository? (y/n): " setup_git_config
if [[ "$setup_git_config" =~ ^[Yy]$ ]]; then
    read -p "Enter your name for Git commits: " git_name
    read -p "Enter your email for Git commits: " git_email
    
    # Configure Git locally for this repository
    git config user.name "$git_name"
    git config user.email "$git_email"
    echo "Git configuration updated."
fi

# Initialize git repository (if not already initialized)
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
fi

# Make sure we have the latest .gitignore
if [ ! -f .gitignore ]; then
    echo "Error: .gitignore file is missing. Please create it first."
    exit 1
fi

# Check if SSH configuration exists
SSH_CONFIG_PATH="$HOME/.ssh/config"
if ! grep -q "Host github.com-${GITHUB_USER}" "${SSH_CONFIG_PATH}" 2>/dev/null; then
    echo "Warning: SSH configuration for ${GITHUB_USER} is not found."
    echo "Run ./setup_github_ssh.sh first to configure SSH keys properly."
    read -p "Do you want to continue anyway? (y/n): " continue_anyway
    if [[ ! "$continue_anyway" =~ ^[Yy]$ ]]; then
        echo "Aborting. Please run ./setup_github_ssh.sh first."
        exit 1
    fi
fi

# Check if GitHub repository exists
echo ""
echo "Before continuing, please ensure:"
echo "1. You've created the repository at: https://github.com/${GITHUB_USER}/${REPO_NAME}"
echo "2. You have added the appropriate SSH key to your GitHub account"
echo "3. You have the necessary permissions to push to this repository"
echo ""
read -p "Is the repository ready on GitHub? (y/n): " repo_ready
if [[ ! "$repo_ready" =~ ^[Yy]$ ]]; then
    echo "Please create the repository before continuing."
    echo "Visit: https://github.com/new"
    echo "Repository name: ${REPO_NAME}"
    echo "Make it public or private as needed."
    echo "DO NOT initialize with README, .gitignore, or license files."
    echo ""
    read -p "Press Enter when the repository is ready..."
fi

# Add remote origin (if not already added)
if ! git remote | grep -q "origin"; then
    echo "Adding remote origin..."
    git remote add origin "${GITHUB_REPO}"
else
    # Update the remote URL
    echo "Updating remote origin URL..."
    git remote set-url origin "${GITHUB_REPO}"
fi

# Stage all files except those in .gitignore
echo "Staging files..."
git add .

# Rename GITHUB_README.md to README.md if it exists
if [ -f GITHUB_README.md ]; then
    echo "Renaming GITHUB_README.md to README.md..."
    mv GITHUB_README.md README.md
    git add README.md
fi

# Commit changes
echo "Committing with message: '$COMMIT_MESSAGE'"
git commit -m "$COMMIT_MESSAGE"

# Create main branch if it doesn't exist
if ! git show-ref --quiet --verify refs/heads/main; then
    echo "Creating main branch..."
    git branch -M main
fi

# Push to GitHub with verbose output to help diagnose issues
echo "Pushing to GitHub repository..."
echo "Command: git push -v -u origin main"
git push -v -u origin main

# Check if push was successful
if [ $? -eq 0 ]; then
    echo "Success! Your project has been pushed to GitHub: https://github.com/${GITHUB_USER}/${REPO_NAME}"
    echo "Visit https://github.com/${GITHUB_USER}/${REPO_NAME} to see your repository online."
else
    echo "Push failed. Please check your SSH configuration and GitHub permissions."
    echo "You can try running: ./setup_github_ssh.sh again to refresh your SSH setup."
    echo "Make sure you've added the SSH key to your GitHub account."
    echo "Also check that the repository exists and is accessible."
fi 