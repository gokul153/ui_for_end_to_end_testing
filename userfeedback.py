import streamlit as st
import uuid
from state import State

def get_user_feedback(state: State):
    st.write("Original Body:", state["original_body"])
    user_inputs = {}

    for key, value in state["original_body"].items():
        st.write(f"Current Field: {key}, Current Value: {value}")

        # Streamlit input widget for user feedback
        user_feedback = st.text_input(f"Provide feedback for field: {key}", value="")

        # Process user feedback
        if user_feedback.strip() == "":
            user_inputs[key] = value  # User wants to copy the same value
        # elif user_feedback.lower() == "generate similar uuid":
        #     user_inputs[key] = str(uuid.uuid4())  # Generate a new UUID
        else:
            user_inputs[key] = user_feedback  # Use the provided user input

    return user_inputs
