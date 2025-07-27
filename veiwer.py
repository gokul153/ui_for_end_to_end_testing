import streamlit as st
import requests
from state import State
from userfeedback import get_user_feedback

def request_entity_viewer():
    st.header("Request Entity Viewer")

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
                    for index, request in enumerate(data):
                        with st.expander(request.get('name', 'No Name'), expanded=False):  # Use the request name as title
                            st.write(f"**Method:** {request.get('method')}")
                            st.write(f"**URL:** {request.get('url')}")
                            st.write("**Headers:**")
                            st.json(request.get('headers'))
                            st.write("**Body:**")
                            st.json(request.get('body'))
                            
                            if st.button(f"Regenerate {request_name}", key=f"trigger_{index}"):
                                intialState = State(original_body=request.get('body')) 
                                get_user_feedback(intialState)
                                # st.session_state['selected_request'] = request
                                # st.session_state['regenerate'] = True
                             # Button to test the request
                            if st.button(f"Test the Request", key=f"test_{index}"):
                               with st.spinner("Sending request..."):
                                 try:
                                   url = request.get('url')  # Optionally use request.get('url') if different
                                   headers = request.get('headers', {})
                                   input_data = request.get('name')
 
                                   # Make the POST request
                                   response = requests.post(url, headers=headers, json={'input': input_data})
                    
                                   # Check for a successful response
                                   if response.status_code == 200:
                                      st.write("Response:")
                                      st.json(response.json())  # Display the response as JSON
                                   else:
                                      st.error(f"Request failed: {response.status_code} - {response.text}")

                                 except Exception as e:
                                   st.error(f"An error occurred: {e}")  # Display any error during the request
                                
                    # Navigation based on session state
                    if st.session_state.get('regenerate'):
                      st.write("### Regenerated Request")
                      st.write(f"**Request Name:** {st.session_state['selected_request']['name']}")
                      st.write("**Payload:**")
                      st.json(st.session_state['selected_request'])

                      # Optionally, provide a button to reset or go back
                      if st.button("Go Back"):
                        st.session_state['regenerate'] = False  # Reset the regenerate flag
           
                else:
                    st.warning("No requests found for the given name.")
            else:
                st.error(f"Request failed with status code: {response.status_code} - {response.text}")
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
             