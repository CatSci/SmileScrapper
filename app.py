import sys
import os
import time
import streamlit as st
import pandas as pd
from smilescraper.exception import CustomException
from smilescraper.logger import logging

from smilescraper.pubchem import get_data
from smilescraper.utils import convert_df
# st.set_page_config(page_title="My Streamlit App", page_icon=":smiley:", layout="wide", page_bg_color="#11b2b")
# background-color: ed9439;
# color:#0f1b2a;
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #ed9439;
    color:#0f1b2a;
    border:None;
}
div.stButton > button:first-child:focus {
    background-color: #ed9439;
    color:#0f1b2a;
    border:None;
}

</style>""", unsafe_allow_html=True)
st.title("CAS Number to SMILES Converter")
st.info('Please make sure you cas value column name is **CAS Number**')

uploaded_file = st.file_uploader("Choose a file")

if st.button('Search'):
    # add try except instead if uploaded_files
    try:
        filename = uploaded_file.name
        if ".xlsx" in filename:
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
        
        df = get_data(df= df) 
        smile_output = convert_df(df)   
        # Display the DataFrame in the Streamlit app
        st.write(df)
        st.success('Successful')
        st.download_button(
            label = 'Download data as CSV',
            data = smile_output,
            file_name = 'smiles.csv',
            mime = 'text/csv',
        )
    except Exception as e:
        st.error('File not uplaoded or correct file not uplaoded')


########################
######## Input #########
########################
# cas_no = st.text_input('CAS Number', '57-27-2,102-54-5, 108-88-3')


# st.text('')
# colT1,colT2 = st.columns([3,4])
# with colT2:
#     st.write('Or')

# uploaded_file = st.file_uploader("Choose a file")

########################
#### Search Button #####
########################
# if st.button('Search'):
#     if cas_no == '' and uploaded_file is None:
#         st.error('Enter some values or uplaod a file')
#     else:
#         with st.spinner('Processing...'):
#             data = {}

#             if uploaded_file is None and cas_no != '':
#                 st.info('You have entered Cas values')
#                 input_cas_list = cas_no.split(',')
#             elif uploaded_file is not None and cas_no == '':
#                 st.info('You have Uploaded a file')
#                 filename = uploaded_file.name
#                 if ".xlsx" in filename:
#                     input_df = pd.read_excel(uploaded_file)
#                 else:
#                     input_df = pd.read_csv(uploaded_file)
                
#                 input_cas_list = input_df['CAS Number'].values
#             else:
#                 st.error('Please enter values or upload file not both')

#             try:
#                 df = get_data(data = data, input_cas_list= input_cas_list)
#                 smile_output = convert_df(df)
#                 st.success('Successful')
#                 st.table(df)
#                 st.download_button(
#                     label = 'Download data as CSV',
#                     data = smile_output,
#                     file_name = 'smiles.csv',
#                     mime = 'text/csv',
#                 )
#             except Exception as e:
#                 raise CustomException(error_msg= e, error_detail= sys)

            



