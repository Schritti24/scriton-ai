import os
import requests
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

# --- FUNKTION: LIVE-WETTER AUS DEM INTERNET HOLEN ---
def hole_wetter(stadt):
    try:
        # Ruft ein kostenloses, schnelles Wetter-Format ab
        url = f"https://wttr.in{stadt}?format=%C+%t"
        antwort = requests.get(url, timeout=5)
        if antwort.status_code == 200:
            return antwort.text.strip()
    except:
        pass
    return "Leider konnte ich das Wetter gerade nicht abrufen."

# --- KEY-EINGABE DIREKT IN DER APP ---
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

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
            
            # --- WETTER-ABFRAGE ERKENNEN ---
            if "wetter" in eingabe.lower():
                stadt = "Mank"  # Deine Standardstadt
                woerter = eingabe.split()
                if "in" in woerter:
                    idx = woerter.index("in")
                    if idx + 1 < len(woerter):
                        stadt = woerter[idx + 1].replace("?", "")
                
                # Echte Live-Daten abrufen
                wetter_daten = hole_wetter(stadt)
                
                # Die KI nutzt die echten Daten, um einen netten Antwortsatz zu formulieren
                prompt_wetter = (
                    f"Nutze diese echten Wetterdaten: '{wetter_daten}' für die Stadt '{stadt}' "
                    f"und formuliere eine kurze, freundliche Antwort auf Deutsch für den Nutzer."
                )
                try:
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt_wetter}],
                        model="openai/gpt-oss-20b",
                    )
                    antwort_text = chat_completion.choices.message.content
                except:
                    antwort_text = f"Das Wetter in {stadt} ist aktuell: {wetter_daten}."
            
            # --- NORMALE CHAT-ANFRAGE ---
            else:
                try:
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Du bist eine hilfreiche KI und dein Name ist Scriton AI. Antworte immer freundlich auf Deutsch."},
                            {"role": "user", "content": eingabe}
                        ],
                        model="openai/gpt-oss-20b",
                    )
                    antwort_text = chat_completion.choices.message.content
                except Exception as e:
                    antwort_text = f"Fehler bei der Verbindung: {str(e)}"

            antwort_platzhalter.markdown(antwort_text)
        
        st.session_state.messages.append({"role": "assistant", "content": antwort_text})
