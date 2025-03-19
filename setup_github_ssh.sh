#!/bin/bash
# Script to set up a dedicated SSH key for pushing to repositories under a specific GitHub account
# This is useful when you need to push to a repository owned by a different GitHub user

# GitHub user information
GITHUB_USER="amitmahajan78"
REPO_NAME="aws-multi-stage-gateway"
SSH_KEY_NAME="id_ed25519_github_${GITHUB_USER}"
SSH_KEY_PATH="$HOME/.ssh/${SSH_KEY_NAME}"

echo "Setting up dedicated SSH key for GitHub user: ${GITHUB_USER}"
echo "====================================================="

# Check if SSH key already exists
if [ -f "${SSH_KEY_PATH}" ]; then
    echo "SSH key already exists at ${SSH_KEY_PATH}"
    read -p "Do you want to create a new key anyway? (y/n): " create_new_key
    if [[ "$create_new_key" =~ ^[Yy]$ ]]; then
        # Generate new SSH key
        echo "Generating new SSH key..."
        ssh-keygen -t ed25519 -C "${GITHUB_USER}@github.com" -f "${SSH_KEY_PATH}"
    else
        echo "Using existing SSH key."
    fi
else
    # Generate new SSH key
    echo "Generating new SSH key..."
    ssh-keygen -t ed25519 -C "${GITHUB_USER}@github.com" -f "${SSH_KEY_PATH}"
fi

# Ensure proper permissions
chmod 600 "${SSH_KEY_PATH}"
chmod 644 "${SSH_KEY_PATH}.pub"

# Start SSH agent if not running
eval "$(ssh-agent -s)"

# Add key to SSH agent
ssh-add "${SSH_KEY_PATH}"

# Create or update SSH config file
SSH_CONFIG_PATH="$HOME/.ssh/config"
if [ ! -f "${SSH_CONFIG_PATH}" ]; then
    touch "${SSH_CONFIG_PATH}"
    chmod 600 "${SSH_CONFIG_PATH}"
fi

# Check if config entry already exists
if grep -q "Host github.com-${GITHUB_USER}" "${SSH_CONFIG_PATH}"; then
    echo "SSH config entry for ${GITHUB_USER} already exists."
else
    echo "Adding SSH config entry for ${GITHUB_USER}..."
    cat >> "${SSH_CONFIG_PATH}" << EOF

# GitHub account: ${GITHUB_USER}
Host github.com-${GITHUB_USER}
    HostName github.com
    User git
    IdentityFile ${SSH_KEY_PATH}
    IdentitiesOnly yes
EOF
fi

# Display the public key for the user to add to GitHub
echo ""
echo "====================================================="
echo "IMPORTANT: Add this SSH public key to your GitHub account (${GITHUB_USER}):"
echo "https://github.com/settings/keys"
echo "---------------------------------------------------"
cat "${SSH_KEY_PATH}.pub"
echo "---------------------------------------------------"
echo ""
echo "Copy the ENTIRE key above, including 'ssh-ed25519' at the beginning"
echo "and the email address at the end."
echo ""
echo "After adding the key to GitHub, you can use this modified repository URL:"
echo "git@github.com-${GITHUB_USER}:${GITHUB_USER}/${REPO_NAME}.git"
echo ""

# Update the remote for the current repository
if [ -d .git ]; then
    echo "Updating remote URL for the current repository..."
    git remote set-url origin "git@github.com-${GITHUB_USER}:${GITHUB_USER}/${REPO_NAME}.git"
    echo "Remote URL updated to use the SSH key for ${GITHUB_USER}."
fi

# Wait for user to add key to GitHub
read -p "Have you added the SSH key to your GitHub account? (y/n): " key_added
if [[ "$key_added" =~ ^[Yy]$ ]]; then
    # Test SSH connection with verbose output to help diagnose issues
    echo "Testing SSH connection to GitHub with the new key..."
    echo "Command: ssh -vT git@github.com-${GITHUB_USER}"
    ssh -vT "git@github.com-${GITHUB_USER}"
    
    # Check the exit code
    if [ $? -eq 0 ] || [ $? -eq 1 ]; then
        # GitHub's SSH test command returns 1 even when authentication succeeds
        echo "SSH connection successful! You should have seen a message from GitHub."
        echo "You can now push your repository."
    else
        echo "SSH connection failed. Please check:"
        echo "1. That you added the key correctly to GitHub"
        echo "2. That your SSH config file is correct"
        echo "3. That the key is loaded in the SSH agent (run 'ssh-add -l')"
    fi
else
    echo "Please add the SSH key to your GitHub account before pushing."
fi

# Update the setup_github_repo.sh script to use the correct URL format if it exists
if [ -f "setup_github_repo.sh" ]; then
    echo "Updating setup_github_repo.sh to use the correct SSH URL format..."
    sed -i.bak "s|GITHUB_REPO=\"git@github.com:${GITHUB_USER}/${REPO_NAME}.git\"|GITHUB_REPO=\"git@github.com-${GITHUB_USER}:${GITHUB_USER}/${REPO_NAME}.git\"|g" setup_github_repo.sh
    echo "setup_github_repo.sh updated."
fi

echo ""
echo "SSH setup completed!"
echo ""
echo "To push your repository to GitHub:"
echo "1. Make sure the repository exists at: https://github.com/${GITHUB_USER}/${REPO_NAME}"
echo "2. Run: ./setup_github_repo.sh" 