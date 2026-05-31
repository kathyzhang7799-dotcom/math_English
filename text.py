import streamlit as st
import time
from groq import Groq

# 1. 頁面配置
st.set_page_config(page_title="MATRIX_FIXER", layout="wide")

# 2. 駭客風格 CSS
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #00FF41; font-family: 'Courier New', monospace; }
    .stTextArea textarea { background-color: #1a1a1a !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; font-family: 'Courier New', monospace !important; }
    div.stButton > button { background-color: #00FF41 !important; color: #000000 !important; font-weight: bold; border-radius: 0px !important; border: none; }
    h1, h2, h3, p { color: #00FF41 !important; }
    .blink { animation: blinker 1s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
""", unsafe_allow_html=True)

# 3. 初始化 Groq Client
try:
    # 這裡對應你在 Streamlit Secrets 設定的名稱
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("SYSTEM_FAILURE: 無法讀取 API 金鑰，請檢查 Streamlit Secrets 是否設定正確。")
    st.stop()

# 4. 核心糾錯功能
def fix_text(wrong_text):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": f"請修正以下英文，只回傳修正後的文字，不要解釋：{wrong_text}"}],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content.strip()

# 5. UI 介面
st.title("> SYSTEM: MATRIX_ENGLISH_FIXER")
st.markdown("---")
st.write("Status: Connection Established... <span class='blink'>_</span>", unsafe_allow_html=True)

user_input = st.text_area("COMMAND_INPUT:", height=150, placeholder="Type your broken English here...")

if st.button("> EXECUTE_CORRECTION"):
    if not user_input.strip():
        st.warning("ERROR: INPUT_NULL_DETECTED")
    else:
        with st.spinner('Accessing Neural Link...'):
            try:
                result = fix_text(user_input)
                st.subheader("> OUTPUT_STREAM:")
                
                # 打字機效果
                placeholder = st.empty()
                full_text = ""
                for char in result:
                    full_text += char
                    placeholder.code(full_text + "▌")
                    time.sleep(0.02)
                placeholder.code(result) 
            except Exception as e:
                st.error(f"RUNTIME_ERROR: {str(e)}")

st.markdown("---")
st.caption("WARNING: Unauthorized access will be traced.")
