import pandas as pd
import fastparquet
from pathlib import Path
import sys


def csv_to_parquet(inputfile, outputfile):
    print(f"csv2parquet: Converting file {inputfile}")

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

    base_filename = Path(inputfile).stem 
    dtype = dtypes.get(base_filename)

    print(f"Using dtype: {dtype}")

    if dtype:
        rows = pd.read_csv(inputfile, sep=',', dtype=dtype, compression='gzip', chunksize=chunk_size)
    else:
        rows = pd.read_csv(inputfile, sep=',', compression='gzip', chunksize=chunk_size)

    first_chunk = True
    for chunk in rows:
        if first_chunk:
            fastparquet.write(outputfile, chunk, compression='snappy', append=False)
            first_chunk = False
        else:
            fastparquet.write(outputfile, chunk, compression='snappy', append=True)
