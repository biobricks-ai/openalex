#! /usr/bin/env bash

mkdir -p brick csv
python3 stages/02_flatten-openalex-jsonl.py
