import streamlit as st
import sqlite3
import hashlib
from groq import Groq

# 1. Database Initialization
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
    conn.commit()
    conn.close()

init_db()

# 2. Authentication Functions
def register_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_pw))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, hashed_pw))
    user = c.fetchone()
    conn.close()
    return user is not None

# 3. UI Config
st.set_page_config(page_title="MATRIX_CORE", layout="wide")
ADMIN_KEY = "123456" # Replace with your admin secret

# Custom CSS (English UI focus)
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #00FF41; font-family: 'Courier New', monospace; }
    .stTextArea textarea { background-color: #1a1a1a !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; }
    div.stButton > button { background-color: #00FF41 !important; color: #000000 !important; font-weight: bold; border-radius: 0px; }
    h1, h2, p { color: #00FF41 !important; }
    .chat-msg { background: #1a1a1a; padding: 10px; border-left: 3px solid #00FF41; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# 4. Auth Logic
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("> SYSTEM_LOGIN_REQUIRED")
    choice = st.radio("SELECT_MODE", ["LOGIN", "CREATE_ACCOUNT (ADMIN_AUTH_REQUIRED)"])
    
    user = st.text_input("USERNAME")
    pw = st.text_input("PASSWORD", type="password")
    
    if choice == "LOGIN":
        if st.button("> ACCESS_SYSTEM"):
            if login_user(user, pw):
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error("ACCESS_DENIED: INVALID_CREDENTIALS")
    else:
        admin_code = st.text_input("ADMIN_AUTH_KEY", type="password")
        if st.button("> REGISTER_USER"):
            if admin_code == ADMIN_KEY:
                if register_user(user, pw):
                    st.success("SUCCESS: USER_CREATED")
                else:
                    st.error("FAILURE: USER_ALREADY_EXISTS")
            else:
                st.error("ACCESS_DENIED: UNAUTHORIZED_OPERATION")

# 5. Secure Chat Logic (Post-Login)
else:
    st.title(f"> SYSTEM_CORE_ACTIVE: WELCOME {st.session_state.user}")
    if st.button("LOGOUT"):
        st.session_state.logged_in = False
        st.rerun()
    
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
