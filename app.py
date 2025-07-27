import streamlit as st
from uploader import upload_csv
from veiwer import request_entity_viewer

def main():
    # Set the title for the Streamlit app
    st.title("API Interface App")

    # CSV File Upload Section
    upload_csv()

    # Request Entity Viewer Section
    request_entity_viewer()


if __name__ == "__main__":
    # Initialize streamlit session state variables
    if 'regenerate' not in st.session_state:
        st.session_state['regenerate'] = False  # Initialize regenerate state

    # Call the main function to run the app
    main()