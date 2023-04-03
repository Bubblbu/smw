#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This script is a minimal working example of a script that takes a list of DOIs
as an input and queries the Crossref REST API for respective metadata.

Input: A file with DOIs
Output: A spreadsheet with 

Author: Asura Enkhbayar (2023)
'''

# import
from datetime import datetime
from pathlib import Path

import habanero

def update_collection_progress(doi: str, ts: str, error: str):
    collection_progress.loc[doi]['timestamp'] = ts
    collection_progress.loc[doi]['error'] = error
    collection_progress.to_csv(collection_progress_f)

def collect_references(overwrite: False):
    if crossref_responses_f.exists():
        if overwrite:
            with open(crossref_responses_f, 'w') as f:
                for doi in tqdm(dois):
                    ts = datetime.datetime.now().isoformat()
                    error = None

                    try:
                        response = cr.works(doi, warn=True)

                        if response['status'] != 'ok':
                            error = response['status']
                        else:
                            f.write(json.dumps(response["message"]) + "\n")
                    except Exception as e:
                        error = e

                    # update collection progress
                    update_collection_progress(doi, ts, error)
        else:
            print("file already exists")

if __name__=="__main__":
    # Initialize project directory
    data_dir = Path("data")

    input_file = data_dir / "external/dois.csv"
    output_jsonl = data_dir / "raw/metadata.jsonl"
    collection_log = data_dir / "interim/log.csv"

    # Initialize Crossref API Client
    # More info here: https://habanero.readthedocs.io/en/latest/modules/crossref.html#habanero.Crossref
    mailto = "asura.enkhbayar@gmail.ca"
    ua_string = "Asura Enkhbayar"
    cr = Crossref(mailto=mailto,ua_string=ua_string)

