import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS

st.title("🌍 AI Translator App")

text = st.text_area("Enter text:")

lang = st.selectbox("Select Language", ["hi","ta","te","kn","ml","en"])

if st.button("Translate"):
    if text:
        result = GoogleTranslator(source="auto", target=lang).translate(text)
        st.success(result)

        tts = gTTS(result, lang=lang)
        tts.save("voice.mp3")
        st.audio("voice.mp3")
