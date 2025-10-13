import streamlit as st
import time
from utils.pdf_reader import extract_text_from_pdf
from agents.llm_gemini import llm
from prompts.chatbot import CHATBOT_PROMPT
from agents.report_agent import ReportAgent  
from agents.research_agent import ResearchAgent  
from dotenv import load_dotenv
from memories.chat_memo import get_history_chat
from memories.chat_memo import select_chat as load_chat
query_id = st.query_params.get("id")
isResearch = st.session_state.get("is_research", False)
load_dotenv()
long_term_chat = get_history_chat()
# Set page configuration with a wide layout and a title.
st.set_page_config(layout="wide", page_title="AI Chatbot Agent", page_icon="🤖")

# --- Initialize Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_docs" not in st.session_state:
    st.session_state.uploaded_docs = []
    # text_content = extract_text_from_pdf("./data/ESG.pdf")
    # st.session_state.uploaded_docs.append({
    #     "name": "ESG.pdf",
    #     "content": text_content
    # })
if "uploaded_templates" not in st.session_state:
    st.session_state.uploaded_templates = []
    # text_content = extract_text_from_pdf("./data/ESG-template.pdf")
    # st.session_state.uploaded_docs.append({
    #     "name": "ESG-template.pdf",
    #     "content": text_content
    # })
def new_chat():
    st.query_params.clear()
    st.session_state.messages = []
def logout():
    st.session_state["is_logged_in"] = False
def cancel_trigger():
    st.session_state["show_login"] = False


# def login_page():
#     st.title("🔐 Login")
#     with st.form("login_form"):
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")
#         submitted = st.form_submit_button("Login")
       
#         print(username, password)
#         # if submitted:
#         #     if username == "admin" and password == "123":
#         #         st.session_state["is_logged_in"] = True
#         #         st.success("✅ Logged in successfully!")
#         #         st.rerun()
#         #     else:
#         #         st.error("❌ Invalid username or password")
#         st.form_submit_button("Cancel",on_click=cancel_trigger)
# if st.session_state.get("show_login"):
#     login_page()
# else:
#     st.title("Welcome 👋")
#     st.write("Please click 'Login' to access the system.")


# Select chat function, get id chat in sidebar and load the chat
def select_chat(id:str):
    # load chat in chat_memo
    load_chat(id)

# check if there is a chat id and when user load the page, the chat will not be disappeared
if not query_id:
    # if there is no chat id, create a new chat
    new_chat()
else:
    # if there is a chat id, load the chat
     
    select_chat(query_id)
# --- Left Panel for Document Upload and Display ---
with st.sidebar:
    col1, col2 = st.columns(2)
    # with col1:
    #     if st.button("Login"):
    #         st.session_state["show_login"] = True
    with col1:
        if st.button("Research", key="search"):
            st.session_state["is_research"] = not isResearch
            st.rerun()
            
    with col2:
        st.button("New Chat",on_click=new_chat, key="new_chat")
            
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
    
    st.title("🕰️History Chat")
    for chat in reversed(long_term_chat):
        if 'message' in chat and isinstance(chat['message'], list) and chat['message']:
            user_msg = chat['message'][0].get('user_message', '')
            trimmed = (user_msg[:50] + '...') if len(user_msg) > 50 else user_msg
            st.button(f"{trimmed}",on_click=select_chat, args=(chat['_id'],),key=chat['_id'])
            
# --- Main Content Area: Chatbot Interface ---
st.title("🤖 Reporting Assistant")
print(st.session_state.get("is_research"))
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
                if st.session_state.get("is_research"):
                    # print(f"Research agent will process this request {user_input} ...")
                    research_agent = ResearchAgent()
                    agent_response = research_agent.execute(user_input)
                    response = agent_response.content
                elif doc_contents or template_contents:
                    # print(f"Reporting agent will process this request {user_input} ...")
                    
                    # NEW: Create an instance of the ReportAgent
                    report_agent = ReportAgent()

                    # NEW: Call the agent's execute method
                    agent_response = report_agent.execute(doc_contents, template_contents, user_input)
                    response = agent_response.content
                else:
                    # print("Chatbot agent working ...")
                    full_query = CHATBOT_PROMPT + "\n\nUser's request: " + user_input
                    response = llm._call(full_query)
                
                st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response, "avatar": "🤖"})
    st.rerun()