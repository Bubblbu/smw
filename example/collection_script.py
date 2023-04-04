#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This script is a minimal working example of a script that takes a list of DOIs
as an input and queries the Crossref REST API for metadata.

Author: Asura Enkhbayar (2023)
'''

# import from standard lib
import csv
from datetime import datetime
from pathlib import Path
import sys

# import third-party stuff
import click
import habanero
import pandas as pd
import tqdm as tqdm

@click.command()
@click.option("--overwrite", default=False, is_flag=True, help="Overwrite existing metadata.")
def main(overwrite: bool):
    # Initialize project directory
    data_dir = Path("data")

    # Input file and output file
    input_file = data_dir / "external/articles.csv"
    output_jsonl = data_dir / "raw/metadata.jsonl"
    
    # Log for collection metadata
    collection_log = data_dir / "interim/log.csv"
    
    # Initialize Crossref API Client
    # More info here: 
    # https://habanero.readthedocs.io/en/latest/modules/crossref.html#habanero.Crossref
    mailto = "asura.enkhbayar@gmail.ca"
    ua_string = "Asura Enkhbayar"
    cr = Crossref(mailto=mailto,ua_string=ua_string)

    # Load DOIs
    input_df = pd.read_csv(input_file, index_col="id")
    dois = input_df["DOI"]

    # Check if file already exists
    if output_jsonl.exists():
        if overwrite:
            pass
        else:
            if click.confirm("File already exists. Do you want to overwrite?"):
                pass
            else:
                sys.exit()

    # Init collection log
    log_f = open(collection_log, 'w')
    log_writer = csv.writer(log_f, delimiter=",")
    log_writer.writerow(["DOI", "timestamp", "status"])

    # Open the output file as a stream to write to
    with open(output_jsonl, 'w') as f:
        # Iterate over all DOIs
        # tqdm produces a nice progress bar
        for doi in tqdm(dois):
            # Init collection metadata
            ts = datetime.datetime.now().isoformat()
            error = None

            # Query the /works endpoint with current DOI
            # More info here:
            # https://api.crossref.org/swagger-ui/index.html#/Works/get_works__doi_
            try:
                response = cr.works(doi, warn=True)

                if response['status'] != 'ok':
                    error = response['status']
                else:
                    item = response["message"]
                    f.write(json.dumps(item) + "\n")
            except Exception as e:
                error = e

            # update collection progress
            log_writer.writerow([doi, ts, error])
    
    # close the file stream
    log_f.close()

if __name__ == "__main__":
    main()