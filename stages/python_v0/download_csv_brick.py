import sys
import glob
from pathlib import Path
import subprocess
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
import boto3
from botocore import UNSIGNED
from botocore.client import Config

import csv2parquet
import flatten_openalex_jsonl

print('Working directory: ', Path.cwd())

# Create directories
Path('download').mkdir(exist_ok=True)
Path('csv').mkdir(exist_ok=True)
Path('brick').mkdir(exist_ok=True)

# Download OpenAlex data

def download_file(s3, bucket, file_key):
    local_file_path = Path('download') / file_key
    local_file_path.parent.mkdir(parents=True, exist_ok=True)
    s3.download_file(bucket, file_key, str(local_file_path))

def run_s3():
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    bucket = 'openalex'

    file_keys = []
    paginator = s3.get_paginator('list_objects_v2')
    for result in paginator.paginate(Bucket=bucket):
        if 'Contents' in result:
            file_keys.extend([item['Key'] for item in result['Contents']])

    with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        executor.map(lambda key: download_file(s3, bucket, key), file_keys)
    
    print("S3 download completed")

# Processing and flattening data
def process_single_file(file):
    flatten_openalex_jsonl.run_flattening(str(file))
    print(f"Processed file: {file}")

def process_data():
    jsonl_files = glob.glob('download/**/*.gz', recursive=True)
    with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        executor.map(process_single_file, jsonl_files)
    
    print("Data processing and flattening completed")

# Converting to parquet
def process_file(file):
    base_name = file.stem.removesuffix('csv')
    output_file = Path('brick') / f'{base_name}.parquet'
    csv2parquet.csv_to_parquet(str(file), str(output_file))
    print(f'CSV to Parquet conversion completed for {file}')

def convert_csv_to_parquet():
    files = list(Path('csv').glob('*.csv.gz'))
    with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        executor.map(process_file, files)
    print('All CSV to Parquet conversions completed')



# Download OpexAlex Data
run_s3()

# Process data
process_data()

# Convert to parquet format
convert_csv_to_parquet()
