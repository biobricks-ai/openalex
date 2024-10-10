import sys
import glob
from pathlib import Path
import subprocess
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import boto3
import botocore

print('Working directory: ', Path.cwd())

# Create directories
Path('download').mkdir(exist_ok=True)
Path('csv').mkdir(exist_ok=True)
Path('brick').mkdir(exist_ok=True)

# Download OpenAlex data

def download_file(s3,bucket,file_keys):
    local_file_path = Path('download')
    local_file_path.parent.mkdir(parents=True, exist_ok=True)
    s3.download_file(bucket, str(local_file_path))

def run_s3():
    s3 = boto3.client('s3', config=boto3.session.Config(signature_version=botocore.UNSIGNED))
    bucket = 'openalex'

    file_keys = []
    paginator = s3.get_paginator('list_objects_v2')
    for result in paginator.paginate(Bucket=bucket):
        if 'Contents' in result:
            file_keys.extend([item['Key'] for item in result['Contents']])

    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        args_list = [(s3, bucket, file_key) for file_key in file_keys]
        executor.map(download_file, args_list)
    
    print("S3 download completed")

# Processing and flattening data
def process_single_file(file):
    subprocess.run(['python', 'flatten_openalex_jsonl_v2.py', str(file)], check=True)
    print(f"Processed file: {file}")

def process_data():
    jsonl_files = glob.glob('download/**/*.gz', recursive=True)
    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        executor.map(process_single_file, jsonl_files)
    
    print("Data processing and flattening completed")

# Converting to parquet
def process_file(file):
    base_name = file.stem.removesuffix('csv')
    output_file = Path('brick') / f'{base_name}.parquet'
    subprocess.run(['python', 'csv2parquet.py', str(file), str(output_file)], check=True)
    print(f'CSV to Parquet conversion completed for {file}')

def convert_csv_to_parquet():
    files = list(Path('csv').glob('*.csv.gz'))
    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        executor.map(process_file, files)
    print('All CSV to Parquet conversions completed')



# Download OpexAlex Data
run_s3()

# Process data
process_data()

# Convert to parquet format
convert_csv_to_parquet()
