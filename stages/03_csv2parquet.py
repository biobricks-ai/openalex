import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os, sys

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

base_filename = os.path.basename(InFileName).split('.', 1)[0]
if base_filename in schemas:
    dtype = dtypes.get(base_filename)
    schema = schemas[base_filename]
else:
    dtype = None
    # Determine the schema from the first few rows of the CSV
    # Use a small number of rows to minimize memory usage
    schema_df = pd.read_csv(InFileName, sep=',', nrows=1000000, compression='gzip')
    schema = pa.Table.from_pandas(df=schema_df).schema

print(schema)

# Use a context manager to ensure the Parquet writer is properly closed after processing
with pq.ParquetWriter(OutFileName, schema, compression='snappy') as writer:
    if dtype:
        rows = pd.read_csv(InFileName, sep=',', dtype=dtype, compression='gzip', chunksize=chunk_size)
    else:
        rows = pd.read_csv(InFileName, sep=',', compression='gzip', chunksize=chunk_size)

    for chunk in rows:
        table = pa.Table.from_pandas(chunk, schema=schema)
        writer.write_table(table)
