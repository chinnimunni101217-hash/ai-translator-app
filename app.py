import streamlit as st
from googletrans import Translator
from gtts import gTTS


translator = Translator()

st.title("🌍 AI Translator App")

text = st.text_area("Enter text:")

lang = st.selectbox("Select Language", ["hi","ta","te","kn","ml","en"])

if st.button("Translate"):
    if text:
        result = translator.translate(text, dest=lang)
        st.success(result.text)

        tts = gTTS(result.text, lang=lang)
        tts.save("voice.mp3")

        st.audio("voice.mp3")

import speech_recognition as sr
from pydub import AudioSegment

st.subheader("🎤 Voice Input (Upload & Translate)")

audio_file = st.file_uploader("Upload audio (wav/mp3)", type=["wav", "mp3"])

if audio_file is not None:
    st.audio(audio_file)

    # Save file ONCE (important fix)
    file_bytes = audio_file.read()
    with open("input_audio", "wb") as f:
        f.write(file_bytes)

    if st.button("Translate Audio"):

        try:
            # Convert mp3 → wav if needed
            if audio_file.name.endswith(".mp3"):
                sound = AudioSegment.from_file("input_audio")
                sound.export("converted.wav", format="wav")
                audio_path = "converted.wav"
            else:
                audio_path = "input_audio"

            r = sr.Recognizer()

            with sr.AudioFile(audio_path) as source:
                audio_data = r.record(source)

            text = r.recognize_google(audio_data)
            st.write("📝 Recognized Text:", text)

            result = translator.translate(text, dest=lang)
            st.success("🌍 Translated Text: " + result.text)

        except Exception as e:
            st.error("❌ Error: " + str(e))