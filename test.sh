#!/bin/bash

# Set the destination directory
DEST_DIR="../roey-musetalk"

# Create the destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Get the list of files from git status, excluding deleted files
FILES=$(git status --porcelain | grep -v '^ D' | sed 's/^...//')

# Copy each file to the destination directory
for file in $FILES; do
    # Create the directory structure in the destination
    mkdir -p "$DEST_DIR/$(dirname "$file")"
    # Copy the file
    cp -r "$file" "$DEST_DIR/$file"
done

echo "Files copied to $DEST_DIR"