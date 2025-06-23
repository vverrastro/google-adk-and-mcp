import os
import streamlit as st
from dotenv import load_dotenv
import asyncio
from filesystem_agent import FilesystemAgent

# Load environment variables from .env file
load_dotenv()
absolute_path = os.getenv("ABSOLUTE_PATH")

# Create a single global event loop to avoid inconsistencies
global_loop = asyncio.new_event_loop()
asyncio.set_event_loop(global_loop)

st.set_page_config(page_title="Filesystem AI Agent", layout="centered")
st.title("\U0001F4AC Filesystem AI Agent")

# Initialize chat history and agent only once
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = FilesystemAgent(absolute_path)
    global_loop.run_until_complete(st.session_state.agent.start())

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle user input
if prompt := st.chat_input("Ask to Filesystem Agent..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Always use the persistent event loop
    response_text = global_loop.run_until_complete(
        st.session_state.agent.ask(prompt)
    )

    with st.chat_message("assistant"):
        st.markdown(response_text)

    st.session_state.messages.append({"role": "assistant", "content": response_text})

# Optional shutdown button
if st.button("\U0001F50C Shutdown Agent"):
    global_loop.run_until_complete(st.session_state.agent.shutdown())
    st.success("Agent connection closed.")