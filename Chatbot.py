import math
import operator
import re
import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Ask Me",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "recent" not in st.session_state:
    st.session_state.recent = []

if "rating" not in st.session_state:
    st.session_state.rating = 5

if "feedback_message" not in st.session_state:
    st.session_state.feedback_message = ""

# ============================================================
# UNIFIED COLOR PALETTES & THEME ENGINE
# ============================================================

if st.session_state.theme == "Dark":
    BG = "#0B0F19"
    SIDEBAR = "#111827"
    CARD = "#1F2937"
    TEXT = "#F9FAFB"
    MUTED = "#9CA3AF"
    BORDER = "#374151"
    INPUT_BG = "#1F2937"
    INPUT_TEXT = "#F9FAFB"
    BTN_BG = "#1F2937"
    BTN_TEXT = "#F9FAFB"
else:
    BG = "#FFFFFF"
    SIDEBAR = "#F1F5F9"
    CARD = "#F8FAFC"
    TEXT = "#0F172A"
    MUTED = "#64748B"
    BORDER = "#E2E8F0"
    INPUT_BG = "#F8FAFC"
    INPUT_TEXT = "#0F172A"
    BTN_BG = "#FFFFFF"
    BTN_TEXT = "#0F172A"

# Dynamic CSS for Star Ratings
star_css = "".join([
    f'div[class*="st-key-star_btn_{i}"] button {{ color: {"#FFD700" if i <= st.session_state.rating else MUTED} !important; }}'
    for i in range(1, 6)
])

# Inject Master Styles
st.markdown(
    f"""
    <style>
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: {BG} !important;
        color: {TEXT} !important;
    }}

    [data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child {{
        background-color: {SIDEBAR} !important;
        border-right: 1px solid {BORDER} !important;
    }}

    [data-testid="stSidebar"] * {{
        color: {TEXT} !important;
    }}

    p, span, label, div, h1, h2, h3, h4, h5, h6 {{
        color: {TEXT} !important;
    }}

    .block-container {{
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 7rem;
    }}

    .stButton > button {{
        border-radius: 10px !important;
        border: 1px solid {BORDER} !important;
        background-color: {BTN_BG} !important;
        color: {BTN_TEXT} !important;
        font-weight: 600 !important;
    }}

    .stButton > button:hover {{
        border-color: #6366F1 !important;
        color: #6366F1 !important;
    }}

    [data-testid="stChatMessage"] {{
        background-color: {CARD} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 14px !important;
        color: {TEXT} !important;
        margin-bottom: 12px !important;
    }}

    [data-testid="stBottom"], [data-testid="stBottom"] > div {{
        background-color: {BG} !important;
        padding-bottom: 20px !important;
    }}

    .stChatInputContainer {{
        background-color: {INPUT_BG} !important;
        border-radius: 14px !important;
        border: 1px solid {BORDER} !important;
    }}

    .stChatInput textarea {{
        background-color: transparent !important;
        color: {INPUT_TEXT} !important;
        font-size: 16px !important;
    }}

    .stChatInput textarea::placeholder {{
        color: {MUTED} !important;
    }}

    .brand {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 4px 0px 20px 0px;
    }}

    .brand-logo {{
        width: 42px;
        height: 42px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #4F46E5, #2563EB);
        color: #FFFFFF !important;
        font-size: 22px;
        font-weight: 800;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }}

    .brand-title {{
        font-size: 22px;
        font-weight: 800;
        color: {TEXT} !important;
    }}

    .hero {{
        text-align: center;
        padding: 80px 10px 40px 10px;
    }}

    .hero-logo {{
        width: 80px;
        height: 80px;
        border-radius: 22px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #4F46E5, #2563EB);
        color: #FFFFFF !important;
        font-size: 40px;
        font-weight: 800;
        box-shadow: 0 8px 24px rgba(79, 70, 229, 0.35);
    }}

    .hero-title {{
        color: {TEXT} !important;
        font-size: 42px;
        font-weight: 800;
        margin-top: 16px;
    }}

    .side-heading {{
        font-size: 11px;
        font-weight: 700;
        color: {MUTED} !important;
        letter-spacing: 1px;
        margin-top: 18px;
        margin-bottom: 8px;
    }}

    .online {{
        color: #10B981 !important;
        font-size: 13px;
        font-weight: 600;
    }}

    .bottom-disclaimer {{
        width: 100%;
        text-align: center;
        font-size: 12px !important;
        color: {MUTED} !important;
        margin-top: 6px;
        padding-bottom: 10px;
        font-weight: 500;
    }}

    div[class*="st-key-star_btn_"] button {{
        background: transparent !important;
        border: none !important;
        font-size: 24px !important;
        padding: 0px !important;
        box-shadow: none !important;
    }}

    {star_css}
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# DYNAMIC LANGUAGE & KNOWLEDGE LOGIC
# ============================================================

def format_number(val: float) -> str:
    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    return f"{val:.10f}".rstrip("0").rstrip(".") if isinstance(val, float) else str(val)

def is_hinglish(text: str) -> bool:
    """Checks if the user prompt contains Hindi/Hinglish vocabulary."""
    hinglish_keywords = [
        "kya", "hai", "kaise", "kaun", "batao", "bataiye", "mujhe", "mujhse", 
        "hoga", "sab", "mera", "ye", "karo", "bata", "kuch", "naam", "kaunse"
    ]
    words = re.findall(r'\b\w+\b', text.lower())
    return any(word in hinglish_keywords for word in words)

def calculate_expression(text: str, hinglish_mode: bool):
    expr = text.lower()
    
    # Square Root Queries
    if "square root" in expr or "sqrt" in expr or "vargas" in expr:
        match = re.search(r"(?:square root of|sqrt of|sqrt|root of|square root)\s*(-?\d+(?:\.\d+)?)", expr)
        if match:
            val = float(match.group(1))
            if val < 0:
                return "Negative number ka square root real numbers mein define nahi hota." if hinglish_mode else "Square root of a negative number is undefined in real numbers."
            res = math.sqrt(val)
            if hinglish_mode:
                return f"{format_number(val)} ka square root **{format_number(res)}** hai."
            return f"The square root of {format_number(val)} is **{format_number(res)}**."

    # Multi-operator BODMAS calculations (e.g. 9 * 9 - 5 + 10)
    clean_expr = expr.replace("×", "*").replace("÷", "/").replace("x", "*")
    clean_expr = clean_expr.replace("plus", "+").replace("minus", "-").replace("times", "*")
    
    found_expr = re.search(r"[\d\s\+\-\*\/\(\)\.]+", clean_expr)
    if found_expr:
        raw_math = found_expr.group(0).strip()
        if re.search(r"\d", raw_math) and re.search(r"[\+\-\*\/]", raw_math):
            try:
                res = eval(raw_math, {"__builtins__": None}, {})
                if hinglish_mode:
                    return f"Calculation ka answer **{format_number(res)}** hai."
                return f"The result of the calculation is **{format_number(res)}**."
            except Exception:
                pass

    return None

def get_answer(user_text: str) -> str:
    text = user_text.strip()
    lower = text.lower()

    if not text:
        return "Please ask a question."

    hinglish_mode = is_hinglish(text)

    # Greetings & Bot Persona
    if lower in ["hi", "hello", "hey", "hii", "namaste"]:
        return "Hello! Main aapki kya help kar sakta hu?" if hinglish_mode else "Hello! How can I help you today?"

    if "your name" in lower or "who are you" in lower or "naam kya hai" in lower or "kaun ho" in lower:
        return ("Mera naam **Ask Me** hai. Main aapke general questions, programming queries, "
                "aur complex math problems solve kar sakta hu!") if hinglish_mode else (
                "I am **Ask Me**, your assistant for general questions, programming concepts, and mathematical calculations.")

    # Programming Knowledgebase
    if "sql" in lower:
        return ("SQL (Structured Query Language) ek standard database programming language hai. "
                "Iska use relational databases ko manage, search, update, aur query karne ke liye hota hai.") if hinglish_mode else (
                "SQL stands for Structured Query Language. It is a standard programming language designed for managing, searching, and updating relational databases.")

    if "python" in lower:
        return ("Python ek high-level, general-purpose programming language hai jo simple aur easy-to-read syntax ke liye jaani jaati hai. "
                "Ye AI, Machine Learning, Web Development, aur Data Analysis mein bohot popular hai.") if hinglish_mode else (
                "Python is a high-level, general-purpose programming language known for its clean, easy-to-read syntax. It is widely used in AI, web development, and data analysis.")

    if "javascript" in lower or " js " in lower:
        return ("JavaScript web browsers ki main programming language hai jo websites ko dynamic aur interactive banati hai. "
                "Node.js ki madad se ye servers par bhi run hoti hai.") if hinglish_mode else (
                "JavaScript is a core programming language of the web used to build dynamic and interactive websites. It runs inside web browsers and on servers using Node.js.")

    if "html" in lower:
        return ("HTML (HyperText Markup Language) web pages ka structure aur layout design karne ke liye standard markup language hai. "
                "Ye tags aur elements ka use karke content organise karti hai.") if hinglish_mode else (
                "HTML stands for HyperText Markup Language. It is the standard markup language used to structure web pages and organize web content using tags and elements.")

    if "c++" in lower or "cpp" in lower:
        return ("C++ ek high-performance compiled programming language hai. Ye low-level memory management allow karti hai "
                "aur games, operating systems, aur performance-critical applications banane mein use hoti hai.") if hinglish_mode else (
                "C++ is a high-performance, compiled programming language that provides low-level memory management and is widely used for games and system software.")

    # Math Calculation Check
    calc_res = calculate_expression(text, hinglish_mode)
    if calc_res:
        return calc_res

    if hinglish_mode:
        return f"Aapka query mila: '{text}'. Mujhe batayein agar aapko koi topic samajhna hai ya math problem calculate karni hai!"
    
    return f"I received your request: '{text}'. Let me know if you would like me to explain any topic or calculate something for you!"

def new_chat():
    st.session_state.messages = []
    st.session_state.feedback_message = ""

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        f"""
        <div class="brand">
            <div class="brand-logo">✦</div>
            <div class="brand-title">Ask Me</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("＋ New Chat", use_container_width=True):
        new_chat()
        st.rerun()

    st.markdown('<div class="side-heading">RECENT</div>', unsafe_allow_html=True)
    if not st.session_state.recent:
        st.caption("No recent questions")
    else:
        for idx, q in enumerate(st.session_state.recent[:8]):
            label = q if len(q) <= 28 else q[:28] + "..."
            if st.button(label, key=f"recent_{idx}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": q})
                st.session_state.messages.append({"role": "assistant", "content": get_answer(q)})
                st.rerun()

    st.markdown("---")
    st.markdown('<div class="side-heading">THEME</div>', unsafe_allow_html=True)
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        if st.button("☀ Light", use_container_width=True):
            st.session_state.theme = "Light"
            st.rerun()
    with col_t2:
        if st.button("☾ Dark", use_container_width=True):
            st.session_state.theme = "Dark"
            st.rerun()

    st.markdown("---")
    st.markdown('<div class="side-heading">STATUS</div>', unsafe_allow_html=True)
    st.markdown('<div class="online">● Online</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="side-heading">RATE US</div>', unsafe_allow_html=True)

    star_cols = st.columns(5)
    feedback_msgs = {
        1: "We are sorry to hear that! We will work on making this better.",
        2: "Thank you for the feedback. We will work to improve!",
        3: "Thanks! Let us know how we can make your experience even better.",
        4: "Awesome! Glad you are enjoying Ask Me.",
        5: "Thank you so much! We are thrilled that you love using Ask Me!"
    }

    for i in range(1, 6):
        if star_cols[i - 1].button("★", key=f"star_btn_{i}"):
            st.session_state.rating = i
            st.session_state.feedback_message = feedback_msgs[i]
            st.rerun()

    if st.session_state.feedback_message:
        if st.session_state.rating <= 2:
            st.warning(st.session_state.feedback_message)
        else:
            st.success(st.session_state.feedback_message)

# ============================================================
# MAIN INTERFACE
# ============================================================

if not st.session_state.messages:
    st.markdown('<div class="hero"><div class="hero-logo">✦</div><div class="hero-title">Ask Me</div></div>', unsafe_allow_html=True)
else:
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:20px;">
            <div class="brand-logo" style="width:36px; height:36px; font-size:18px;">✦</div>
            <div style="font-size:24px; font-weight:800; color:{TEXT};">Ask Me</div>
        </div>
        """,
        unsafe_allow_html=True
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask me anything...")

if prompt:
    user_prompt = prompt.strip()
    if user_prompt:
        st.session_state.messages.append({"role": "user", "content": user_prompt})

        if user_prompt in st.session_state.recent:
            st.session_state.recent.remove(user_prompt)
        st.session_state.recent.insert(0, user_prompt)
        st.session_state.recent = st.session_state.recent[:8]

        response = get_answer(user_prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

st.markdown('<div class="bottom-disclaimer">Ask Me is an AI and can make mistakes.</div>', unsafe_allow_html=True)