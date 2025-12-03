import streamlit as st

# Title for the app
st.title("Chatbot Application")

# Description
st.write("Welcome to the Chatbot! Ask your questions below.")

# Input for user question
user_input = st.text_input("Ask the chatbot:")

# Simulate a response (replace this with your actual chatbot logic)
if user_input:
    # Replace this with your actual chatbot logic
    response = f"Bot: This is a response to '{user_input}'"
    st.write(response)