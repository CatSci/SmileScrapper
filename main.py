import sys
import streamlit as st
from smilescraper.exception import CustomException
from smilescraper.logger import logging

st.header('Smile Scraper Project')

cas_no = st.text_input('CAS Number', '57-27-2')



# if __name__ == "__main__":
#     try:
#         a = 1/0
#     except Exception as e:
#         logging.info('Logging started')
#         logging.error('Error divde by 0')
#         raise CustomException(error_msg= e, error_detail= sys)