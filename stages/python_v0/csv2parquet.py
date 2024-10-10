import pandas as pd
import fastparquet
from pathlib import Path
import sys

InFileName = sys.argv[1]
OutFileName = sys.argv[2]

print(f"csv2parquet: Converting file {InFileName}")

chunk_size = 10000  # Adjust based on your system's memory capacity

schemas = {
    "authors_ids": pa.schema([
        ('author_id', pa.string()),
        ('openalex', pa.string()),
        ('orcid', pa.string()),
        ('scopus', pa.string()),
        ('twitter', pa.string()),
        ('wikipedia', pa.string()),
        ('mag', pa.float64()),
    ]),
    "works_biblio": pa.schema([
        ('work_id', pa.string()),
        ('volume', pa.string()),
        ('issue', pa.string()),
        ('first_page', pa.string()),
        ('last_page', pa.string()),
    ]),
}

dtypes = {
    "authors_ids": {
        "author_id": "string",
        "openalex": "string",
        "orcid": "string",
        "scopus": "string",
        "twitter": "string",
        "wikipedia": "string",
        "mag": "float64",
    },
    "works_biblio": {
        "work_id": "string",
        "volume": "string",
        "issue": "string",
        "first_page": "string",
        "last_page": "string",
    },
}

base_filename = Path(InFileName).stem 
dtype = dtypes.get(base_filename)

print(f"Using dtype: {dtype}")

if dtype:
    rows = pd.read_csv(InFileName, sep=',', dtype=dtype, compression='gzip', chunksize=chunk_size)
else:
    rows = pd.read_csv(InFileName, sep=',', compression='gzip', chunksize=chunk_size)

first_chunk = True
for chunk in rows:
    if first_chunk:
        fastparquet.write(OutFileName, chunk, compression='snappy', append=False)
        first_chunk = False
    else:
        fastparquet.write(OutFileName, chunk, compression='snappy', append=True)