from schemas.chat_schema import ChatSchema
from schemas.chat_schema import Message
from db.mongo import get_collection
from collections import deque
chats = get_collection("chats")
short_term = deque(maxlen=5)
from datetime import datetime
from bson.objectid import ObjectId as objectid
import streamlit as st

"""
function to format chat history after get user_message and bot_message from chatSchema
"""
def format_chat(chat: ChatSchema) -> str:
    history_lines = []
    for msg in chat.message:
        history_lines.append(f"User: {msg.user_message}")
        history_lines.append(f"Bot: {msg.bot_message}")
    return "\n".join(history_lines)

"""
function to insert chat history and add to short_term memory
"""
def insert_chat(chat: ChatSchema):
    if "id" not in st.query_params or not st.query_params["id"]:
        new_chat =  chats.insert_one(chat.model_dump())
        st.query_params["id"] = str(new_chat.inserted_id)
    else:
        last_msg = chat.message[-1]
        update_chat(last_msg, st.query_params["id"])
    chat_str = format_chat(chat)
    if len(short_term) == short_term.maxlen:
        short_term.popleft()  
    print(chat_str)
    short_term.append(chat_str)

"""
function to update chat 
"""
def update_chat(new_message: Message,chat_id: str):
    chats.update_one(
        {"_id": objectid(chat_id)},
        {"$push": {"message": new_message.model_dump()}, 
         "$set": {"updated_at": datetime.now()}}
    )
"""
return short term memory
"""
def get_short_term_chats():
    return list(short_term)

def get_history_chat():
    return list(chats.find({"session_id": "cb9caadc-20b3-4c10-9969-669beb8a62cb"}))


def select_chat(id: str):
    obj_id = objectid(str(id).strip())
    chat = chats.find_one({"_id": obj_id})

    if not chat:
        st.warning(f"⚠️Can not find chat with ID: {obj_id}")
        return

    raw_messages = chat.get("message", [])
    messages = []

    for m in raw_messages:
        if isinstance(m, dict):
            user_msg = m.get("user_message")
            bot_msg = m.get("bot_message")
            print(user_msg,bot_msg)
            if user_msg:
                messages.append({
                    "role": "user",
                    "content": user_msg,
                    "avatar": "🧑‍💻"
                })
            if bot_msg:
                messages.append({
                    "role": "assistant",
                    "content": bot_msg,
                    "avatar": "🤖"
                })
        else:
            messages.append({
                "role": "user",
                "content": str(m),
                "avatar": "🧑‍💻"
            })
    st.query_params["id"] = str(obj_id)
    st.session_state.messages = messages