import streamlit as st
from fractions import Fraction
import math
import os
import json
import time  # ✅ 修正：補上缺失的 time 模組，避免登入時崩潰

DB_FILE = "users_db.json"

# --- 1. 網頁全域配置與黑客帝國數位雨特效注入 ---
st.set_page_config(page_title="THE MATRIX: CORE V8", page_icon="⚡", layout="wide")

st.markdown("""
    <canvas id="matrix-canvas" style="position:fixed; top:0; left:0; width:100vw; height:100vh; z-index:-1;"></canvas>
    <script>
    const canvas = document.getElementById('matrix-canvas');
    const ctx = canvas.getContext('2d');
    function resizeCanvas() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    const katakana = "ABCDEFGHIJKLMNOPQRSTUVWXYZ012345678901";
    const fontSize = 16;
    let columns = canvas.width / fontSize;
    const rainDrops = Array(Math.floor(columns)).fill(1);
    function draw() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#00FF00';
        ctx.font = fontSize + 'px monospace';
        for (let i = 0; i < rainDrops.length; i++) {
            const text = katakana.charAt(Math.floor(Math.random() * katakana.length));
            ctx.fillText(text, i * fontSize, rainDrops[i] * fontSize);
            if (rainDrops[i] * fontSize > canvas.height && Math.random() > 0.975) rainDrops[i] = 0;
            rainDrops[i]++;
        }
    }
    setInterval(draw, 30);
    </script>
    <style>
    .stApp { background: transparent; }
    .main .block-container { background-color: rgba(0, 0, 0, 0.85); border: 1px solid #00FF00; border-radius: 15px; padding: 2.5rem; }
    h1, h2, h3, label, p, span, div { color: #00FF00 !important; font-family: 'Courier New', monospace; }
    div.stButton > button { background: #000; color: #0F0; border: 1px solid #0F0; width: 100%; font-weight: bold; }
    div.stButton > button:hover { background: #00FF00; color: #000; border: 1px solid #00FF00; }
    .stTextInput>div>div>input { background-color: rgba(0,0,0,0.7) !important; color: #00FF00 !important; border: 1px solid #00FF00 !important; }
    .stSelectbox>div>div>div { background-color: rgba(0,0,0,0.7) !important; color: #00FF00 !important; border: 1px solid #00FF00 !important; }
    .stRadio>div { color: #00FF00 !important; }
    div[data-testid="stCodeBlock"] { border: 1px solid #00FF00; background-color: rgba(0,0,0,0.9); }
    </style>
""", unsafe_allow_html=True)

# --- 2. 持久化账户读写函数（明文存储） ---
def load_users() -> dict:
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_users(users_data: dict):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users_data, f, ensure_ascii=False, indent=4)

# 二次方程分數轉換輔助函數
def to_fraction_str(val):
    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    try:
        frac = Fraction(val).limit_denominator(1000)
        if abs(float(frac) - float(val)) > 1e-9:
            return f"{val:.4f}"
        return str(frac)
    except:
        return f"{val:.4f}"

# --- 3. 初始化 Streamlit 会话状态机 ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# --- 4. 核心鉴权层（GATEWAY AUTHENTICATION） ---
if not st.session_state.authenticated:
    st.title("⚡ THE MATRIX: GATEWAY SECURITY")
    st.write("ACCESS DENIED. IDENTITY VERIFICATION REQUIRED TO BOOT CORE V8.")
    
    users = load_users()
    
    auth_mode = st.radio("SELECT GATEWAY COMMAND:", ["1. LOGIN (账户登录)", "2. REGISTER (新冒险者注册)"])
    
    st.markdown("---")
    
    if auth_mode == "1. LOGIN (账户登录)":
        login_user = st.text_input("ENTER USERNAME (账号):", key="login_u")
        login_pwd = st.text_input("ENTER PASSWORD (密码):", type="password", key="login_p") # ✅ 優化：加上 type="password" 隱藏密碼
        
        if st.button("EXECUTE LOGIN PROTOCOL"):
            if login_user in users and users[login_user] == login_pwd:
                st.session_state.authenticated = True
                st.session_state.current_user = login_user
                st.success(f"🔓 ACCESS GRANTED. WELCOME BACK, OPERATOR: {login_user}")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ INVALID CREDENTIALS. ACCESS DENIED.")
                
    elif auth_mode == "2. REGISTER (新冒险者注册)":
        st.markdown("### 🛡️ ARCHITECT AUTHORIZATION REQUIRED")
        st.write("欲創建新矩陣帳號，請聯繫管理員 Harry 輸入驗證密鑰。")
        
        # 第一關：管理員實體驗證（只有你懂得密碼，加上 type="password" 隱藏）
        admin_key = st.text_input("ENTER ARCHITECT KEY (管理員授權密碼):", type="password", key="admin_k")
        
        st.markdown("---")
        st.write(">>> 授權通過後方可填寫下方新帳號資訊：")
        
        # 第二關：原本的註冊輸入框
        reg_user = st.text_input("CREATE NEW USERNAME (输入新账号):", key="reg_u").strip()
        reg_pwd = st.text_input("CREATE NEW PASSWORD (输入新密码):", type="password", key="reg_p")
        
        if st.button("COMMIT REGISTRATION TO DATABASE"):
            # 💡 核心防禦：先檢查管理員密碼對不對（這裡假設你設定的終極密碼是 "MatrixAdmin99"）
            if admin_key != "MatrixAdmin99":
                st.error("❌ 授權失敗：管理員密鑰錯誤！拒絕創建帳號。")
            elif not reg_user:
                st.error("❌ USERNAME CANNOT BE EMPTY.")
            elif reg_user in users:
                st.error("❌ ARCHITECT NODE ALREADY EXISTS. CHOOSE ANOTHER NAME.")
            else:
                # 兩關都過了，才允許寫入 JSON 檔案
                users[reg_user] = reg_pwd
                save_users(users)
                st.success(f"🎉 ARCHITECT ACCOUNT [{reg_user}] SUCCESSFULLY LOGGED TO MATRIX DATABASE.")
                st.info(">>> Switching to Login tab to enter.")

else:
    # --- 5. 鉴权通过：释放主程序系统 ---
    st.sidebar.markdown(f"**🟢 OPERATOR:** `{st.session_state.current_user}`")
    if st.sidebar.button("🚪 LOGOUT / LOCKDOWN"):
        st.session_state.authenticated = False
        st.session_state.current_user = ""
        st.rerun()

    st.title("⚡ THE MATRIX: LOGIC SOURCE CORE V8")
    st.write(f"Welcome back to the Ultimate Math Engine Web Interface, {st.session_state.current_user}.")

    # --- 侧边栏系统主选单对接 ---
    menu = st.sidebar.selectbox("請選擇模組功能 (SYSTEM MENU):", [
        "1. Addition Mode",
        "2. Subtraction Mode",
        "3. Multiplication Mode",
        "4. Division Mode",
        "5. Advanced Formulas Selection",
        "6. Multi-functional Data Charts",
        "7. Perimeter Formulas Module",
        "8. Hexadecimal ASCII Cipher Encryption",
        "9. Hexadecimal ASCII Cipher Decryption"
    ])

    # --- 模組核心逻辑完全實現 ---
    if menu == "1. Addition Mode":
        st.subheader("➕ [Addition Mode]")
        raw_one = st.text_input("Enter 1st addend:")
        raw_two = st.text_input("Enter 2nd addend:")
        if st.button("EXECUTE ADDITION"):
            if raw_one and raw_two:
                try:
                    one = Fraction(raw_one)
                    two = Fraction(raw_two)
                    st.success(f"Result: {one} + {two} = {one + two}")
                except ValueError:
                    st.error("❌ Error: Please enter valid numbers or fractions!")

    elif menu == "2. Subtraction Mode":
        st.subheader("➖ [Subtraction Mode]")
        raw_one = st.text_input("Enter minuend:")
        raw_two = st.text_input("Enter subtrahend:")
        if st.button("EXECUTE SUBTRACTION"):
            if raw_one and raw_two:
                try:
                    one = Fraction(raw_one)
                    two = Fraction(raw_two)
                    st.success(f"Result: {one} - {two} = {one - two}")
                except ValueError:
                    st.error("❌ Error: Please enter valid numbers or fractions!")

    elif menu == "3. Multiplication Mode":
        st.subheader("✖️ [Multiplication Mode]")
        raw_one = st.text_input("Enter 1st factor:")
        raw_two = st.text_input("Enter 2nd factor:")
        if st.button("EXECUTE MULTIPLICATION"):
            if raw_one and raw_two:
                try:
                    one = Fraction(raw_one)
                    two = Fraction(raw_two)
                    st.success(f"Result: {one} × {two} = {one * two}")
                except ValueError:
                    st.error("❌ Error: Please enter valid numbers or fractions!")

    elif menu == "4. Division Mode":
        st.subheader("➗ [Division Mode]")
        raw_one = st.text_input("Enter dividend:")
        raw_two = st.text_input("Enter divisor:")
        if st.button("EXECUTE DIVISION"):
            if raw_one and raw_two:
                try:
                    if raw_two == "0":
                        st.warning("⚠️ Error: Divisor cannot be zero!")
                    else:
                        one = Fraction(raw_one)
                        two = Fraction(raw_two)
                        st.success(f"Result: {one} ÷ {two} = {one / two}")
                except ValueError:
                    st.error("❌ Error: Please enter valid numbers or fractions!")

    elif menu == "5. Advanced Formulas Selection":
        st.subheader("🧠 [Advanced Formulas Menu]")
        adv_choice = st.selectbox("Select an advanced formula:", [
            "1. Quadratic Equation Root Solver",
            "2. Perfect Square Expansion",
            "3. Pythagorean Theorem Unknown Side",
            "4. Area Formulas Core",
            "5. Volume Formulas Core"
        ])
        
        if adv_choice == "1. Quadratic Equation Root Solver":
            st.markdown("#### Quadratic Equation Solver (ax² + bx + c = 0)")
            raw_a = st.text_input("Enter a:")
            raw_b = st.text_input("Enter b:")
            raw_c = st.text_input("Enter c:")
            if st.button("SOLVE QUADRATIC"):
                try:
                    input_one = float(raw_a)
                    input_two = float(raw_b)
                    input_three = float(raw_c)
                    if input_one == 0:
                        st.error("❌ Error: 'a' cannot be 0 in a quadratic equation.")
                    else:
                        discriminant = input_two ** 2 - 4 * input_one * input_three
                        if discriminant < 0:
                            st.error("❌ This equation has no real roots.")
                        else:
                            anser_one = (-input_two + (discriminant ** 0.5)) / (2 * input_one)
                            anser_two = (-input_two - (discriminant ** 0.5)) / (2 * input_one)
                            st.success(f"🎉 Roots: {to_fraction_str(anser_one)} OR {to_fraction_str(anser_two)}")
                except ValueError:
                    st.error("❌ Error: Please enter valid numbers. Try again!")

        elif adv_choice == "2. Perfect Square Expansion":
            st.markdown("#### Perfect Square Expansion (a²+2ab+b²)")
            raw_a = st.text_input("Enter expression 'a':")
            raw_b = st.text_input("Enter expression 'b':")
            if st.button("EXPAND EXPRESSION"):
                try:
                    user_input_for_wan_quan_ping_fang_one = Fraction(raw_a)
                    user_input_for_wan_quan_ping_fang_two = Fraction(raw_b)
                    ansers_for_wan_quan_ping_fang = user_input_for_wan_quan_ping_fang_one ** 2 + 2 * user_input_for_wan_quan_ping_fang_one * user_input_for_wan_quan_ping_fang_two + user_input_for_wan_quan_ping_fang_two ** 2
                    st.success(f"🎉 Expanded Result: {str(ansers_for_wan_quan_ping_fang)}")
                except ValueError:
                    st.error("❌ Error: Please enter integers or decimals.")

        elif adv_choice == "3. Pythagorean Theorem Unknown Side":
            st.markdown("#### Pythagorean Theorem Solver")
            py_mode = st.radio("What do you want to solve for?", ["Hypotenuse (求斜邊)", "Leg Side (求直角邊)"])
            if py_mode == "Hypotenuse (求斜邊)":
                raw_a = st.text_input("Enter leg length A:")
                raw_b = st.text_input("Enter leg length B:")
                if st.button("CALCULATE HYPOTENUSE"):
                    try:
                        a = Fraction(raw_a)
                        b = Fraction(raw_b)
                        ans = (a ** 2 + b ** 2) ** 0.5
                        st.success(f"🎉 Hypotenuse length: {to_fraction_str(ans)}") # ✅ 優化：用格式化函數美化輸出
                    except ValueError:
                        st.error("❌ Error: Please enter valid numbers.")
            else:
                raw_a = st.text_input("Enter known leg length:")
                raw_c = st.text_input("Enter hypotenuse length:")
                if st.button("CALCULATE LEG SIDE"):
                    try:
                        a = Fraction(raw_a)
                        c = Fraction(raw_c)
                        if a >= c:
                            st.warning("⚠️ Error: The leg cannot be greater than or equal to the hypotenuse!")
                        else:
                            ans = (c ** 2 - a ** 2) ** 0.5
                            st.success(f"🎉 The other leg length: {to_fraction_str(ans)}") # ✅ 優化：用格式化函數美化輸出
                    except ValueError:
                        st.error("❌ Error: Please enter valid numbers.")

        elif adv_choice == "4. Area Formulas Core":
            st.markdown("#### [Area Calculation Mode]")
            shape = st.selectbox("Please select a shape:", ["1. Rectangle / Square Area", "2. Triangle Area", "3. Circle Area"])
            if shape == "1. Rectangle / Square Area":
                c = st.text_input("Enter length:")
                d = st.text_input("Enter width:")
                if st.button("CALCULATE AREA"):
                    try:
                        c_frac = Fraction(c)
                        d_frac = Fraction(d)
                        if d_frac == c_frac:
                            st.success(f"🎉 The area of the square is: {c_frac * d_frac}")
                        else:
                            st.success(f"🎉 The area of the rectangle is: {c_frac * d_frac}")
                    except ValueError:
                        st.error("❌ Error: Please enter valid numbers.")
            elif shape == "2. Triangle Area":
                st.markdown("##### [Triangle Area Mode]")
                anser = st.text_input("Enter base length:")
                anser_ = st.text_input("Enter height:")
                if st.button("CALCULATE TRIANGLE AREA"):
                    try:
                        base = Fraction(anser)
                        height = Fraction(anser_)
                        st.success(f"🎉 The area of the triangle is: {Fraction(1, 2) * base * height}")
                    except ValueError:
                        st.error("❌ Error: Please enter valid numbers.")
            elif shape == "3. Circle Area":
                st.markdown("##### [Circle Area Mode]")
                user_input_yu = st.text_input("Enter radius:")
                if st.button("CALCULATE CIRCLE AREA"):
                    try:
                        user_input_yu = Fraction(user_input_yu)
                        st.success(f"🎉 The area of the circle is approx: {float(user_input_yu) ** 2 * 3.1415926:.4f}")
                    except ValueError:
                        st.error("❌ Error: Please enter valid numbers.")

        elif adv_choice == "5. Volume Formulas Core":
            st.markdown("#### [Volume Calculation Mode]")
            v_shape = st.selectbox("Please select a formula:", ["1. Cube / Rectangular Prism Volume", "2. Cylinder Volume", "3. Cone Volume"])
            if v_shape == "1. Cube / Rectangular Prism Volume":
                l = st.text_input("Enter length:")
                w = st.text_input("Enter width:")
                h = st.text_input("Enter height:")
                if st.button("CALCULATE PRISM VOLUME"):
                    try:
                        l_f = Fraction(l)
                        w_f = Fraction(w)
                        h_f = Fraction(h)
                        st.success(f"🎉 The volume of the prism is: {l_f * w_f * h_f}")
                    except ValueError:
                        st.error("❌ Error: Please enter valid numbers.")
            elif v_shape == "2. Cylinder Volume":
                r = st.text_input("Enter base radius:")
                h = st.text_input("Enter height:")
                if st.button("CALCULATE CYLINDER VOLUME"):
                    try:
                        r_f = float(r)
                        h_f = float(h)
                        v = math.pi * (r_f ** 2) * h_f
                        st.success(f"🎉 The volume of the cylinder is approx: {v:.6f}")
                    except ValueError:
                        st.error("❌ Error: Please enter valid numbers.")
            elif v_shape == "3. Cone Volume":
                r = st.text_input("Enter base radius:")
                h = st.text_input("Enter height:")
                if st.button("CALCULATE CONNE VOLUME"):
                    try:
                        r_f = float(r)
                        h_f = float(h)
                        v = (1 / 3) * math.pi * (r_f ** 2) * h_f
                        st.success(f"🎉 The volume of the cone is approx: {v:.6f}")
                    except ValueError:
                        st.error("❌ Error: Please enter valid numbers.")

    elif menu == "6. Multi-functional Data Charts":
        st.subheader("📚 [Data Reference Charts]")
        chart_choice = st.selectbox("Select Database Chart:", [
            "1. Multiplication Table",
            "2. Prime Numbers Chart (under 1000)",
            "3. Squares Table (under 1000)",
            "4. Common Pythagorean Triples"
        ])
        
        if chart_choice == "1. Multiplication Table":
            st.code("""
1x1=1
1x2=2 2x2=4
1x3=3 2x3=6 3x3=9
1x4=4 2x4=8 3x4=12 4x4=16
1x5=5 2x5=10 3x5=15 4x5=20 5x5=25
1x6=6 2x6=12 3x6=18 4x6=24 5x6=30 6x6=36
1x7=7 2x7=14 3x7=21 4x7=28 5x7=35 6x7=42 7x7=49
1x8=8 2x8=16 3x8=24 4x8=32 5x8=40 6x8=48 7x8=56 8x8=64
1x9=9 2x9=18 3x9=27 4x9=36 5x9=45 6x9=54 7x9=63 8x9=72 9x9=81
""", language="text")

        elif chart_choice == "2. Prime Numbers Chart (under 1000)":
            st.code("""
Prime Numbers up to 1000:
2,    3,    5,    7,   11,   13,   17,   19,   23,   29, 
31,   37,   41,   43,   47,   53,   59,   61,   67,   71, 
73,   79,   83,   89,   97,  101,  103,  107,  109,  113, 
127,  131,  137,  139,  149,  151,  157,  163,  167,  173, 
179,  181,  191,  193,  197,  199,  211,  223,  227,  229, 
233,  239,  241,  251,  257,  263,  269,  271,  277,  281, 
283,  293,  307,  311,  313,  317,  331,  337,  347,  349, 
353,  359,  367,  373,  379,  383,  389,  397,  401,  409, 
419,  421,  431,  433,  439,  443,  449,  457,  461,  463, 
467,  479,  487,  491,  499,  503,  509,  521,  523,  541, 
547,  557,  563,  569,  571,  577,  587,  593,  599,  601, 
607,  613,  617,  619,  631,  641,  643,  647,  653,  659, 
661,  673,  677,  683,  691,  701,  709,  719,  727,  733, 
739,  743,  751,  757,  761,  769,  773,  779,  787,  797, 
809,  811,  821,  823,  827,  829,  839,  853,  857,  859, 
863,  877,  881,  883,  887,  907,  911,  919,  929,  937, 
941,  947,  953,  967,  971,  977,  983,  991,  997
""", language="text")

        elif chart_choice == "3. Squares Table (under 1000)":
            st.code("""
Square Numbers Chart:
1^2 = 1          2^2 = 4          3^2 = 9          4^2 = 16   
5^2 = 25         6^2 = 36         7^2 = 49         8^2 = 64   
9^2 = 81         10^2 = 100       11^2 = 121       12^2 = 144  
13^2 = 169       14^2 = 196       15^2 = 225       16^2 = 256  
17^2 = 289       18^2 = 324       19^2 = 361       20^2 = 400  
21^2 = 441       22^2 = 484       23^2 = 529       24^2 = 576  
25^2 = 625       26^2 = 676       27^2 = 729       28^2 = 784  
29^2 = 841       30^2 = 900       31^2 = 961
""", language="text")
            
            st.markdown("##### [SYSTEM DATABASE] UNLOCKED: PERFECT CUBE NUMBERS (1-1000)")
            st.code("""
┌────────────────────────────────────────────────────────────────────────┐
│  ▶▶▶ [SYSTEM DATABASE] UNLOCKED: PERFECT CUBE NUMBERS (1-1000) ◀◀◀     │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│        [CORE-A: 01-05]                   [CORE-B: 06-10]               │
│   ─────────────────────────        ─────────────────────────           │
│    [001]  01³ = 1                   [006]  06³ = 216                   │
│    [002]  02³ = 8                   [007]  07³ = 343                   │
│    [003]  03³ = 27                  [008]  08³ = 512                   │
│    [004]  04³ = 64                  [009]  09³ = 729                   │
│    [005]  05³ = 125                 [010]  10³ = 1000                  │
│                                                                        │
├────────────────────────────────────────────────────────────────────────┤
│  ▶▶▶ STATUS: SUCCESS | TOTAL: 10 CORE DATA UNITS LOGGED | [E.N.D] ◀◀◀  │
└────────────────────────────────────────────────────────────────────────┘
""", language="text")

        elif chart_choice == "4. Common Pythagorean Triples":
            st.code("""
   Legs    Hypotenuse
3 — 4 — 5
5 — 12 — 13
8 — 15 — 17
7 — 24 — 25
9 — 40 — 41
11 — 60 — 61
12 — 35 — 37
20 — 21 — 29
""", language="text")

    elif menu == "7. Perimeter Formulas Module":
        st.subheader("📏 [Perimeter Calculation Mode]")
        p_shape = st.selectbox("Select Perimeter Sub-module:", [
            "1. Rectangle Perimeter",
            "2. Triangle Perimeter",
            "3. Circle Circumference",
            "4. General Quadrilateral Perimeter"
        ])
        
        if p_shape == "1. Rectangle Perimeter":
            c = st.text_input("Rectangle Mode - Enter width:")
            d = st.text_input("Enter length:")
            if st.button("CALCULATE RECTANGLE PERIMETER"):
                try:
                    c = Fraction(c)
                    d = Fraction(d)
                    st.success(f"🎉 Rectangle perimeter is: {(c + d) * 2}")
                except ValueError:
                    st.error("❌ Error: Please enter valid numbers.")

        elif p_shape == "2. Triangle Perimeter":
            st.markdown("##### [Triangle Perimeter Mode]")
            d = st.text_input("Enter length of side 1:")
            b_side = st.text_input("Enter length of side 2:")
            c = st.text_input("Enter length of side 3:")
            if st.button("CALCULATE TRIANGLE PERIMETER"):
                try:
                    d = Fraction(d)
                    b_side = Fraction(b_side)
                    c = Fraction(c)
                    if d >= (b_side + c) or b_side >= (c + d) or c >= (d + b_side):
                        st.error("❌ Error: These sides cannot form a valid triangle!")
                    else:
                        st.success(f"🎉 The perimeter of the triangle is: {d + b_side + c}")
                except ValueError:
                    st.error("❌ Error: Please enter valid numbers.")

        elif p_shape == "3. Circle Circumference":
            st.markdown("##### Select Precision:")
            prec = st.radio("Precision standard:", ["1. Low Precision (π = 3)", "2. Normal Precision (π = 3.14)", "3. High Precision (π = 3.1415926)"])
            pi_dict = {"1. Low Precision (π = 3)": 3.0, "2. Normal Precision (π = 3.14)": 3.14, "3. High Precision (π = 3.1415926)": 3.1415926}
            pi_val = pi_dict[prec]
            r = st.text_input(f"Enter radius (Current π = {pi_val}):")
            if st.button("CALCULATE CIRCUMFERENCE"):
                try:
                    r_val = float(r)
                    st.success(f"🎉 Circumference is: {2 * pi_val * r_val}")
                except ValueError:
                    st.error("❌ Error: Please enter valid numbers.")

        elif p_shape == "4. General Quadrilateral Perimeter":
            st.markdown("##### [Quadrilateral Perimeter Mode]")
            ganjinwanshi = st.text_input("Enter side 1:")
            ganjinwanshizaiyibian = st.text_input("Enter side 2:")
            ganjinwanshidisanbian = st.text_input("Enter side 3:")
            zhongyuyaowanshilema = st.text_input("Enter side 4:")
            if st.button("CALCULATE QUADRILATERAL PERIMETER"):
                try:
                    one = Fraction(ganjinwanshi)
                    two = Fraction(ganjinwanshizaiyibian)
                    three = Fraction(ganjinwanshidisanbian)
                    four = Fraction(zhongyuyaowanshilema)
                    st.success(f"🎉 Quadrilateral perimeter is: {one + two + three + four}")
                except ValueError:
                    st.error("❌ Error: Please enter valid numbers.")

    elif menu == "8. Hexadecimal ASCII Cipher Encryption":
        st.subheader("🔒 [Hexadecimal ASCII Cipher Encryption]")
        user_input = st.text_input("Enter plaintext to encrypt:")
        if st.button("RUN ENCRYPTION MODULE"):
            if user_input:
                list_one = []
                for i in user_input:
                    list_one.append(hex(ord(i) + 3)[2:])
                clean_output = " ".join(list_one)
                st.success(f"🔒 Ciphertext: {clean_output}")
                st.code(clean_output, language="text")

    elif menu == "9. Hexadecimal ASCII Cipher Decryption":
        st.subheader("🔓 [Hexadecimal ASCII Cipher Decryption]")
        user_input = st.text_input("Enter ciphertext to decrypt:")
        if st.button("RUN DECRYPTION MODULE"):
            if user_input:
                try:
                    new_list = user_input.split()
                    new_list_ = []
                    for i in new_list:
                        new_list_.append(chr(int(i, 16) - 3))
                    clean_output = "".join(new_list_)
                    st.success(f"🔓 Decrypted Plaintext: {clean_output}")
                    st.code(clean_output, language="text")
                except Exception:
                    st.error("❌ Error: Invalid hexadecimal ciphertext. Check your input!")
