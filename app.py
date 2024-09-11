import json
import streamlit as st
import google.generativeai as genai
import time
import random

# Set page configuration with a modern title and favicon (optional)
st.set_page_config(
    page_title="Chat with Abhishek Sharma's Portfolio Chatbot",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="💬"
)

# Customize the main title and description
st.title("💬 Chat with Abhishek Sharma's Portfolio Chatbot")
st.caption("An AI-powered Portfolio Assistant built using Google Gemini Pro")

# Load the API key for Google Gemini from Streamlit secrets
st.session_state.app_key = st.secrets["API_KEY"]

# Initialize chat history if not present
if "history" not in st.session_state:
    st.session_state.history = []

# Configure the Generative AI model
genai.configure(api_key=st.session_state.app_key)
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=st.session_state.history)

# Read context from file for use in the chatbot conversation
with open("context.json", "r") as file:
    context = json.load(file)

# Sidebar with social links and a clear chat button
with st.sidebar:
    st.markdown("## Connect with Abhishek:")
    st.write("[LinkedIn](https://www.linkedin.com/in/abhishek-sharma-2a3764252/) | [GitHub](https://github.com/AbhiSharma096) | [Instagram](https://www.instagram.com/abhi.sharma_31/?hl=en)")
    if st.button("🔄 Clear Chat"):
        st.session_state.history = []  # Clear chat history without rerunning the script

# Chat input box at the bottom of the page
if prompt := st.chat_input(placeholder="Type your message here and press enter..."):
    prompt = prompt.replace('\n', ' \n')

    # User message
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(f"**You**: {prompt}")

    # Assistant response placeholder
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        message_placeholder.markdown("_Thinking..._")

        try:
            # Prepare input text and get AI response
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
                        message_placeholder.markdown(f"{full_response}_")
                        word_count = 0
                        random_int = random.randint(5, 10)
            message_placeholder.markdown(f"**Bot**: {full_response}")
        except genai.types.generation_types.BlockedPromptException as e:
            st.error("Sorry, this prompt is blocked. Try rephrasing.")
        except Exception as e:
            st.exception(e)

    # Store chat history
    st.session_state.history.append({"user": prompt, "bot": full_response})

# Custom styling for modern and minimalistic UI
st.markdown("""
    <style>
    /* General Page Styling */
    .stApp {
        background-color: #f7f7f7;
        font-family: 'Roboto', sans-serif;
    }

    /* Modern Chat Bubble Design */
    .st-chat {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 12px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        margin: 10px;
        max-width: 90%;
    }
    
    .user .st-chat {
        background-color: #d1f5e5;
        color: #333;
        text-align: left;
    }

    .assistant .st-chat {
        background-color: #e0f7fa;
        color: #333;
        text-align: left;
    }

    /* Input Box Styling */
    .st-chat-input {
        padding: 12px;
        border-radius: 15px;
        border: 1px solid #ccc;
        font-size: 16px;
    }

    /* Custom Button Style */
    .stButton>button {
        background-color: #1e90ff;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
        cursor: pointer;
    }
    
    /* Sidebar Design */
    .sidebar .stButton>button {
        background-color: #e91e63;
        font-weight: bold;
        margin: 5px 0;
    }

    .st-chat-message-container {
        display: flex;
        justify-content: flex-end;
    }

    .st-chat-message-container.user .st-chat {
        justify-content: flex-start;
    }
    
    /* Dark Mode */
    @media (prefers-color-scheme: dark) {
        .stApp {
            background-color: #1c1c1c;
        }
        .st-chat {
            background-color: #333333;
            color: #fff;
        }
        .stButton>button {
            background-color: #4caf50;
        }
        .sidebar {
            background-color: #1c1c1c;
        }
    }
    </style>
""", unsafe_allow_html=True)
