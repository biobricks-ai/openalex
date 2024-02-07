#!/usr/bin/env bash

# See schema diagram at https://2520693015-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FpHVuV3Ib5KXeBKft4Kcl%2Fuploads%2Fgit-blob-bf7f058bf88f3bcc1bd040e2c93607d8f61033b7%2Fopenalex-schema.png?alt=media

set -euo pipefail

rm -rf sqlite
mkdir -p sqlite

sqlite3 sqlite/sqlite.db < stages/04_create_table.sql

duckdb -c 'INSTALL sqlite'
duckdb -echo -unsigned sqlite/sqlite.db < stages/04_duckdb.sql

sqlite3 sqlite/sqlite.db < stages/04_create_index.sql
