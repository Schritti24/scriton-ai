import os
import ollama
import requests
import streamlit as st

st.set_page_config(page_title="Scriton AI App", page_icon="🤖", layout="centered")

st.title("🤖 Scriton AI")
st.write("Diese App läuft jetzt auf deinem PC und deinem Handy!")

def hole_wetter(stadt):
    try:
        url = f"https://wttr.in{stadt}?format=%C+%t"
        antwort = requests.get(url, timeout=5)
        if antwort.status_code == 200:
            return antwort.text.strip()
    except:
        pass
    return "Leider konnte ich das Wetter gerade nicht abrufen."

def liste_desktop_dateien():
    try:
        dateien = os.listdir(".")
        assistent_dateien = [d for d in dateien if os.path.isfile(d)]
        if assistent_dateien:
            return ", ".join(assistent_dateien[:10])
        return "Keine Dateien gefunden."
    except Exception as e:
        return f"Fehler: {e}"

# Die erste Begrüßung der KI beim Starten der App
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hallo! Ich bin Scriton AI. Wie kann ich dir heute helfen?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if eingabe := st.chat_input("Schreibe deiner KI..."):
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
            
        elif "datei" in eingabe.lower() or "ordner" in eingabe.lower():
            dateien_liste = liste_desktop_dateien()
            antwort_text = f"Ich habe nachgesehen. Folgende Dateien liegen im Ordner: {dateien_liste}."
            
        else:
            try:
                # Hier befehlen wir der KI fest im Gedächtnis, dass sie Scriton AI heißt:
                system_anweisung = {"role": "system", "content": "Du bist eine hilfreiche KI und dein Name ist Scriton AI. Antworte immer freundlich auf Deutsch."}
                alle_nachrichten = [system_anweisung] + st.session_state.messages
                
                antwort = ollama.chat(
                    model="llama3.2:1b",
                    messages=alle_nachrichten,
                )
                antwort_text = antwort["message"]["content"]
            except:
                antwort_text = "Fehler: Bitte starte das Programm 'Ollama' im Hintergrund!"

        antwort_platzhalter.markdown(antwort_text)
    
    st.session_state.messages.append({"role": "assistant", "content": antwort_text})
