import json
import streamlit as st
import google.generativeai as genai
import time
import random
from dotenv import load_dotenv
import os




st.set_page_config(
    page_title="Chat with Shivansh's Portfolio chatbot",
    
)

st.title("Shivansh's Portfolio Chatbot")
st.caption("A Chatbot Powered by Google Gemini Pro")

load_dotenv()

st.session_state.app_key = os.getenv("API_KEY") 

if "history" not in st.session_state:
    st.session_state.history = []

genai.configure(api_key=st.session_state.app_key)

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=st.session_state.history)

# Read context from file
with open("context.json", "r") as file:
    context = json.load(file)

with st.sidebar:
    if st.button("Clear Chat Window", use_container_width=True, type="primary"):
        st.session_state.history = []  # Clear the chat history without rerunning the script
    
    st.subheader("Connect with Shivansh:")
    st.write("[LinkedIn | ](https://linkedin.com/in/shivanshtri010)", "[ GitHub](https://github.com/shivanshtri010)", "[ | Instagram](https://www.instagram.com/shivanshtripathi010/)")

if "app_key" in st.session_state:
    if prompt := st.chat_input(""):
        prompt = prompt.replace('\n', ' \n')
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            try:
                # Combine context and user input properly
                input_text = json.dumps(context) + f' � {prompt}'
                full_response = ""
                for chunk in chat.send_message(input_text, stream=True):
                    word_count = 0
                    random_int = random.randint(5, 10)
                    for word in chunk.text:
                        full_response += word
                        word_count += 1
                        if word_count == random_int:
                            time.sleep(0.05)
                            message_placeholder.markdown(full_response + "_")
                            word_count = 0
                            random_int = random.randint(5, 10)
                message_placeholder.markdown(full_response)
            except genai.types.generation_types.BlockedPromptException as e:
                st.exception(e)
            except Exception as e:
                st.exception(e)
            st.session_state.history.extend(chat.history)  # Preserve chat history
