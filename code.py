

import streamlit as st
import requests

# create the title for the page
st.title("🤝 Your Personal Assistant")

# add subheader
st.subheader("What can your personal assistant do?")

# create a list of what your assistant can do
st.markdown("""
            1. Answer questions on various topics.   
            2. Arrange Calendar events and meetings.  
            3. Read your emails and send replies, can even summarize them for you.
            4. Manage your tasks and to-do lists.
            5. Take quick notes for you.
            6. Track your expenses and budgeting.
            """)

# add chats subheader
st.subheader("💬 Chat with your assistant")

# create a session state for message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# show the messages in chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# create a chat input box
user_message = st.chat_input()

# if user sends a message
if user_message:
    with st.chat_message("user"):
        st.markdown(user_message)
        st.session_state.messages.append({"role": "user", "content": user_message})

    try:
        # send the user message directly to Ollama (Gemma model)
        response = requests.post(
            "https://ollama-production-4e61.up.railway.app/api/generate",
            json={
                "model": "gemma:latest",
                "prompt": user_message
            }
        )

        # parse Ollama response safely
        data = response.json()
        st.write("Raw response:", data)  # Debugging output

        # Ollama streams chunks, so join them if needed
        ai_response = ""
        if isinstance(data, dict) and "response" in data:
            ai_response = data["response"]
        elif isinstance(data, list):
            ai_response = "".join(chunk.get("response", "") for chunk in data)
        else:
            ai_response = str(data)

        # display the AI response in chat
        with st.chat_message("assistant"):
            st.markdown(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

    except Exception as e:
        st.error(f"Error: {e}")
