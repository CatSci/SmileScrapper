import re
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_binary

from smilescraper.logger import logging
from smilescraper.exception import CustomException
import sys
import pandas as pd
import streamlit as st

WAIT_TIME = 5

def get_driver():
    """Start Selenium Chrome Driver

    Returns:
        driver: Chrome Driver
    """
    try:
        # logging.info('Logging Started')
        # logging.info('Chrome Driver Starting')
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        option.add_argument('--no-sandbox')
        # service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(options = option)
        return driver
    except Exception as e:
        # logging.error('Error Occured in loading Driver')
        raise CustomException(error_msg= e, error_detail= sys)

def find_cas_number_link(start_link, driver):
    """_summary_

    Args:
        start_link (_type_): _description_
        driver (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        elements = WebDriverWait(driver, WAIT_TIME).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'span.breakword')))
        cid = elements[1].text
        n_link = start_link.split('#')[0]
        link = f"{n_link}compound/{cid}"
        return link
    except Exception as e:
        raise CustomException(error_msg= e, error_detail= sys)

def get_smile(data, driver, cas_no):
    """To get the smile formula.
    Args:
        data {dict}: dictionary to store information extracted from website.
        driver {selenium web driver}: to load the website and extract data.
    Returns:
        data {dict}: returns a dictionary of information stored.
    """
    try:
        element = WebDriverWait(driver, WAIT_TIME).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#Canonical-SMILES')))
        # Get the text of the element
        text = element.text
        split_text = text.split()
        canonical_smiles = split_text[2]
        data[cas_no] = canonical_smiles
    except Exception as e:
        # st.write('[INFO] Smile not found')
        data[cas_no] = 'None'
        raise CustomException(error_msg= e, error_detail= sys)

    return data

def get_data(data, input_cas_list):
    """_summary_

    Args:
        data (_type_): _description_
        input_cas_list (_type_): _description_

    Returns:
        _type_: _description_
    """
    for i in input_cas_list:           
        start_link = "https://pubchem.ncbi.nlm.nih.gov/#query=" + str(i)

        driver = get_driver()
        driver.get(start_link)

        link = find_cas_number_link(start_link, driver)

        driver.get(link)
        data = get_smile(data, driver, cas_no= i)
    
    df = pd.DataFrame(list(data.items()), columns= ['Cas No', 'Smile'])
    return df

