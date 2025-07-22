import streamlit as st
import requests

def upload_csv():
    st.header("CSV File Upload")

    # File uploader widget
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Display the file name
        st.write(f"You have uploaded: {uploaded_file.name}")
        
        # When the user clicks the upload button, call the FastAPI endpoint
        if st.button("Upload"):
            # Prepare the file for upload
            files = {'file': (uploaded_file.name, uploaded_file, 'text/csv')}
            
            try:
                # Call the FastAPI endpoint to upload the CSV
                response = requests.post('http://127.0.0.1:8000/upload-csv/', files=files)
                
                # Check if the request was successful
                if response.status_code == 200:
                    st.success("File successfully uploaded!")
                    st.json(response.json())  # Display the response from the FastAPI
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")