import os
import streamlit as st
from groq import Groq

# Setup für die App
st.set_page_config(page_title="Scriton AI App", page_icon="🤖", layout="centered")

# --- DESIGN FEST FÜR ALLE PROGRAMMIEREN (DUNKELBLAUER LOOK) ---
st.markdown("""
    <style>
    .stApp { background-color: #111827 !important; }
    h1, h2, h3, p, span, .stMarkdown, label { color: #ffffff !important; }
    .stChatInput textarea {
        background-color: #1f2937 !important;
        color: #ffffff !important;
        border: 1px solid #3b82f6 !important;
        border-radius: 8px !important;
    }
    .stChatMessage {
        background-color: #1f2937 !important;
        border-radius: 12px !important;
        padding: 10px !important;
        margin-bottom: 10px !important;
        border: 1px solid #374151 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGO UND ÜBERSCHRIFTEN ---
if os.path.exists("Scriton.png"):
    st.image("Scriton.png", width=120)

st.title("🤖 Scriton AI")
st.write("Ask your Question :)")

# Hier nutzen wir die offizielle, sichere Verbindung
@st.cache_resource
def get_groq_client():
    return Groq(api_key="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")

try:
    client = get_groq_client()
except Exception as e:
    st.error("Fehler beim Starten des KI-Clients. Bitte lade die Seite neu.")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hallo! Ich bin Scriton AI. Ich bin jetzt rund um die Uhr online. Wie kann ich dir helfen?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if eingabe := st.chat_input("Schreibe Scriton AI..."):
    with st.chat_message("user"):
        st.markdown(eingabe)
    st.session_state.messages.append({"role": "user", "content": eingabe})

    with st.chat_message("assistant"):
        antwort_platzhalter = st.empty()
        
        try:
            # Offizieller Abruf über das Groq-System
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Du bist eine hilfreiche KI und dein Name ist Scriton AI. Antworte immer freundlich auf Deutsch."},
                    {"role": "user", "content": eingabe}
                ],
                model="llama-3.1-8b-instant",
            )
            antwort_text = chat_completion.choices[0].message.content
        except Exception as e:
            antwort_text = "Fehler bei der Verbindung zum Online-Server. Bitte versuche es gleich noch einmal!"

        antwort_platzhalter.markdown(antwort_text)
    
    st.session_state.messages.append({"role": "assistant", "content": antwort_text})
