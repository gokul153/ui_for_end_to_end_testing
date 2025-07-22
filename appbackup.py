import streamlit as st
import requests
import os

# Title for the Streamlit app
st.title("CSV File Upload")

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

# Set the title of the application
st.title("Request Entity Viewer")

# Input box for request name
request_name = st.text_input("Enter the request name:", "billing_engine")
# Button to fetch requests
if st.button("Fetch Requests"):
    # Call the FastAPI endpoint
    try:
        response = requests.get(f'http://127.0.0.1:8000/list?request_name={request_name}', headers={'accept': 'application/json'})

        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()  # Parse the JSON response
            if data:
                # Display each request in a tile format
                for index,request in enumerate(data):
                    with st.expander(request.get('name', 'No Name'), expanded=False):  # Use the request name as title
                        st.write(f"**Method:** {request.get('method')}")
                        st.write(f"**URL:** {request.get('url')}")
                        st.write("**Headers:**")
                        st.json(request.get('headers'))
                        st.write("**Body:**")
                        st.json(request.get('body'))
                        if st.button(f"Regenerate {request_name}", key=f"trigger_{request_name}_{index}"):
                           # Add the action to be performed when the button is pressed
                           print("trying to triger and compare with the old request")
                           
                           st.success(f"{request_name} triggered!")  
            else:
                st.warning("No requests found for the given name.")
        else:
            st.error(f"Request failed with status code: {response.status_code} - {response.text}")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")