import streamlit as st
import time
from utils.pdf_reader import extract_text_from_pdf
from agents.llm_gemini import llm
from prompts.chatbot import CHATBOT_PROMPT




from dotenv import load_dotenv
load_dotenv()

# Set page configuration with a wide layout and a title.
st.set_page_config(layout="wide", page_title="AI Chatbot Agent", page_icon="🤖")

# --- Initialize Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = {
        "resume": {"name": None, "content": None},
        "job_description": {"name": None, "content": None}
    }

# --- Left Panel for Document Upload and Display ---
with st.sidebar:
    st.title("📁 Documents")
    st.markdown("Upload your Resume and Job Description here.")
    st.markdown("---")

    uploaded_doc = st.file_uploader(
        "Choose your resume", 
        type=["pdf"],
        key="cv_uploader"
    )

    if uploaded_doc:
        if st.session_state.uploaded_files["resume"]["name"] != uploaded_doc.name:
            st.session_state.uploaded_files["resume"]["name"] = uploaded_doc.name
            text_content = extract_text_from_pdf(uploaded_doc)
            st.session_state.uploaded_files["resume"]["content"] = text_content
            st.toast(f"Resume **{uploaded_doc.name}** uploaded successfully!", icon="✅")
            st.rerun()

    st.markdown("---")

    
            
    st.subheader("Uploaded Files")
    if st.session_state.uploaded_files["resume"]["name"]:
        st.markdown(f"- **Resume:** `{st.session_state.uploaded_files['resume']['name']}`")
    if st.session_state.uploaded_files["job_description"]["name"]:
        st.markdown(f"- **Job Description:** `{st.session_state.uploaded_files['job_description']['name']}`")
    
    if not st.session_state.uploaded_files["resume"]["name"] and not st.session_state.uploaded_files["job_description"]["name"]:
        st.markdown("No documents uploaded yet.")

# --- Main Content Area: Chatbot Interface ---
st.title("🤖 Plywood Source LLC AI Chatbot")

# --- Conversation History Container ---
chat_placeholder = st.empty()

with chat_placeholder.container():
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message.get("avatar")):
            st.write(message["content"])
# Define agents and team:


# --- Text Input at the bottom ---
if user_input := st.chat_input("What do you need help with?"):
    st.session_state.messages.append({"role": "user", "content": user_input, "avatar": "🧑‍💻"})

    with chat_placeholder.container():
        with st.chat_message("user", avatar="🧑‍💻"):
            st.write(user_input)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                doc_conent = st.session_state.uploaded_files["resume"]["content"]
                                
                if doc_conent:
                    print("Extract agent working ...")
                    # Update the exatract agent here

                else:
                    print("Chatbot agent working ...")
                    full_query = CHATBOT_PROMPT + "\n\nUser's request: " + user_input
                    response = llm._call(full_query)
                
                st.write(response)

            st.session_state.messages.append({"role": "assistant", "content": response, "avatar": "🤖"})
    st.rerun()