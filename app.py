import streamlit as st
from uploader import upload_csv
from veiwer import request_entity_viewer

# Set the title for the Streamlit app
st.title("API Interface App")

# CSV File Upload Section
upload_csv()

# Request Entity Viewer Section
request_entity_viewer()