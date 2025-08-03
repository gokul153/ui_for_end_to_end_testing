import streamlit as st
import requests
from state import State
from userfeedback import get_user_feedback
from sseclient import SSEClient
from state import State
import uuid



# ✅ Add this debug block early need to remove
st.sidebar.markdown("### 🐛 Debug Info")
st.sidebar.json(st.session_state)
def resume_chat(thread_id, feedback):
    st.info(f"Resuming interrupted thread `{thread_id}`...")
    url = "http://127.0.0.1:8000/resume"
    payload = {"thread_id": thread_id, "feedback": feedback}
    try:
        response = requests.post(url, json=payload, stream=True)
        client = SSEClient(response)

        placeholder = st.empty()
        for event in client.events():
            if event.event == "interrupt":
                placeholder.warning(f"⚠️ INTERRUPT: {event.data}")
            elif event.event == "update":
                placeholder.info(event.data)
            elif event.event == "end":
                placeholder.success("✅ Resumed and finished")
                break
    except Exception as e:
        st.error(f"Error resuming chat: {e}")


def stream_chat(request_name,thread_id):
    st.write(f"### Streaming for `{request_name}` started")
    url = f"http://127.0.0.1:8000/chat_stream/{request_name}?checkpoint_id={thread_id}"

    try:
        response = requests.get(url, stream=True)
        client = SSEClient(response)
        placeholder = st.empty()

        for event in client.events():
            if event.event == "interrupt":
                st.warning(f"⚠️ INTERRUPT: {event.data}")
                st.session_state['interrupted_thread'] = thread_id
                break
            elif event.event == "update":
                placeholder.info(event.data)
            elif event.event == "end":
                placeholder.success("✅ Execution finished")
                st.session_state['regenerate_requested'] = False

        # Show feedback form
        # with st.form(key=f"feedback_form_{request_name}"):
        #     feedback = st.text_area("💬 Please enter your feedback to continue:", "")
        #     print(st.session_state)
        #     st.markdown(f"**Thread ID:** `{thread_id}`")
        #     st.markdown(f"**Request Name:** `{request_name}`")
        #     submitted = st.form_submit_button("Submit Feedback and Resume")
        #     if submitted:
        #         st.markdown("🔄 Resuming the chat with your feedback...")
        #         st.session_state['feedback'] = feedback
        #         st.session_state['resume_requested'] = True
        #         st.session_state['interrupted_thread'] = thread_id
        #         st.session_state['interrupted_request_name'] = request_name
        #         st.markdown("🔁 Restarting the streaming based on the user feed back...")
        #         st.experimental_rerun()  
                # 🔁 RESTART STREAMING AFTER RESUME
               

    except Exception as e:
        st.error(f"Error streaming chat: {e}")
def resume_chat(thread_id, feedback):
    print(f"📞 Resuming chat: thread={thread_id}, feedback={feedback}")
    # Check if the thread_id and feedback are provided
    if not thread_id or not feedback:
        st.error("Thread ID and feedback are required to resume the chat.")
        return "Please provide both thread ID and feedback to resume the chat."
    st.info(f"Resuming interrupted thread `{thread_id}`...")
    url = "http://127.0.0.1:8000/resume"
    payload = {"thread_id": thread_id, "feedback": feedback}
    try:
        response = requests.post(url, json=payload, stream=True)
        client = SSEClient(response)
        placeholder = st.empty()
        for event in client.events():
            st.write(f"🔄 Processing event: {event.event} - {event.data}")
            if event.event == "interrupt":
                placeholder.warning(f"⚠️ INTERRUPT: {event.data}")
                    # 🔁 Save context and trigger next resume cycle
                st.session_state["resume_requested"] = True
                st.session_state["interrupted_thread"] = thread_id
                st.session_state["interrupted_request_name"] = st.session_state.get("request_name")
                st.session_state["feedback_needed"] = True  # Custom flag
                return  # Exit early and wait for next form submission
            elif event.event == "update":
                placeholder.info(event.data)
            elif event.event == "end":
                placeholder.success("✅ Resumed and finished")
                break
    except Exception as e:
        st.error(f"Error resuming chat: {e}")
# --- Call stream_chat if triggered ---
if st.session_state.get("regenerate_requested"):
    request_name = st.session_state.pop("request_name", None)
    thread_id = st.session_state.get("thread_id")
    if request_name and thread_id:
        # Only trigger once
        st.session_state["regenerate_requested"] = False
         #stream_chat(st.session_state['request_name'], st.session_state['thread_id'])

if st.session_state.get("resume_requested"):
    print("🔄 Resuming chat based on user feedback...")
    st.session_state["resume_requested"] = False  # Reset the flag
    thread_id = st.session_state.get("interrupted_thread")
    request_name = st.session_state.get("interrupted_request_name")
    feedback = st.session_state.get("feedback")
    if thread_id and feedback:
        resume_chat(thread_id, feedback)        




def request_entity_viewer():
    st.header("Request Entity Viewer")

    # Input box for request name
    request_name = st.text_input("Enter the request name:", "enter request name here")

    # Button to fetch requests
    if st.button("Fetch Requests"):
        st.sidebar.markdown("### 🐛 Debug Info")
        st.sidebar.json(st.session_state)
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
           
                else:
                    st.warning("No requests found for the given name.")
            else:
                st.error(f"Request failed with status code: {response.status_code} - {response.text}")
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    if st.button("Generate Request Using AI"):
        
        thread_id = str(uuid.uuid4())
        st.markdown("🔄 Calling `stream_chat()` now...")
        st.session_state["regenerate_requested"] = True
        st.write("📦 Session State:", st.session_state)
        st.session_state["request_name"] = request_name
        st.session_state["thread_id"] = thread_id
        stream_chat(request_name, thread_id)
    with st.form(key=f"feedback_form_{request_name}"):
            st.sidebar.markdown("### 🐛 Debug Info")
            st.sidebar.json(st.session_state)
            feedback = st.text_area("💬 Please enter your feedback to continue:", "generate similar to  email in bteam@gmail.com")
            submitted = st.form_submit_button("Submit Feedback and Resume")
            if submitted:
                st.markdown("🔄 Resuming the chat with your feedback...")
                st.session_state['feedback'] = feedback
                st.session_state['resume_requested'] = True
                st.session_state['interrupted_thread'] = st.session_state.get("thread_id")
                st.session_state['interrupted_request_name'] = st.session_state.get("request_name")
                resume_chat(st.session_state['interrupted_thread'], feedback)
                # 🔁 RESTART STREAMING AFTER RESUME
                # st.markdown("🔁 Restarting the streaming based on the user feed back...")
                # st.markdown("🔄 Calling `stream_chat()` now...")
                # st.session_state["regenerate_requested"] = True
                # st.write("📦 Session State:", st.session_state)
                # stream_chat(st.session_state['interrupted_request_name'], st.session_state['interrupted_thread'])
    