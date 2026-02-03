import streamlit as st
from groq import Groq
import time

# --- CONFIGURATION ZA GROQ ---
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="MOHAMED_AI", page_icon="🤖", layout="wide")

# --- 2. CSS YA KUREKEBISHA MPANGILIO NA RANGI ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f5;
        color: #000000;
    }

    /* Kuficha icons za kizamani */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {
        display: none !important;
    }

    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0px !important;
    }

    /* Bubble la User */
    .user-bubble {
        background-color: #0084ff;
        color: white !important;
        padding: 12px 18px;
        border-radius: 20px 20px 0px 20px;
        margin-left: auto;
        max-width: 80%;
        width: fit-content;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        font-family: 'Inter', sans-serif;
    }

    /* Bubble la AI (MOHAMED_AI) */
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
        margin-bottom: 10px;
        font-family: 'Inter', sans-serif;
    }

    .header-container {
        text-align: center;
        padding: 15px;
        background: white;
        border-bottom: 3px solid #0084ff;
        margin-bottom: 30px;
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>

    <div class="header-container">
        <h1 style="color: #0084ff; margin:0; font-family: sans-serif;">MOHAMED_AI</h1>
        <p style="color: #666; margin:0;">Inajibu sasa hivi...</p>
    </div>
    """, unsafe_allow_html=True)

# --- 3. LOGIC YA CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Onyesha historia ya mazungumzo
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-bubble">{message["content"]}</div>', unsafe_allow_html=True)

# Sehemu ya kuandika (Input)
if prompt := st.chat_input("Uliza chochote kwa MOHAMED_AI..."):
    # Onyesha swali la mtumiaji mara moja
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="user-bubble">{prompt}</div>', unsafe_allow_html=True)

    # Response kutoka kwa AI yenye Typing Effect
    with st.empty():
        full_response = ""
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Wewe unaitwa MOHAMED_AI. Wewe ni msaidizi mwerevu uliyebuniwa kusaidia watu. Kamwe usiseme wewe ni Gemini au ChatGPT. Jibu maswali kwa ufasaha na maandishi meusi."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                stream=True,
            )
            
            # Hapa tunatengeneza ile "Typing Effect"
            message_placeholder = st.empty()
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    # Tunatumia HTML ndani ya placeholder ili muonekano ubaki kuwa bubble
                    message_placeholder.markdown(f'<div class="ai-bubble">{full_response} ▌</div>', unsafe_allow_html=True)
            
            # Jibu la mwisho baada ya kumaliza ku-type
            message_placeholder.markdown(f'<div class="ai-bubble">{full_response}</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error("Samahani, MOHAMED_AI amepata hitilafu kidogo.")

    st.session_state.messages.append({"role": "assistant", "content": full_response})
