from smilescraper.logger import logging
from smilescraper.exception import CustomException
import requests
import sys
import pandas as pd
import streamlit as st

import time

logging.basicConfig(level=logging.INFO)


def get_smile_inchi(cas_number):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{cas_number}/property/CanonicalSMILES,InChi/JSON"
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        try:
            # Extract the canonical SMILES and InChI from the response
            data = response.json()['PropertyTable']['Properties'][0]
            # st.write(data)
            canonical_smiles = data['CanonicalSMILES']
            inchi = data['InChI'].replace('InChI=1S/', '')

            return {'Smile': canonical_smiles,
                    'InChi': inchi}
        except (KeyError, IndexError):
            return None
    else:
        # Handle the error
        print(f'Request failed with status code {response.status_code}')
    
    time.sleep(0.25)

def get_data(df):
    df["SMILES"] = ""
    df["InChI"] = ""
    progress_bar = st.progress(0)
    status_text = st.empty()
    for i, cas_number in df["CAS Number"].items():
        if pd.isna(cas_number):
            df.at[i, "SMILES"] = ""
            df.at[i , "InChi"] = ""
        else:
            result = get_smile_inchi(cas_number)
            if result is not None:
                smile = result['Smile']
                inchi = result['InChi']
                df.at[i, "SMILES"] = smile
                df.at[i, "InChi"] = inchi
            else:
                df.at[i, "SMILES"] = ""
                df.at[i, "InChi"] = ""
        progress = (i + 1) / len(df)
        progress_bar.progress(progress)
        status_text.text(f"{int(progress*100)}% Complete")
    
    return df
