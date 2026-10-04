import os
import requests
import streamlit as st
from PIL import Image

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
# Prüfen, ob deine hochgeladene Datei Scriton.png da ist, und sie ganz oben anzeigen
if os.path.exists("Scriton.png"):
    st.image("Scriton.png", width=120)

st.title("🤖 Scriton AI")
st.write("Ask your Question :)")

def hole_wetter(stadt):
    try:
        url = f"https://wttr.in{stadt}?format=%C+%t"
        antwort = requests.get(url, timeout=5)
        if antwort.status_code == 200:
            return antwort.text.strip()
    except:
        pass
    return "Leider konnte ich das Wetter gerade nicht abrufen."

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
        antwort_text = ""
        
        if "wetter" in eingabe.lower():
            stadt = "Mank"
            woerter = eingabe.split()
            if "in" in woerter:
                idx = woerter.index("in")
                if idx + 1 < len(woerter):
                    stadt = woerter[idx + 1].replace("?", "")
            wetter_daten = hole_wetter(stadt)
            antwort_text = f"Ich habe nachgesehen. Das Wetter in {stadt} ist aktuell: {wetter_daten}."
            
        else:
            try:
                url = "https://groq.com"
                headers = {
                    "Authorization": "Bearer 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",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "llama-3.1-8b-instant",
                    "messages": [
                        {"role": "system", "content": "Du bist eine hilfreiche KI und dein Name ist Scriton AI. Antworte immer freundlich auf Deutsch."},
                        {"role": "user", "content": eingabe}
                    ]
                }
                antwort = requests.post(url, json=data, headers=headers, timeout=10)
                antwort_text = antwort.json()["choices"]["message"]["content"]
            except Exception as e:
                antwort_text = "Fehler bei der Verbindung zum Online-Server. Bitte versuche es gleich noch einmal!"

        antwort_platzhalter.markdown(antwort_text)
    
    st.session_state.messages.append({"role": "assistant", "content": antwort_text})
