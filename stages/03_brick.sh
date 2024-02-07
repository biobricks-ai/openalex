#!/usr/bin/env bash

set -euo pipefail

# Directory containing the .csv.gz files
input_dir="csv"
# Directory where the .parquet files will be stored
output_dir="brick"

# Create output directory if it doesn't exist
mkdir -p "$output_dir"

# Loop through each .csv.gz file in the input directory
for file in "$input_dir"/*.csv.gz; do
    # Extract the base name of the file without the .csv.gz extension
    base_name=$(basename "$file" .csv.gz)

    # Construct the output file path
    output_file="$output_dir/$base_name.parquet"

    # Execute the conversion command
    python3 stages/03_csv2parquet.py "$file" "$output_file"

    # The temporary CSV file will be automatically removed at script exit
done

echo "Conversion completed."
