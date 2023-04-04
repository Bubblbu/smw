#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''


Author: Asura Enkhbayar (2023)
'''

# import from standard lib
from pathlib import Path

# import third-party stuff
import click
import pandas as pd
import tqdm as tqdm

@click.command()
@click.option("--overwrite", default=False, is_flag=True, help="Overwrite existing metadata.")
def main(overwrite: bool):
    # Initialize project directory
    data_dir = Path("data")

    # Input file and output file
    input_file = data_dir / "external/dois.csv"
    output_jsonl = data_dir / "raw/metadata.jsonl"
    
    # Log for collection metadata
    collection_log = data_dir / "interim/log.csv"

    # Load DOIs
    input_df = pd.read_csv(input_file)

    # Check if file already exists
    if output_jsonl.exists():
        if overwrite:
            pass
        else:
            if click.confirm("File already exists. Do you want to overwrite?"):
                pass
            else:
                sys.exit()

if __name__ == "__main__":
    main()