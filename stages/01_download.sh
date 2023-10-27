#!/usr/bin/env bash

# Script to download files

# Get local [ath]
localpath=$(pwd)
echo "Local path: $localpath"

# Create brick directory
brickpath="$localpath/brick"
mkdir -p $brickpath
echo "Brick path: $brickpath"

# Retrieve the files
aws s3 sync "s3://openalex" "$brickpath" --no-sign-request

echo "Download done."
