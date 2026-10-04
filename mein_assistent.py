import os
import ollama
import requests
import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="Scriton AI App", page_icon="🤖", layout="centered")

st.title("🤖 Scriton AI")
st.write("Diese App läuft jetzt permanent im Internet! Du kannst mir auch Fotos schicken.")

def hole_wetter(stadt):
    try:
        url = f"https://wttr.in{stadt}?format=%C+%t"
        antwort = requests.get(url, timeout=5)
        if antwort.status_code == 200:
            return antwort.text.strip()
    except:
        pass
    return "Leider konnte ich das Wetter gerade nicht abrufen."

# Chat-Verlauf im Speicher der Webseite merken
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hallo! Ich bin Scriton AI. Wie kann ich dir helfen? Du kannst mir jetzt auch ein Foto hochladen!"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- FOTO-FUNKTION EINBAUEN ---
# Erstellt ein Upload-Feld für Bilder (Kamera am Handy oder Datei am PC)
hochgeladenes_bild = st.file_uploader("📸 Lade ein Bild hoch oder mache ein Foto:", type=["jpg", "jpeg", "png"])

bild_bytes = None
if hochgeladenes_bild is not None:
    # Zeige das Bild in der App an
    bild = Image.open(hochgeladenes_bild)
    st.image(bild, caption="Dein hochgeladenes Foto", use_column_width=True)
    
    # Bild in das richtige Format für die KI umwandeln
    puffer = io.BytesIO()
    bild.save(puffer, format="PNG")
    bild_bytes = puffer.getvalue()

# Text-Eingabe unten
if eingabe := st.chat_input("Schreibe deiner KI oder beschreibe das Foto..."):
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
                if bild_bytes is not None:
                    # Wenn ein Bild da ist, nutzen wir das Seh-Modell 'llava'
                    antwort = ollama.chat(
                        model="llava",
                        messages=[{
                            "role": "user",
                            "content": eingabe if eingabe else "Beschreibe dieses Bild im Detail auf Deutsch.",
                            "images": [bild_bytes]
                        }]
                    )
                else:
                    # Normaler Text-Chat ohne Bild
                    system_anweisung = {"role": "system", "content": "Du bist eine hilfreiche KI und dein Name ist Scriton AI. Antworte immer freundlich auf Deutsch."}
                    alle_nachrichten = [system_anweisung] + st.session_state.messages
                    
                    antwort = ollama.chat(
                        model="llama3.2:1b",
                        messages=alle_nachrichten,
                    )
                
                antwort_text = antwort["message"]["content"]
            except:
                antwort_text = "Fehler: Bitte stelle sicher, dass das Modell auf dem Server aktiv ist!"

        antwort_platzhalter.markdown(antwort_text)
    
    st.session_state.messages.append({"role": "assistant", "content": antwort_text})
