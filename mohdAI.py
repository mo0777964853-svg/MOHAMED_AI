import streamlit as st
from groq import Groq

# --- CONFIGURATION ZA GROQ ---
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# --- 1. SET PAGE CONFIG (Inasaidia Responsive Layout) ---
st.set_page_config(page_title="MOHAMED_AI", page_icon="🤖", layout="wide")

# --- 2. CSS KWA AJILI YA RANGI NA MULTIPLE DEVICES ---
st.markdown("""
    <style>
    /* Background angavu */
    .stApp {
        background-color: #f8f9fa;
        color: #000000;
    }

    /* Maandishi yawe meusi kwenye mfumo mzima */
    html, body, [class*="st-"] {
        color: #000000 !important;
        font-family: 'Inter', sans-serif;
    }

    /* Kichwa cha Habari - Responsive Font Size */
    .header-container {
        text-align: center;
        padding: 20px;
        background: white;
        border-bottom: 2px solid #6a11cb;
        margin-bottom: 20px;
    }

    .header-title {
        font-size: clamp(24px, 5vw, 45px); /* Inajirekebisha kulingana na kioo */
        font-weight: 800;
        color: #6a11cb;
    }

    /* Chat Bubbles - Responsive Width */
    [data-testid="stChatMessage"] {
        max-width: 90%; /* Kwenye simu inachukua nafasi kubwa */
        margin: auto;
        margin-bottom: 15px;
        border-radius: 15px;
        background-color: #ffffff !important;
        border: 1px solid #dee2e6 !important;
    }

    /* Kwenye Screen kubwa (PC) fanya chat iwe katikati */
    @media (min-width: 768px) {
        [data-testid="stChatMessage"] {
            max-width: 70%;
        }
    }

    /* Rangi ya maandishi ndani ya majibu ya AI na User */
    .stMarkdown p {
        color: #000000 !important;
        font-size: 16px;
        line-height: 1.6;
    }

    /* Input box iwe wazi na ionekane vizuri */
    .stChatInputContainer {
        border-top: 1px solid #ddd !important;
        background-color: white !important;
    }
    
    /* Hide Streamlit elements */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>

    <div class="header-container">
        <div class="header-title">MOHAMED_AI</div>
        <p style="color: #444;">Msaidizi Mahiri kwa Kila Kifaa</p>
    </div>
    """, unsafe_allow_html=True)

# --- 3. LOGIC YA CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("⚙️ Mipangilio")
    if st.button("Futa Chat"):
        st.session_state.messages = []
        st.rerun()

# Onyesha Historia (Display messages)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(f'<div style="color: black;">{message["content"]}</div>', unsafe_allow_html=True)

# User Input
if prompt := st.chat_input("Andika swali lako hapa..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f'<div style="color: black;">{prompt}</div>', unsafe_allow_html=True)

    # Response Generation
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Wewe ni MOHAMED_AI. Jibu maswali yote kwa lugha ya mtumiaji. Hakikisha majibu yako ni meusi na rahisi kusomeka."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                stream=True,
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(f'<div style="color: black;">{full_response} ▌</div>', unsafe_allow_html=True)
            
            message_placeholder.markdown(f'<div style="color: black;">{full_response}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error("Samahani, kuna tatizo la muunganisho.")

    st.session_state.messages.append({"role": "assistant", "content": full_response})
