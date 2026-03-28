import streamlit as st
from googletrans import Translator
from gtts import gTTS
import speech_recognition as sr
from pydub import AudioSegment

# Initialize
translator = Translator()

st.set_page_config(page_title="Multilingual Translator", layout="centered")
st.title("🌍 Multilingual Translator App")
st.markdown("Translate text, audio, and songs")

# Language dictionary
lang_dict = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml"
}

# Sidebar
menu = st.sidebar.selectbox("Choose Feature", [
    "Text Translator",
    "Audio Translator",
    "Song Translator 🎵"
])

# Language selection
selected_lang = st.selectbox("🌍 Select Output Language", list(lang_dict.keys()))
lang_code = lang_dict[selected_lang]

# =========================
# TEXT TRANSLATOR
# =========================
if menu == "Text Translator":
    st.subheader("📝 Text Translator")

    text = st.text_area("Enter text:")

    if st.button("Translate Text"):
        if text:
            result = translator.translate(text, dest=lang_code)
            st.success(result.text)

            tts = gTTS(result.text, lang=lang_code)
            tts.save("voice.mp3")
            st.audio("voice.mp3")

# =========================
# AUDIO TRANSLATOR
# =========================
elif menu == "Audio Translator":
    st.subheader("🎤 Audio → Translate")

    audio_file = st.file_uploader("Upload speech audio", type=["mp3", "wav"])

    if audio_file:
        st.audio(audio_file)

        if st.button("Translate Audio"):
            try:
                with open("audio.mp3", "wb") as f:
                    f.write(audio_file.getbuffer())

                sound = AudioSegment.from_file("audio.mp3")
                sound.export("audio.wav", format="wav")

                r = sr.Recognizer()
                with sr.AudioFile("audio.wav") as source:
                    audio_data = r.record(source)

                text = r.recognize_google(audio_data)
                st.write("📝 Recognized:", text)

                translated = translator.translate(text, dest=lang_code)
                st.success("🌍 " + translated.text)

            except Exception as e:
                st.error(str(e))

# =========================
# SONG TRANSLATOR
# =========================
elif menu == "Song Translator 🎵":
    st.subheader("🎵 Song Translator")

    st.warning("⚠️ Works best for slow songs with clear lyrics")

    song_file = st.file_uploader("Upload song (mp3)", type=["mp3"])

    if song_file:
        st.audio(song_file)

        if st.button("Translate Song"):
            try:
                with open("song.mp3", "wb") as f:
                    f.write(song_file.getbuffer())

                sound = AudioSegment.from_file("song.mp3")
                sound.export("song.wav", format="wav")

                r = sr.Recognizer()
                with sr.AudioFile("song.wav") as source:
                    audio_data = r.record(source)

                # Try recognizing lyrics
                text = r.recognize_google(audio_data)
                st.write("📝 Extracted Lyrics:", text)

                translated = translator.translate(text, dest=lang_code)
                st.success("🌍 Translated Lyrics: " + translated.text)

            except:
                st.error("❌ Could not extract lyrics. Try clearer audio.")