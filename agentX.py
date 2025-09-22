import streamlit as st
import time
from utils.pdf_reader import extract_text_from_pdf
from agents.llm_gemini import llm
from prompts.chatbot import CHATBOT_PROMPT
from agents.report_agent import ReportAgent  
from dotenv import load_dotenv
load_dotenv()

# Set page configuration with a wide layout and a title.
st.set_page_config(layout="wide", page_title="AI Chatbot Agent", page_icon="🤖")

# --- Initialize Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_docs" not in st.session_state:
    st.session_state.uploaded_docs = []
if "uploaded_templates" not in st.session_state:
    st.session_state.uploaded_templates = []

# --- Left Panel for Document Upload and Display ---
with st.sidebar:
    st.title("📁 Documents")
    st.markdown("Upload your documents here.")
    st.markdown("---")

    uploaded_files = st.file_uploader(
        "Choose PDF documents",
        type=["pdf"],
        accept_multiple_files=True,
        key="doc_uploader"
    )

    if uploaded_files:
        current_file_names = [f.name for f in uploaded_files]
        session_file_names = [f['name'] for f in st.session_state.uploaded_docs]
        
        if sorted(current_file_names) != sorted(session_file_names):
            st.session_state.uploaded_docs = []
            for uploaded_file in uploaded_files:
                text_content = extract_text_from_pdf(uploaded_file)
                st.session_state.uploaded_docs.append({
                    "name": uploaded_file.name,
                    "content": text_content
                })
            
            st.toast(f"**{len(uploaded_files)}** document(s) uploaded successfully!", icon="✅")
            st.rerun()

    st.markdown("---")

    uploaded_templates = st.file_uploader(
        "Choose report templates",
        type=["pdf"],
        accept_multiple_files=True,
        key="template_uploader"
    )

    if uploaded_templates:
        current_template_names = [f.name for f in uploaded_templates]
        session_template_names = [f['name'] for f in st.session_state.uploaded_templates]

        if sorted(current_template_names) != sorted(session_template_names):
            st.session_state.uploaded_templates = []
            for uploaded_template in uploaded_templates:
                text_content = extract_text_from_pdf(uploaded_template)
                st.session_state.uploaded_templates.append({
                    "name": uploaded_template.name,
                    "content": text_content
                })
            
            st.toast(f"**{len(uploaded_templates)}** template(s) uploaded successfully!", icon="📝")
            st.rerun()

    st.subheader("Uploaded Files")
    if st.session_state.uploaded_docs:
        st.markdown("**Documents:**")
        for doc in st.session_state.uploaded_docs:
            st.markdown(f"- `{doc['name']}`")
    
    if st.session_state.uploaded_templates:
        st.markdown("**Templates:**")
        for template in st.session_state.uploaded_templates:
            st.markdown(f"- `{template['name']}`")
    
    if not st.session_state.uploaded_docs and not st.session_state.uploaded_templates:
        st.markdown("No documents uploaded yet.")

# --- Main Content Area: Chatbot Interface ---
st.title("🤖 Reporting Assistant")

# --- Conversation History Container ---
chat_placeholder = st.empty()

with chat_placeholder.container():
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message.get("avatar")):
            st.write(message["content"])

# --- Text Input at the bottom ---
if user_input := st.chat_input("What do you need help with?"):
    st.session_state.messages.append({"role": "user", "content": user_input, "avatar": "🧑‍💻"})

    with chat_placeholder.container():
        with st.chat_message("user", avatar="🧑‍💻"):
            st.write(user_input)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                doc_contents = [doc['content'] for doc in st.session_state.uploaded_docs]
                template_contents = [tpl['content'] for tpl in st.session_state.uploaded_templates]

                if doc_contents or template_contents:
                    print(f"Reporting agent will process this request {user_input} ...")
                    
                    # NEW: Create an instance of the ReportAgent
                    report_agent = ReportAgent()

                    # NEW: Call the agent's execute method
                    agent_response = report_agent.execute(doc_contents, template_contents, user_input)
                    response = agent_response.content
                else:
                    print("Chatbot agent working ...")
                    full_query = CHATBOT_PROMPT + "\n\nUser's request: " + user_input
                    response = llm._call(full_query)
                
                st.write(response)

            st.session_state.messages.append({"role": "assistant", "content": response, "avatar": "🤖"})
    st.rerun()