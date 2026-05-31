import streamlit as st
import sqlite3
import hashlib
from groq import Groq

# 1. 資料庫初始化 (只執行一次)
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
    conn.commit()
    conn.close()

init_db()

# 2. 帳號功能函數
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

# 3. 頁面邏輯
st.set_page_config(page_title="MATRIX_CORE", layout="wide")
ADMIN_KEY = "123456"  # 這裡改成你專屬的管理員密碼

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("> SYSTEM_LOGIN_REQUIRED")
    choice = st.radio("模式", ["登入", "創建帳號 (需管理員授權)"])
    
    user = st.text_input("帳號")
    pw = st.text_input("密碼", type="password")
    
    if choice == "登入":
        if st.button("確認登入"):
            if login_user(user, pw):
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error("帳號或密碼錯誤")
    else:
        admin_code = st.text_input("管理員密碼", type="password")
        if st.button("註冊"):
            if admin_code == ADMIN_KEY:
                if register_user(user, pw):
                    st.success("註冊成功，請登入！")
                else:
                    st.error("帳號已存在")
            else:
                st.error("管理員密碼錯誤，拒絕訪問")
else:
    st.write(f"歡迎回來, {st.session_state.user}")
    if st.button("登出"):
        st.session_state.logged_in = False
        st.rerun()
    
    # 這裡放你原本的聊天機器人邏輯
    st.title("> MATRIX_CHAT_ACTIVE")
    # ... (你的聊天代碼)
