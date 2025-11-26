
import os
from groq import Groq
import streamlit as st

# -----------------------------------------------------------
# PAGE SETTINGS
# -----------------------------------------------------------
st.set_page_config(
    page_title="Smart Calculator",
    page_icon="🧮",
    layout="centered"
)

# custom modern CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1f1c2c, #928dab);
        color: white;
    }
    .stButton>button {
        font-size: 18px;
        padding: 10px 25px;
        border-radius: 10px;
        background-color: #6C5DD3;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #5347B8;
        color: #fff;
        transform: scale(1.03);
    }
    .calculator-box {
        background: rgba(255, 255, 255, 0.15);
        padding: 25px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    .section-title {
        font-size: 26px !important;
        font-weight: 700 !important;
        color: #FFD369 !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------
# PAGE TITLE
# -----------------------------------------------------------
st.title("🧮 Smart Calculator")
st.markdown("<p style='color:#F8F8F2;'>Modern UI • Fast • Groq-Powered</p>", unsafe_allow_html=True)


# -----------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------
def create_groq_client():
    """Load Groq API key from environment."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return None, "❌ GROQ_API_KEY is missing. Please add it in Colab Secrets."
    try:
        return Groq(api_key=api_key), None
    except Exception as e:
        return None, f"Error creating Groq client: {e}"


def calculate(a, b, op):
    """Perform basic arithmetic."""
    if op == "Add (+)":
        return a + b, "+"
    if op == "Subtract (-)":
        return a - b, "-"
    if op == "Multiply (×)":
        return a * b, "×"
    if op == "Divide (÷)":
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a / b, "÷"
    raise ValueError("Invalid operation selected.")


# -----------------------------------------------------------
# CALCULATOR UI
# -----------------------------------------------------------
st.markdown("<div class='calculator-box'>", unsafe_allow_html=True)

st.markdown("<h3 class='section-title'>1️⃣ Basic Calculator</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    num1 = st.number_input("Enter first number", value=0.0, format="%.6f")
with col2:
    num2 = st.number_input("Enter second number", value=0.0, format="%.6f")

operation = st.radio(
    "Choose operation:",
    ["Add (+)", "Subtract (-)", "Multiply (×)", "Divide (÷)"],
    horizontal=True
)

if "last_calc" not in st.session_state:
    st.session_state["last_calc"] = None

if st.button("Calculate"):
    try:
        result, sym = calculate(num1, num2, operation)
        st.success(f"Result: {num1} {sym} {num2} = {result}")

        st.session_state["last_calc"] = {
            "num1": num1,
            "num2": num2,
            "symbol": sym,
            "result": result,
        }
    except Exception as e:
        st.error(str(e))

st.markdown("</div>", unsafe_allow_html=True)
st.divider()


# -----------------------------------------------------------
# AI EXPLANATION (GROQ)
# -----------------------------------------------------------
st.markdown("<div class='calculator-box'>", unsafe_allow_html=True)
st.markdown("<h3 class='section-title'>2️⃣ AI Explanation (Groq LLM)</h3>", unsafe_allow_html=True)

last = st.session_state["last_calc"]

if last is None:
    st.info("Perform a calculation first to get an AI explanation.")
else:
    default_prompt = (
        f"Explain step by step how to compute {last['num1']} {last['symbol']} "
        f"{last['num2']} to get {last['result']} in a simple beginner-friendly way."
    )

    user_prompt = st.text_area("Ask the AI anything about this calculation:", value=default_prompt)

    if st.button("Explain with AI 🤖"):
        client, err = create_groq_client()
        if err:
            st.error(err)
        else:
            with st.spinner("Groq is thinking..."):
                try:
                    reply = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": user_prompt}],
                    )

                    st.subheader("📘 AI Explanation")
                    st.write(reply.choices[0].message.content)

                except Exception as e:
                    st.error(f"Groq error: {e}")

st.markdown("</div>", unsafe_allow_html=True)


# FOOTER
st.caption(
    "Made with ❤️ using Streamlit + Groq • Fully modern UI • Beginner-friendly."
)
