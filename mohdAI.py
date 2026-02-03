import streamlit as st
from groq import Groq

# --- CONFIGURATION ZA GROQ ---
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="MOHAMED_AI", page_icon="🤖", layout="wide")

# --- 2. HTML & CSS INJECTION (MUONEKANO ANGAVU) ---
st.markdown("""
    <style>
    /* Background ya App (Rangi Angavu/Light Mode) */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        color: #2d3436;
    }

    /* Kichwa cha Habari */
    .header-container {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    .header-title {
        background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 45px;
        font-weight: 800;
        letter-spacing: 1px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Chat Messages Styles */
    .stChatMessage {
        border-radius: 15px !important;
        padding: 15px !important;
        margin-bottom: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
    }

    /* Ujumbe wa User */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #ffffff !important;
        border: 1px solid #e0e0e0 !important;
        color: #2d3436 !important;
    }

    /* Ujumbe wa AI */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #e3f2fd !important;
        border: 1px solid #bbdefb !important;
        color: #1565c0 !important;
    }

    /* Input Bar */
    .stChatInputContainer {
        border-radius: 30px !important;
        background: white !important;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05) !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: white !important;
        border-right: 1px solid #eee;
    }

    /* Hide Streamlit elements */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>

    <div class="header-container">
        <div class="header-title">MOHAMED_AI</div>
        <p style="color: #636e72; font-weight: 500;">Msaidizi Wako wa Akili ya Artificial</p>
    </div>
    """, unsafe_allow_html=True)

# --- 3. LOGIC YA CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.markdown("<h2 style='color: #2575fc;'>Dashboard</h2>", unsafe_allow_html=True)
    st.write("Mfumo: **MOHAMED_AI**")
    st.write("Hali: **Online**")
    if st.button("🗑️ Futa Maongezi"):
        st.session_state.messages = []
        st.rerun()

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Andika hapa..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Response Generation
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Wewe ni MOHAMED_AI, msaidizi mwerevu na mwenye heshima. Jibu maswali kwa usahihi."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                stream=True,
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + " ▌")
            
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Kuna tatizo: {e}")

    st.session_state.messages.append({"role": "assistant", "content": full_response})