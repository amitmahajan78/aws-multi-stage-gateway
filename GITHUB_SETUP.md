# Using Multiple GitHub Accounts

This document explains how to set up your project to work with multiple GitHub accounts, specifically when your local Git configuration uses a different username than the repository owner.

## Problem

When you have multiple GitHub accounts (e.g., personal and work), you might face issues when pushing to repositories owned by different accounts:

1. Your global Git configuration might use a different user name and email than the repository owner
2. GitHub uses SSH keys for authentication, but each key can only be linked to one GitHub account
3. Permission errors occur when trying to push to a repository owned by a different GitHub account

## Solution: SSH Configuration with Per-Host Settings

We've provided two scripts to automate the setup process:

1. `setup_github_ssh.sh` - Configures SSH for multiple GitHub accounts
2. `setup_github_repo.sh` - Initializes and pushes the repository

## Automated Setup (Recommended)

### Step 1: Configure SSH for Multiple GitHub Accounts

Run the SSH setup script:

```bash
./setup_github_ssh.sh
```

This script will:
- Generate a new SSH key specifically for the target GitHub account (if needed)
- Configure your SSH settings to use different keys for different GitHub accounts
- Add a special host entry in your SSH config
- Test the SSH connection to ensure it works
- Display the public key for you to add to GitHub

### Step 2: Add the SSH Key to GitHub

1. Copy the public key displayed by the script
2. Go to [GitHub SSH Keys Settings](https://github.com/settings/keys)
3. Click "New SSH key"
4. Give the key a descriptive title (e.g., "Project Key for amitmahajan78")
5. Paste the entire public key
6. Click "Add SSH key"

### Step 3: Push Your Repository

Run the repository setup script:

```bash
./setup_github_repo.sh
```

This script will:
- Initialize Git (if not already done)
- Configure repository-specific user settings (optional)
- Set the remote origin with the special SSH host format
- Commit your code
- Push to GitHub

## Manual Setup (Alternative)

If you prefer to set up everything manually:

### 1. Create a New SSH Key

```bash
ssh-keygen -t ed25519 -C "your_email@example.com" -f ~/.ssh/github_amitmahajan78
```

### 2. Configure SSH

Add this to your `~/.ssh/config` file:

```
Host github.com-amitmahajan78
    HostName github.com
    User git
    IdentityFile ~/.ssh/github_amitmahajan78
    IdentitiesOnly yes
```

### 3. Add the SSH Key to GitHub

```bash
cat ~/.ssh/github_amitmahajan78.pub
```

Copy the output and add it to GitHub under Settings > SSH and GPG keys.

### 4. Test the Connection

```bash
ssh -T git@github.com-amitmahajan78
```

You should see a message like: "Hi amitmahajan78! You've successfully authenticated..."

### 5. Set Up Your Repository

```bash
git remote add origin git@github.com-amitmahajan78:amitmahajan78/repository-name.git
git push -u origin main
```

## Troubleshooting

### SSH Connection Issues

If you see "Permission denied (publickey)" when testing the SSH connection:

1. **Verify your public key was added to GitHub**
   - Make sure you copied the ENTIRE public key
   - Check that it's added to the correct GitHub account

2. **Check SSH configuration**
   - Ensure your SSH config file has the correct host entry
   - Verify the path to your SSH key is correct
   - Run `ssh -vT git@github.com-amitmahajan78` for verbose output

3. **Check SSH agent**
   - Run `ssh-add -l` to list loaded keys
   - If your key isn't listed, add it: `ssh-add ~/.ssh/github_amitmahajan78`

4. **File permissions**
   - SSH keys should have restricted permissions:
   ```bash
   chmod 600 ~/.ssh/github_amitmahajan78
   chmod 644 ~/.ssh/github_amitmahajan78.pub
   ```

### Push Issues

If you're still having trouble pushing to GitHub:

1. **Verify remote URL**
   ```bash
   git remote -v
   ```
   The URL should be in the format: `git@github.com-amitmahajan78:amitmahajan78/repository-name.git`

2. **Update remote URL**
   ```bash
   git remote set-url origin git@github.com-amitmahajan78:amitmahajan78/repository-name.git
   ```

3. **Check repository existence**
   - Ensure the repository exists on GitHub
   - Make sure you have the correct permissions

## Additional Resources

- [GitHub's guide on connecting with SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [Managing multiple GitHub accounts](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-your-personal-account/maintaining-ownership-continuity-of-your-personal-account-repositories) 