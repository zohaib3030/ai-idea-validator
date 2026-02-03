import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv() 
# Page config
st.set_page_config(page_title="Simple Groq Chatbot", page_icon="🤖")

st.title("🤖 Simple Chatbot")
st.write("Ask anything, I’ll try to help!")

# Get API key (from environment variable)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# GROQ_API_KEY = st.secrets["GROQ_API_KEY"]


if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found. Please set it in environment variables.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your question here...")

if user_input:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get response from Groq
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=st.session_state.messages
    )

    bot_reply = response.choices[0].message.content

    # Show bot message
    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )
    with st.chat_message("assistant"):
        st.markdown(bot_reply)