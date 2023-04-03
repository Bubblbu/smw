#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This script is a minimal working example of a script that takes a list of DOIs
as an input and queries the Crossref REST API for respective metadata.

Author: Asura Enkhbayar (2023)
'''
# import
from datetime import datetime
from pathlib import Path

import habanero

def collect_data():
    pass

if __name__=="__main__":
    data_dir = Path("data")
    input_file = data_dir / "input/dois.csv"
    output_jsonl = data_dir / "output/metadata.jsonl"


