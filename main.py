import streamlit as st
import sqlite3
import hashlib
from groq import Groq

# 1. 頁面與資料庫基礎配置
st.set_page_config(page_title="MATRIX_CORE", layout="wide")

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
    conn.commit()
    conn.close()

init_db()

# 2. 帳號與加密管理
def register_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_pw))
        conn.commit()
        return True
    except: return False
    finally: conn.close()

def login_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, hashed_pw))
    user = c.fetchone()
    conn.close()
    return user is not None

# 3. 駭客介面風格 (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #00FF41; font-family: 'Courier New', monospace; }
    .chat-msg { background: #1a1a1a; padding: 10px; border-left: 3px solid #00FF41; margin: 10px 0; }
    </style>
""", unsafe_allow_html=True)

# 4. 系統狀態管理
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "messages" not in st.session_state: 
    st.session_state.messages = [{"role": "system", "content": "You are a cold, efficient Matrix AI assistant."}]

@st.dialog("SYSTEM_WARNING")
def confirm_clear():
    st.write("Are you sure you want to PURGE all neural history?")
    if st.button("EXECUTE_PURGE"):
        st.session_state.messages = [{"role": "system", "content": "You are a cold, efficient Matrix AI assistant."}]
        st.rerun()

# 5. 主程式邏輯
if not st.session_state.logged_in:
    st.title("> SYSTEM_ACCESS_REQUIRED")
    choice = st.radio("SELECT_MODE", ["LOGIN", "CREATE_ACCOUNT"])
    user = st.text_input("USERNAME")
    pw = st.text_input("PASSWORD", type="password")
    
    if choice == "LOGIN":
        if st.button("> LOGIN_EXECUTE"):
            if login_user(user, pw):
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()
            else: st.error("ACCESS_DENIED")
    else:
        admin_auth = st.text_input("ADMIN_AUTH_KEY", type="password")
        if st.button("> REGISTER_EXECUTE"):
            if admin_auth == "Idontknow!":
                if register_user(user, pw): st.success("USER_CREATED")
                else: st.error("USER_EXISTS")
            else: st.error("AUTH_FAILED")
else:
    st.title(f"> SYSTEM_CORE: {st.session_state.user}")
    if st.button("> PURGE_HISTORY"): confirm_clear()
    
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            role_label = "USER" if msg["role"] == "user" else "AI_CORE"
            st.markdown(f"<div class='chat-msg'><strong>{role_label}:</strong> {msg['content']}</div>", unsafe_allow_html=True)

    user_input = st.chat_input("TYPE_COMMAND...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        try:
            # 務必確保你的 Streamlit secrets 有設定 GROQ_API_KEY
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            response = client.chat.completions.create(
                messages=st.session_state.messages,
                model="llama-3.3-70b-versatile",
            )
            ai_reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            st.rerun()
        except Exception as e: st.error(f"RUNTIME_ERROR: {str(e)}")
