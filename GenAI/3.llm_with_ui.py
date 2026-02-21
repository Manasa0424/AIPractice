import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# -----------------------
# Load API Key
# -----------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("GOOGLE_API_KEY not found in .env file")
    st.stop()

# -----------------------
# Page Config
# -----------------------
st.set_page_config(
    page_title="Gemini AI Chat",
    page_icon="🤖",
    layout="centered"
)

# -----------------------
# Custom Background & Styling
# -----------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #1e3c72, #2a5298);
    color: white;
}

.chat-container {
    background-color: rgba(255,255,255,0.05);
    padding: 10px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

st.title("🤖 Gemini AI Assistant")

# -----------------------
# Initialize LLM
# -----------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0.7,
    streaming=True
)

# -----------------------
# Session State for Memory
# -----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------
# Display Chat History
# -----------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------
# Chat Input
# -----------------------
prompt = st.chat_input("Ask me anything...")

if prompt:
    # Add user message to memory
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # Send full history to model
            response = llm.stream(
                [("system", "You are a helpful assistant.")] +
                [(m["role"], m["content"]) for m in st.session_state.messages]
            )

            for chunk in response:
                full_response += chunk.content
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"Error: {str(e)}")
            full_response = "Sorry, something went wrong."

    # Save assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
