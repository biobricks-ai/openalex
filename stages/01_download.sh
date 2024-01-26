#!/usr/bin/env bash

# Script to download files

# Get local [ath]
localpath=$(pwd)
echo "Local path: $localpath"

# Create download directory
dlpath="$localpath/download"
mkdir -p "$dlpath"
echo "Brick path: $dlpath"

# Retrieve the files
aws s3 sync "s3://openalex" "$dlpath" --no-sign-request

echo "Download done."
