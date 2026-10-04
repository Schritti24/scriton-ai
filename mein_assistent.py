import os
import streamlit as st
from groq import Groq

# Setup für die App
st.set_page_config(page_title="Scriton AI App", page_icon="🤖", layout="centered")

# --- DESIGN FEST FÜR ALLE PROGRAMMIEREN (DUNKELBLAUER LOOK) ---
st.markdown("""
    <style>
    /* Hintergrund der gesamten App */
    .stApp {
        background-color: #111827 !important;
    }
    /* Alle Titel, Überschriften und normalen Texte auf Weiß setzen */
    h1, h2, h3, p, span, .stMarkdown, label {
        color: #ffffff !important;
    }
    /* Das Eingabefeld unten dunkel und mit blauem Rand stylen */
    .stChatInput textarea {
        background-color: #1f2937 !important;
        color: #ffffff !important;
        border: 1px solid #3b82f6 !important;
        border-radius: 8px !important;
    }
    /* Die Chat-Nachrichten-Boxen schicker machen */
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

# --- KEY-EINGABE DIREKT IN DER APP (UMGEHT REBOOT- UND SCANNER-FEHLER) ---
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# Falls kein Key da ist, zeigen wir ein Eingabefeld in der Seitenleiste oder oben an
if not st.session_state.api_key:
    st.info("Bitte gib deinen Groq API-Key ein, um Scriton AI zu aktivieren.")
    key_eingabe = st.text_input("Groq API Key (gsk_...)", type="password")
    if st.button("Aktivieren"):
        if key_eingabe.startswith("gsk_"):
            st.session_state.api_key = key_eingabe
            st.rerun()
        else:
            st.error("Ungültiger Schlüssel! Er muss mit 'gsk_' beginnen.")
else:
    # Wenn der Key da ist, starten wir den offiziellen Client
    client = Groq(api_key=st.session_state.api_key)

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
                # Offizieller Abruf über die Groq-Bibliothek
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "Du bist eine hilfreiche KI und dein Name ist Scriton AI. Antworte immer freundlich auf Deutsch."},
                        {"role": "user", "content": eingabe}
                    ],
                    model="llama-3.1-8b-instant",
                )
                antwort_text = chat_completion.choices.message.content
            except Exception as e:
                antwort_text = f"Fehler bei der Verbindung: {str(e)}"

            antwort_platzhalter.markdown(antwort_text)
        
        st.session_state.messages.append({"role": "assistant", "content": antwort_text})
