import streamlit as st
from groq import Groq

# 頁面配置
st.set_page_config(page_title="MATRIX_CHAT", layout="wide")

# 駭客風格 CSS
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #00FF41; font-family: 'Courier New', monospace; }
    .stTextArea textarea { background-color: #1a1a1a !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; }
    div.stButton > button { background-color: #00FF41 !important; color: #000000 !important; font-weight: bold; border-radius: 0px; }
    .chat-msg { background: #1a1a1a; padding: 10px; border-left: 3px solid #00FF41; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# 初始化記憶
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "你是一個駭客風格的 AI，語氣簡潔、冷酷，像一個專業的系統核心。"}]

# 初始化客戶端
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("SYSTEM_FAILURE: API_KEY_MISSING")
    st.stop()

# 顯示聊天標題
st.title("> SYSTEM_TERMINAL_V1.0")
if st.button("CLEAR_MEMORY"):
    st.session_state.messages = [{"role": "system", "content": "系統已重置。"}]
    st.rerun()

# 顯示聊天記錄 (駭客式展示)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        role_label = "USER" if msg["role"] == "user" else "AI_CORE"
        st.markdown(f"<div class='chat-msg'><strong>{role_label}:</strong> {msg['content']}</div>", unsafe_allow_html=True)

# 輸入區
user_input = st.chat_input("輸入指令...")

if user_input:
    # 存入用戶輸入
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # AI 回覆
    with st.spinner("Processing..."):
        response = client.chat.completions.create(
            messages=st.session_state.messages,
            model="llama-3.3-70b-versatile",
        )
        ai_reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        st.rerun()
