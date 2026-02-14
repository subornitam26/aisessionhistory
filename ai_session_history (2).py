import streamlit as st
import google.generativeai as genai

# Configure API Key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Use correct Gemini model name
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("AI Chatbot with Session History")

# Initialize message storage
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize Gemini chat session
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("What can I do for you?"):

    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Gemini response
    try:
        response = st.session_state.chat.send_message(prompt)
        reply = response.text

    except Exception as e:
        reply = "⚠️ Something went wrong while calling Gemini."
        st.error(e)

    # Save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)

# Sidebar clear button
if st.sidebar.button("Clear chat history"):
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[])
    st.rerun()
