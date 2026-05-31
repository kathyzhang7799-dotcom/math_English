import streamlit as st
import sqlite3
import hashlib
from groq import Groq

# 設置頁面與資料庫
st.set_page_config(page_title="MATRIX_CORE", layout="wide")
ADMIN_KEY = "Idontknow!" # 已更新密碼

# (省略資料庫函數，保持與上一版一致...)

# [確認對話框邏輯]
@st.dialog("SYSTEM_WARNING")
def confirm_clear():
    st.markdown("<h3 style='color:red;'>CONFIRMATION_REQUIRED</h3>", unsafe_allow_html=True)
    st.write("Do you really want to permanently erase the neural history?")
    col1, col2 = st.columns(2)
    if col1.button("EXECUTE_PURGE"):
        st.session_state.messages = [{"role": "system", "content": "You are a cold, efficient Matrix AI assistant."}]
        st.rerun()
    if col2.button("ABORT"):
        st.rerun()

# [CSS 風格]
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #00FF41; font-family: 'Courier New', monospace; }
    .chat-msg { background: #1a1a1a; padding: 10px; border-left: 3px solid #00FF41; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# [登入與聊天邏輯]
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # (登入介面邏輯不變...)
    pass 
else:
    st.title(f"> SYSTEM_CORE_ACTIVE: {st.session_state.user}")
    
    # 加入清空按鈕
    if st.button("> PURGE_CHAT_HISTORY"):
        confirm_clear()
        
    # [聊天區塊]
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "You are a cold, efficient Matrix AI assistant."}]

    for msg in st.session_state.messages:
        if msg["role"] != "system":
            role_label = "USER" if msg["role"] == "user" else "AI_CORE"
            st.markdown(f"<div class='chat-msg'><strong>{role_label}:</strong> {msg['content']}</div>", unsafe_allow_html=True)

    user_input = st.chat_input("TYPE_COMMAND...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            response = client.chat.completions.create(
                messages=st.session_state.messages,
                model="llama-3.3-70b-versatile",
            )
            ai_reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            st.rerun()
        except Exception as e:
            st.error(f"RUNTIME_ERROR: {str(e)}")
