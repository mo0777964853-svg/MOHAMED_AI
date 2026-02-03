import streamlit as st
from groq import Groq

# --- CONFIGURATION ZA GROQ ---
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="MOHAMED_AI", page_icon="🤖", layout="wide")

# --- 2. CSS YA KUREKEBISHA MPANGILIO NA RANGI ---
st.markdown("""
    <style>
    /* Background na Font ya Msingi */
    .stApp {
        background-color: #f0f2f5;
        color: #000000;
    }

    /* Kurekebisha Chat Bubbles zisivurugike */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0px !important;
    }

    /* Box la Ujumbe wa Mtumiaji (User) */
    .user-bubble {
        background-color: #0084ff;
        color: white !important;
        padding: 12px 18px;
        border-radius: 20px 20px 0px 20px;
        margin-left: auto;
        max-width: 80%;
        width: fit-content;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }

    /* Box la Ujumbe wa AI (Assistant) */
    .ai-bubble {
        background-color: #ffffff;
        color: #000000 !important;
        padding: 12px 18px;
        border-radius: 20px 20px 20px 0px;
        margin-right: auto;
        max-width: 80%;
        width: fit-content;
        border: 1px solid #ddd;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* Kichwa cha Mfumo */
    .header-container {
        text-align: center;
        padding: 15px;
        background: white;
        border-bottom: 3px solid #0084ff;
        margin-bottom: 30px;
    }

    /* Kuficha alama za icons zilizokuwa zinaleta shida */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {
        display: none !important;
    }

    /* Input box iwe safi */
    .stChatInputContainer {
        padding: 10px !important;
        background-color: transparent !important;
    }
    
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>

    <div class="header-container">
        <h1 style="color: #0084ff; margin:0;">MOHAMED_AI</h1>
        <p style="color: #666; margin:0;">Msaidizi Wako Mahiri</p>
    </div>
    """, unsafe_allow_html=True)

# --- 3. LOGIC YA CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages kwa kutumia Custom HTML
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-bubble">{message["content"]}</div>', unsafe_allow_html=True)

# User Input
if prompt := st.chat_input("Andika ujumbe hapa..."):
    # Hifadhi na onyesha swali la mtumiaji
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="user-bubble">{prompt}</div>', unsafe_allow_html=True)

    # Response kutoka kwa AI
    full_response = ""
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Wewe ni MOHAMED_AI, msaidizi mwerevu. Jibu maswali kwa usahihi na ufasaha."},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            ],
            stream=False, # Tumeizima stream kwa muda ili kuzuia glitch ya muonekano
        )
        full_response = completion.choices[0].message.content
        st.markdown(f'<div class="ai-bubble">{full_response}</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error("Tatizo la kiufundi limetokea.")

    st.session_state.messages.append({"role": "assistant", "content": full_response})
