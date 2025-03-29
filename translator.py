import streamlit as st
import requests
from typing import Dict, Optional
from googletrans import Translator
from gtts import gTTS
import os
import time
import asyncio
import json

# Expanded language code lookup dictionary
LANGUAGE_CODES = {
    "english": "en",
    "spanish": "es",
    "french": "fr",
    "german": "de",
    "italian": "it",
    "portuguese": "pt",
    "russian": "ru",
    "chinese": "zh",
    "japanese": "ja",
    "korean": "ko",
    "arabic": "ar",
    "afrikaans": "af",
    "albanian": "sq",
    "armenian": "hy",
    "azerbaijani": "az",
    "basque": "eu",
    "belarusian": "be",
    "bengali": "bn",
    "bosnian": "bs",
    "bulgarian": "bg",
    "catalan": "ca",
    "cebuano": "ceb",
    "croatian": "hr",
    "czech": "cs",
    "danish": "da",
    "dutch": "nl",
    "esperanto": "eo",
    "estonian": "et",
    "filipino": "tl",
    "finnish": "fi",
    "galician": "gl",
    "georgian": "ka",
    "greek": "el",
    "gujarati": "gu",
    "haitian creole": "ht",
    "hausa": "ha",
    "hebrew": "he",
    "hindi": "hi",
    "hmong": "hmn",
    "hungarian": "hu",
    "icelandic": "is",
    "igbo": "ig",
    "indonesian": "id",
    "irish": "ga",
    "javanese": "jv",
    "kannada": "kn",
    "kazakh": "kk",
    "khmer": "km",
    "kurdish": "ku",
    "kyrgyz": "ky",
    "lao": "lo",
    "latvian": "lv",
    "lithuanian": "lt",
    "luxembourgish": "lb",
    "macedonian": "mk",
    "malagasy": "mg",
    "malay": "ms",
    "malayalam": "ml",
    "maltese": "mt",
    "maori": "mi",
    "marathi": "mr",
    "mongolian": "mn",
    "myanmar": "my",
    "nepali": "ne",
    "norwegian": "no",
    "persian": "fa",
    "polish": "pl",
    "punjabi": "pa",
    "romanian": "ro",
    "serbian": "sr",
    "sinhala": "si",
    "slovak": "sk",
    "slovenian": "sl",
    "somali": "so",
    "sundanese": "su",
    "swahili": "sw",
    "swedish": "sv",
    "tajik": "tg",
    "tamil": "ta",
    "telugu": "te",
    "thai": "th",
    "turkish": "tr",
    "ukrainian": "uk",
    "urdu": "ur",
    "uzbek": "uz",
    "vietnamese": "vi",
    "welsh": "cy",
    "xhosa": "xh",
    "yiddish": "yi",
    "yoruba": "yo",
    "zulu": "zu"
}

def translate(text: str, source: str, target: str, api_key: str = "") -> Dict[str, str]:
    """Translate text using MyMemory API."""
    url = "https://api.mymemory.translated.net/get"
    payload = {"q": text, "langpair": f"{source}|{target}"}
    
    try:
        response = requests.get(url, params=payload)
        response.raise_for_status()
        data = response.json()
        return {
            "translated": data["responseData"]["translatedText"],
            "detected_source_language": source if source != "auto" else "auto-detected",
        }
    except requests.RequestException as e:
        raise Exception(f"Translation API error: {str(e)}")

async def google_translate(text: str, source: str, target: str) -> Dict[str, str]:
    """Translate text using Google Translate (asynchronous)."""
    translator = Translator()
    try:
        result = await translator.translate(text, src="auto" if source == "auto" else source, dest=target)
        return {
            "translated": result.text,
            "detected_source_language": result.src,
        }
    except Exception as e:
        raise Exception(f"Google Translate error: {str(e)}")

def text_to_speech(text: str, lang: str, output_file: str = "output.mp3"):
    """Convert text to speech using gTTS."""
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(output_file)
        return output_file
    except Exception as e:
        raise Exception(f"Text-to-Speech error: {str(e)}")

def get_language_code(lang_name: str) -> Optional[str]:
    """Convert language name to language code."""
    return LANGUAGE_CODES.get(lang_name.lower().strip())

def suggest_languages(partial: str) -> list:
    """Suggest languages based on partial input."""
    return [lang for lang in LANGUAGE_CODES.keys() if lang.startswith(partial.lower())]

def generate_flashcards(text: str, translated: str, source_lang: str, target_lang: str) -> list:
    """Generate flashcards from source and translated text."""
    source_words = text.split()
    translated_words = translated.split()
    
    max_length = max(len(source_words), len(translated_words))
    source_words.extend([""] * (max_length - len(source_words)))
    translated_words.extend([""] * (max_length - len(translated_words)))

    flashcards = [
        {"front": source_words[i], "back": translated_words[i], "source_lang": source_lang, "target_lang": target_lang}
        for i in range(max_length) if source_words[i] and translated_words[i]
    ]
    return flashcards

def save_flashcards(flashcards: list, filename: str = "flashcards.json"):
    """Save flashcards to a JSON file."""
    try:
        existing_flashcards = []
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    f.seek(0)
                    existing_flashcards = json.load(f)

        existing_flashcards.extend(flashcards)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(existing_flashcards, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        st.error(f"Error saving flashcards: {str(e)}")
        return False

def load_flashcards(filename: str = "flashcards.json") -> list:
    """Load flashcards from a JSON file."""
    try:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    f.seek(0)
                    return json.load(f)
                return []
        return []
    except Exception as e:
        st.error(f"Error loading flashcards: {str(e)}")
        return []

def delete_flashcard(index: int, filename: str = "flashcards.json"):
    """Delete a specific flashcard by index from the JSON file."""
    try:
        flashcards = load_flashcards(filename)
        if 0 <= index < len(flashcards):
            del flashcards[index]
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(flashcards, f, ensure_ascii=False, indent=4)
            return True
        else:
            st.error("Invalid flashcard index.")
            return False
    except Exception as e:
        st.error(f"Error deleting flashcard: {str(e)}")
        return False

def main():
    st.set_page_config(page_title="🌍 LinguaSphere", page_icon="✨", layout="wide")

    # Minimal CSS for buttons and header
    st.markdown("""
        <style>
        .h1 {
            color: #4CAF50;
            text-align: center;
            font-size: 36px;
            margin-bottom: 0;
        }
        .subtitle {
            font-size: 20px;
            color: #666;
            text-align: center;
            margin-top: 5px;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            width: 200px;
            height: 40px;
            font-size: 16px;
            margin: 10px auto;
            display: block;
        }
        .delete-button {
            background-color: #FF4B4B;
            color: white;
            border-radius: 5px;
            width: 50px;
            height: 30px;
            font-size: 14px;
            margin-top: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown('<h1 class="h1">🌍 LinguaSphere App 🌍</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Translate, Speak, and Learn - All in One Place!</p>', unsafe_allow_html=True)
    st.write(" ")

    # Sidebar
    with st.sidebar:
        st.header("🚀 Get Started")
        st.write("Explore the power of language with LinguaSphere App!")
        st.write("Translate text between 80+ languages!")

        st.header("🎛️ Options")
        translation_method = st.radio(
            "Translation Method",
            options=["MyMemory API", "Google Translate"],
            index=0,
            horizontal=True
        )

        st.header("🔊 Speech")
        enable_speech_output = st.checkbox("Enable Speech Output", value=False, help="Hear translations aloud!")

        if st.button("💾 Save Flashcards"):
            if st.session_state.get("flashcards", []):
                if save_flashcards(st.session_state.flashcards):
                    st.success("Flashcards saved successfully!")
                st.session_state.flashcards = []
            else:
                st.warning("No flashcards to save yet.")


        st.header("📞 Contact")
        st.write("📧 Email: spreveen123@gmail.com")
        st.write("📱 Phone: +91 94889 60369")

        st.header("💬 Feedback")
        feedback = st.text_area("Tell us what you think!", placeholder="Your feedback helps us grow...")
        if st.button("Submit Feedback"):
            if feedback.strip():
                st.success("Thanks for your feedback! 🌟")
            else:
                st.warning("Please share some thoughts first!")

    # Main Content
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            source_lang_options = (
                ["Choose a language"] + ["Auto-Detect"] + sorted(LANGUAGE_CODES.keys())
                if translation_method == "Google Translate"
                else ["Choose a language"] + sorted(LANGUAGE_CODES.keys())
            )
            source_lang = st.selectbox(
                "🌍 Source Language",
                options=source_lang_options,
                index=0,
                help="Select or auto-detect your input language"
            )
        
        with col2:
            target_lang_options = ["Choose a language"] + sorted(LANGUAGE_CODES.keys())
            target_lang = st.selectbox(
                "🎯 Target Language",
                options=target_lang_options,
                index=0,
                help="Choose the language to translate into"
            )

        text = st.text_area(
            "✍️ Enter Text",
            height=150,
            placeholder="Type or paste text here to translate...",
            help="Start typing to begin your translation journey!"
        )   

    if "translation_result" not in st.session_state:
        st.session_state.translation_result = None
    if "flashcards" not in st.session_state:
        st.session_state.flashcards = []

    if st.button("🌟 Translate Now"):
        if not text.strip():
            st.warning("Please enter some text to translate.")
        elif source_lang == "Choose a language" or target_lang == "Choose a language":
            st.warning("Please select both source and target languages.")
        else:
            source_code = get_language_code(source_lang) if source_lang != "Auto-Detect" else "auto"
            target_code = get_language_code(target_lang)
            
            if target_code:
                with st.spinner("Translating your text..."):
                    try:
                        if translation_method == "MyMemory API":
                            if source_lang == "Auto-Detect":
                                st.error("Auto-Detect is not supported by MyMemory API. Please select a source language.")
                                return
                            result = translate(text, source_code, target_code)
                        else:
                            result = asyncio.run(google_translate(text, source_code, target_code))

                        st.session_state.translation_result = result
                        st.success("Translation ready! 🎉")
                        
                        with st.expander("📜 Translation Results", expanded=True):
                            st.write(f"**Original ({source_lang.capitalize()}):** {text}")
                            st.write(f"**Translated ({target_lang.capitalize()}):** {result['translated']}")
                            detected_language_name = next(
                                (name for name, code in LANGUAGE_CODES.items() if code == result['detected_source_language']),
                                "Unknown"
                            )
                            st.write(f"**Detected Language:** {detected_language_name.capitalize()}")

                        

                        if enable_speech_output:
                            try:
                                speech_file = text_to_speech(result['translated'], target_code)
                                st.audio(speech_file, format="audio/mp3")
                                st.write("🔊 Listen to your translation above!")
                            except Exception as e:
                                st.error(f"Speech Output Error: {str(e)}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

                    st.session_state.flashcards = generate_flashcards(text, result['translated'], source_lang, target_lang)
                    if st.session_state.flashcards:
                        st.info("Save the Flashcard if needed, then View the Flashcard below.")

    if st.button("📚 View Flashcards"):
        flashcards = load_flashcards()
        if flashcards:
            with st.expander("📖 Your Flashcards", expanded=True):
                for i, card in enumerate(flashcards):
                    with st.container():
                        st.write(f"📝 **Card {i + 1}**")
                        col_left, col_right = st.columns([6, 1])
                        with col_left:
                            st.write(f"🌐 **Front** ({card['source_lang'].capitalize()}): {card['front']}")
                            st.write(f"🎯 **Back** ({card['target_lang'].capitalize()}): {card['back']}")
                        with col_right:
                            if st.button("🗑️", key=f"delete_{i}", help="Delete this flashcard", on_click=delete_flashcard, args=(i,)):
                                st.success(f"Card {i + 1} deleted!")
                                st.experimental_rerun()
                        st.write("---" * 10)
        else:
            st.info("No flashcards saved yet. Translate some text to get started!")

if __name__ == "__main__":
    main()