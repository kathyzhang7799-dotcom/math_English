import streamlit as st
from fractions import Fraction
import time
import random
import math

# Configure web page title and icon (Must be the first Streamlit command)
st.set_page_config(page_title="THE MATRIX: CORE V8", page_icon="⚡", layout="wide")

# ==========================================
# 🌊 MATRIX DIGITAL RAIN BACKGROUND INJECTION
# ==========================================
st.markdown("""
    <canvas id="matrix-canvas" style="position:fixed; top:0; left:0; width:100vw; height:100vh; z-index:-1;"></canvas>
    <script>
    const canvas = document.getElementById('matrix-canvas');
    const ctx = canvas.getContext('2d');

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    const katakana = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ";
    const alphabet = katakana.split("");

    const fontSize = 16;
    let columns = canvas.width / fontSize;

    const rainDrops = [];
    for (let x = 0; x < columns; x++) {
        rainDrops[x] = 1;
    }

    function draw() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = '#0F0'; // Matrix Green
        ctx.font = fontSize + 'px monospace';

        for (let i = 0; i < rainDrops.length; i++) {
            const text = alphabet[Math.floor(Math.random() * alphabet.length)];
            ctx.fillText(text, i * fontSize, rainDrops[i] * fontSize);

            if (rainDrops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                rainDrops[i] = 0;
            }
            rainDrops[i]++;
        }
    }
    setInterval(draw, 30);
    </script>
    
    <style>
    /* Global App Background */
    .stApp {
        background: transparent;
    }
    
    /* Main Panel Container */
    .main .block-container {
        background-color: rgba(0, 0, 0, 0.85); 
        padding: 40px !important;
        border-radius: 15px;
        border: 1px solid #00FF00;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
        margin-top: 20px;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(5, 5, 5, 0.9) !important;
        border-right: 1px solid #00FF00;
    }
    
    /* Glowing Matrix Headers */
    h1, h2, h3, h4, h5, h6 { 
        color: #00FF00 !important; 
        text-shadow: 0 0 8px rgba(0, 255, 0, 0.6);
        font-family: 'Courier New', monospace;
    }
    
    /* Cyberpunk Buttons */
    div.stButton > button:first-child {
        background-color: #000000; 
        color: #00FF00; 
        border: 2px solid #00FF00;
        box-shadow: 0 0 10px #00FF00; 
        font-family: 'Courier New', monospace; 
        font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover { 
        background-color: #00FF00; 
        color: #000000; 
        box-shadow: 0 0 20px #00FF00;
    }
    
    /* Input Fields Styling */
    .stTextInput>div>div>input {
        background-color: #111111 !important; 
        color: #00FF00 !important; 
        border: 1px solid #00FF00 !important;
        font-family: 'Courier New', monospace;
    }
    
    /* Markdown Text & Labels */
    div[data-testid="stMarkdownContainer"] p { 
        color: #00FF00 !important; 
        font-family: 'Courier New', monospace;
    }
    label[data-testid="stWidgetLabel"] p {
        color: #00FF00 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ THE MATRIX: LOGIC SOURCE CORE V8")
st.write("Welcome to the Ultimate Math Engine. High-precision algebraic & geometric computation core built for web.")

# ==========================================
# 🎛️ SIDEBAR CONTROL CENTER
# ==========================================
st.sidebar.title("🎛️ SYSTEM CONTROL PANEL")
menu_choice = st.sidebar.selectbox(
    "Select Function Module:",
    [
        "System Initialization Index",
        "1. Addition Mode",
        "2. Subtraction Mode",
        "3. Multiplication Mode",
        "4. Division Mode",
        "5. Advanced Formulas Menu",
        "6. Multi-functional Data Charts",
        "7. Perimeter Formulas Module",
        "8. [Hexadecimal ASCII Encryption]",
        "9. [Hexadecimal ASCII Decryption]"
    ]
)

# ==========================================
# 0. SYSTEM INITIALIZATION INDEX
# ==========================================
if menu_choice == "System Initialization Index":
    st.subheader("📟 System Status: READY")
    st.write("This core engine manages high-precision fractions and geometric calculations. Switch modules using the sidebar.")
    if st.button("🧬 Run Core Database Load Check"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        progresses = [0, 13, 31, 36, 43, 44, 58, 85, 97, 100]
        for p in progresses:
            status_text.text(f"Loading Core Database... {p}%")
            progress_bar.progress(p / 100)
            time.sleep(random.uniform(0.05, 0.15))
        st.success("🟢 System database loaded successfully! Ultimate Math Engine is online.")

# ==========================================
# 1. ADDITION MODE
# ==========================================
elif menu_choice == "1. Addition Mode":
    st.subheader("➕ [Addition Mode]")
    raw_one = st.text_input("Enter 1st addend (Supports fractions/integers/decimals):", key="plus1")
    raw_two = st.text_input("Enter 2nd addend (Supports fractions/integers/decimals):", key="plus2")
    if st.button("Calculate Sum"):
        try:
            one = Fraction(raw_one)
            two = Fraction(raw_two)
            st.code(f"Result: {one} + {two} = {one + two}")
        except ValueError: st.error("❌ Error: Please enter valid numbers or fractions!")

# ==========================================
# 2. SUBTRACTION MODE
# ==========================================
elif menu_choice == "2. Subtraction Mode":
    st.subheader("➖ [Subtraction Mode]")
    raw_one = st.text_input("Enter minuend:", key="minus1")
    raw_two = st.text_input("Enter subtrahend:", key="minus2")
    if st.button("Calculate Difference"):
        try:
            one = Fraction(raw_one)
            two = Fraction(raw_two)
            st.code(f"Result: {one} - {two} = {one - two}")
        except ValueError: st.error("❌ Error: Please enter valid numbers or fractions!")

# ==========================================
# 3. MULTIPLICATION MODE
# ==========================================
elif menu_choice == "3. Multiplication Mode":
    st.subheader("✖️ [Multiplication Mode]")
    raw_one = st.text_input("Enter 1st factor:", key="mul1")
    raw_two = st.text_input("Enter 2nd factor:", key="mul2")
    if st.button("Calculate Product"):
        try:
            one = Fraction(raw_one)
            two = Fraction(raw_two)
            st.code(f"Result: {one} × {two} = {one * two}")
        except ValueError: st.error("❌ Error: Please enter valid numbers or fractions!")

# ==========================================
# 4. DIVISION MODE
# ==========================================
elif menu_choice == "4. Division Mode":
    st.subheader("➗ [Division Mode]")
    raw_one = st.text_input("Enter dividend:", key="div1")
    raw_two = st.text_input("Enter divisor:", key="div2")
    if st.button("Calculate Quotient"):
        if raw_two == "0": st.warning("⚠️ Error: Divisor cannot be zero!")
        else:
            try:
                one = Fraction(raw_one)
                two = Fraction(raw_two)
                st.code(f"Result: {one} ÷ {two} = {one / two}")
            except ValueError: st.error("❌ Error: Please enter valid numbers or fractions!")

# ==========================================
# 5. ADVANCED FORMULAS MENU
# ==========================================
elif menu_choice == "5. Advanced Formulas Menu":
    st.subheader("📐 Advanced Formulas Engine")
    sub_menu = st.radio("Select Target Formula Core:", [
        "Quadratic Equation Solver", 
        "Perfect Square Expansion", 
        "Pythagorean Theorem Unknown Side", 
        "Area Formulas Core", 
        "Volume Formulas Core"
    ])
    
    if sub_menu == "Quadratic Equation Solver":
        st.write("--- Quadratic Equation Solver (ax² + bx + c = 0) ---")
        raw_a = st.text_input("Enter coefficient a:")
        raw_b = st.text_input("Enter coefficient b:")
        raw_c = st.text_input("Enter coefficient c:")
        if st.button("Solve Equation"):
            try:
                input_one, input_two, input_three = float(raw_a), float(raw_b), float(raw_c)
                if input_one == 0: st.error("❌ Error: 'a' cannot be 0 in a quadratic equation.")
                else:
                    discriminant = input_two ** 2 - 4 * input_one * input_three
                    if discriminant < 0: st.error("❌ Error: This equation has no real roots.")
                    else:
                        ans1 = (-input_two + (discriminant ** 0.5)) / (2 * input_one)
                        ans2 = (-input_two - (discriminant ** 0.5)) / (2 * input_one)
                        st.success(f"🎉 Roots: {ans1} OR {ans2}")
            except ValueError: st.error("❌ Error: Please enter valid numbers.")

    elif sub_menu == "Perfect Square Expansion":
        st.write("--- Perfect Square Expansion (a²+2ab+b²) ---")
        raw_a = st.text_input("Enter expression 'a':", key="wan1")
        raw_b = st.text_input("Enter expression 'b':", key="wan2")
        if st.button("Expand"):
            try:
                ans = Fraction(raw_a)**2 + 2*Fraction(raw_a)*Fraction(raw_b) + Fraction(raw_b)**2
                st.success(f"🎉 Expanded Result: {str(ans)}")
            except ValueError: st.error("❌ Error: Please enter valid integers or decimals.")

    elif sub_menu == "Pythagorean Theorem Unknown Side":
        st.write("--- Pythagorean Theorem Solver ---")
        choice = st.selectbox("What do you want to solve for?", ["Solve for Hypotenuse (Given legs A and B)", "Solve for Leg Side (Given leg A and hypotenuse C)"])
        if choice == "Solve for Hypotenuse (Given legs A and B)":
            raw_a = st.text_input("Enter leg length A:")
            raw_b = st.text_input("Enter leg length B:")
            if st.button("Calculate Hypotenuse"):
                try: st.success(f"🎉 Hypotenuse length: {(Fraction(raw_a)**2 + Fraction(raw_b)**2)**0.5}")
                except ValueError: st.error("❌ Error: Invalid input parameters.")
        else:
            raw_a = st.text_input("Enter known leg length:")
            raw_c = st.text_input("Enter hypotenuse length:")
            if st.button("Calculate Missing Leg"):
                try:
                    a_f, c_f = Fraction(raw_a), Fraction(raw_c)
                    if a_f >= c_f: st.warning("⚠️ Error: The leg cannot be greater than or equal to the hypotenuse!")
                    else: st.success(f"🎉 The other leg length: {(c_f**2 - a_f**2)**0.5}")
                except ValueError: st.error("❌ Error: Invalid input parameters.")

    elif sub_menu == "Area Formulas Core":
        st.write("--- [Area Calculation Mode] ---")
        shape = st.selectbox("Select Shape Area Formula:", ["Rectangle / Square Area", "Triangle Area", "Circle Area"])
        if shape == "Rectangle / Square Area":
            c = st.text_input("Enter length:", key="area_rect1")
            d = st.text_input("Enter width:", key="area_rect2")
            if st.button("Calculate Quadrilateral Area"):
                try:
                    c_f, d_f = Fraction(c), Fraction(d)
                    name = "Square" if c_f == d_f else "Rectangle"
                    st.success(f"🎉 The area of the {name} is: {c_f * d_f}")
                except ValueError: st.error("❌ Error: Please enter valid numbers.")
        elif shape == "Triangle Area":
            base = st.text_input("Enter base length:", key="area_tri1")
            height = st.text_input("Enter height:", key="area_tri2")
            if st.button("Calculate Triangle Area"):
                try: st.success(f"🎉 The area of the triangle is: {Fraction(1, 2) * Fraction(base) * Fraction(height)}")
                except ValueError: st.error("❌ Error: Please enter valid numbers.")
        elif shape == "Circle Area":
            r = st.text_input("Enter radius:", key="area_circle")
            if st.button("Calculate Circle Area"):
                try: st.success(f"🎉 The area of the circle is approx: {Fraction(r)**2 * 3.1415926}")
                except ValueError: st.error("❌ Error: Please enter valid numbers.")

    elif sub_menu == "Volume Formulas Core":
        st.write("--- [Volume Calculation Mode] ---")
        v_shape = st.selectbox("Select Solid Figure Volume Formula:", ["Cube / Rectangular Prism Volume", "Cylinder Volume", "Cone Volume"])
        if v_shape == "Cube / Rectangular Prism Volume":
            l = st.text_input("Enter length:", key="vol_cube1")
            w = st.text_input("Enter width:", key="vol_cube2")
            h = st.text_input("Enter height:", key="vol_cube3")
            if st.button("Calculate Prism Volume"):
                try: st.success(f"🎉 The volume of the prism is: {Fraction(l)*Fraction(w)*Fraction(h)}")
                except ValueError: st.error("❌ Error: Please enter valid numbers.")
        elif v_shape == "Cylinder Volume":
            r = st.text_input("Enter base radius:", key="vol_cyl1")
            h = st.text_input("Enter height:", key="vol_cyl2")
            if st.button("Calculate Cylinder Volume"):
                try: st.success(f"🎉 The volume of the cylinder is approx: {math.pi * (float(r)**2) * float(h):.6f}")
                except ValueError: st.error("❌ Error: Please enter valid numbers.")
        elif v_shape == "Cone Volume":
            r = st.text_input("Enter base radius:", key="vol_cone1")
            h = st.text_input("Enter height:", key="vol_cone2")
            if st.button("Calculate Cone Volume"):
                try: st.success(f"🎉 The volume of the cone is approx: {(1 / 3) * math.pi * (float(r)**2) * float(h):.6f}")
                except ValueError: st.error("❌ Error: Please enter valid numbers.")

# ==========================================
# 6. MULTI-FUNCTIONAL DATA CHARTS
# ==========================================
# ==========================================
# 6. MULTI-FUNCTIONAL DATA CHARTS
# ==========================================
elif menu_choice == "6. Multi-functional Data Charts":
    st.subheader("📚 System Internal Reference Charts")
    ref_table = st.selectbox("Select Reference Table Unit:", [
        "Multiplication Table", 
        "Prime Numbers Chart (Under 1000)", 
        "Squares Table (Under 1000)", 
        "Cubes Table (Under 1000)", 
        "Common Pythagorean Triples"
    ])
    
    # CSS injection to force text wrap inside code blocks so they don't overflow the screen
    st.markdown("""
        <style>
        code {
            white-space: pre-wrap !important; /* Forces text to wrap to the next line */
            word-break: break-all !important;
        }
        </style>
    """, unsafe_allow_html=True)

    if ref_table == "Multiplication Table":
        st.code(
            "1x1=1\n"
            "1x2=2   2x2=4\n"
            "1x3=3   2x3=6   3x3=9\n"
            "1x4=4   2x4=8   3x4=12  4x4=16\n"
            "1x5=5   2x5=10  3x5=15  4x5=20  5x5=25\n"
            "1x6=6   2x6=12  3x6=18  4x6=24  5x6=30  6x6=36\n"
            "1x7=7   2x7=14  3x7=21  4x7=28  5x7=35  6x7=42  7x7=49\n"
            "1x8=8   2x8=16  3x8=24  4x8=32  5x8=40  6x8=48  7x8=56  8x8=64\n"
            "1x9=9   2x9=18  3x9=27  4x9=36  5x9=45  6x9=54  7x9=63  8x9=72  9x9=81"
        )
        
    elif ref_table == "Prime Numbers Chart (Under 1000)":
        st.write("--- Core Database: 168 Primes Under 1000 ---")
        primes_data = (
            "2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, "
            "73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, "
            "179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, "
            "283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, "
            "419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, "
            "557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, "
            "673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, "
            "821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, "
            "953, 967, 971, 977, 983, 991, 997"
        )
        st.code(primes_data)
        
    elif ref_table == "Squares Table (Under 1000)":
        st.write("--- Perfect Squares Core (1² to 31²) ---")
        squares_data = ", ".join([f"{i}²={i**2}" for i in range(1, 32)])
        st.code(squares_data)
        
    elif ref_table == "Cubes Table (Under 1000)":
        st.write("--- Perfect Cubes Core (1³ to 10³) ---")
        cubes_data = ", ".join([f"{i}³={i**3}" for i in range(1, 11)])
        st.code(cubes_data)
        
    elif ref_table == "Common Pythagorean Triples":
        st.write("--- Core Database: Essential Pythagorean Triples (a-b-c) ---")
        st.code("3-4-5,  5-12-13,  8-15-17,  7-24-25,  9-40-41,  11-60-61,  12-35-37,  20-21-29")

# ==========================================
# 7. PERIMETER FORMULAS MODULE
# ==========================================
elif menu_choice == "7. Perimeter Formulas Module":
    st.subheader("📐 Perimeter Calculation Mode")
    shape = st.selectbox("Select Perimeter Unit:", ["Rectangle Perimeter", "Triangle Perimeter", "Circle Circumference", "General Quadrilateral Perimeter"])
    
    if shape == "Rectangle Perimeter":
        c = st.text_input("Enter width:", key="peri_rec1")
        d = st.text_input("Enter length:", key="peri_rec2")
        if st.button("Calculate Rectangle Perimeter"):
            try: st.success(f"🎉 Rectangle perimeter is: {(Fraction(c)+Fraction(d))*2}")
            except ValueError: st.error("❌ Error: Please enter valid numbers.")
    elif shape == "Triangle Perimeter":
        d = st.text_input("Enter length of side 1:", key="peri_tri1")
        b_side = st.text_input("Enter length of side 2:", key="peri_tri2")
        c = st.text_input("Enter length of side 3:", key="peri_tri3")
        if st.button("Calculate Triangle Perimeter"):
            try:
                d_f, b_f, c_f = Fraction(d), Fraction(b_side), Fraction(c)
                if d_f >= (b_f+c_f) or b_f >= (c_f+d_f) or c_f >= (d_f+b_f): st.error("❌ Error: These sides cannot form a valid triangle!")
                else: st.success(f"🎉 The perimeter of the triangle is: {d_f + b_f + c_f}")
            except ValueError: st.error("❌ Error: Please enter valid numbers.")
    elif shape == "Circle Circumference":
        pi_mode = st.radio("Select Precision Mode:", ["Low Precision (π = 3)", "Normal Precision (π = 3.14)", "High Precision (π = 3.1415926)"])
        r = st.text_input("Enter radius:", key="peri_cir")
        if st.button("Calculate Circumference"):
            try:
                pi_val = 3.0 if "Low" in pi_mode else (3.14 if "Normal" in pi_mode else 3.1415926)
                st.success(f"🎉 Circumference is: {2 * pi_val * float(r)}")
            except ValueError: st.error("❌ Error: Please enter valid numbers.")
    elif shape == "General Quadrilateral Perimeter":
        g1 = st.text_input("Enter side 1:", key="p_quad1")
        g2 = st.text_input("Enter side 2:", key="p_quad2")
        g3 = st.text_input("Enter side 3:", key="p_quad3")
        g4 = st.text_input("Enter side 4:", key="p_quad4")
        if st.button("Calculate Quadrilateral Perimeter"):
            try: st.success(f"🎉 Quadrilateral perimeter is: {Fraction(g1) + Fraction(g2) + Fraction(g3) + Fraction(g4)}")
            except ValueError: st.error("❌ Error: Please enter valid numbers.")

# ==========================================
# 8. HEXADECIMAL ASCII ENCRYPTION
# ==========================================
elif menu_choice == "8. [Hexadecimal ASCII Encryption]":
    st.subheader("🔐 Hexadecimal Caesar Matrix Encryption System")
    user_input = st.text_input("Enter plaintext string to encrypt:", key="matrix_enc")
    if st.button("🔥 Inject Matrix & Encrypt"):
        if user_input:
            clean_output = " ".join([hex(ord(i) + 3)[2:] for i in user_input])
            st.info("Encryption Complete. Generated Ciphertext Stream:")
            st.code(clean_output)
        else: st.warning("Plaintext string cannot be empty.")

# ==========================================
# 9. HEXADECIMAL ASCII DECRYPTION
# ==========================================
elif menu_choice == "9. [Hexadecimal ASCII Decryption]":
    st.subheader("🔓 Hexadecimal Caesar Matrix Decryption System")
    user_input = st.text_input("Paste ciphertext data stream to crack (Space separated):", key="matrix_dec")
    if st.button("🟢 Execute Decryption Crack"):
        if user_input:
            try:
                clean_output = "".join([chr(int(i, 16) - 3) for i in user_input.split()])
                st.success("🎉 Matrix decryption successful! Restored plaintext raw data:")
                st.code(clean_output)
            except Exception: st.error("❌ Matrix Error! Please verify that the ciphertext stream is valid hex.")
        else: st.warning("Ciphertext stream cannot be empty.")

# ==========================================
# 📜 FOOTER LOGO
# ==========================================
st.markdown("---")
st.caption("© 2026 Cyber Studio | Core Driven by Streamlit Web Framework")
