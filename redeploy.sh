#!/bin/bash

# Print status
echo "Starting game redeployment..."

# Build the executable
echo "Building executable..."
python build.py

# Check if build was successful
if [ ! -f "dist/RingetteGame.exe" ]; then
    echo "Error: Build failed - executable not found"
    exit 1
fi

# Copy executable to docs directory
echo "Copying executable to docs directory..."
cp dist/RingetteGame.exe docs/

# Add changes to git
echo "Committing changes..."
git add docs/RingetteGame.exe

# Check if there are any changes to commit
if git diff --cached --quiet; then
    echo "No changes to commit - executable is up to date"
else
    # Commit and push changes
    git commit -m "Update game executable"
    echo "Pushing changes to GitHub..."
    git push
    echo "Deployment complete! The game will be available at https://BKrowchuk.github.io/RingetteGame/"
fi 