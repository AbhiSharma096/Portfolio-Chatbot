import json
import streamlit as st
import google.generativeai as genai
import time
import random
import os

# Set page configuration
st.set_page_config(
    page_title="Chat with Abhishek Sharma's Portfolio Chatbot",
)
st.title("Abhishek Sharma's Portfolio Chatbot")
st.caption("A Chatbot Powered by Google Gemini Pro")

# Initialize API key from secrets
st.session_state.app_key = st.secrets["API_KEY"]

# Initialize chat history if not already present
if "history" not in st.session_state:
    st.session_state.history = []  # History will store the list of messages

# Configure the Google Gemini API
genai.configure(api_key=st.session_state.app_key)

# Create the model instance
model = genai.GenerativeModel("gemini-pro")

# Format the chat history properly for use with Google Gemini API
def format_history(history):
    return [
        {"role": "user", "content": entry["user"]} if "user" in entry else {"role": "assistant", "content": entry["bot"]}
        for entry in history
    ]

# Format the history for starting the chat
formatted_history = format_history(st.session_state.history)
chat = model.start_chat(history=formatted_history)

# Read context from file
with open("context.json", "r") as file:
    context = json.load(file)

# Sidebar content for clearing chat and linking to social profiles
with st.sidebar:
    if st.button("Clear Chat Window", use_container_width=True, type="primary"):
        st.session_state.history = []  # Clear chat history
    st.subheader("Connect with Abhishek:")
    st.write("[LinkedIn](https://www.linkedin.com/in/abhishek-sharma-2a3764252/)",
              "[GitHub](https://github.com/AbhiSharma096)",
              "[Instagram](https://www.instagram.com/abhi.sharma_31/?hl=en)")

# Main chat interface
if "app_key" in st.session_state:
    if prompt := st.chat_input("Ask Abhishek's Portfolio Chatbot a question"):
        prompt = prompt.replace('\n', ' \n')
        
        # Display user's input in the chat
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Assistant response placeholder
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            try:
                # Combine context and user input for chatbot
                input_text = json.dumps(context) + f' � {prompt}'
                full_response = ""
                
                # Generate chatbot response with streaming
                for chunk in chat.send_message(input_text, stream=True):
                    word_count = 0
                    random_int = random.randint(5, 10)
                    
                    for word in chunk.text:
                        full_response += word
                        word_count += 1
                        if word_count == random_int:
                            time.sleep(0.05)  # Simulate typing effect
                            message_placeholder.markdown(full_response + "_")
                            word_count = 0
                            random_int = random.randint(5, 10)
                
                # Display the full response
                message_placeholder.markdown(full_response)
                
                # Save the chat to history
                st.session_state.history.append({"user": prompt, "bot": full_response})
            except genai.types.generation_types.BlockedPromptException as e:
                st.exception(e)
            except Exception as e:
                st.exception(e)
