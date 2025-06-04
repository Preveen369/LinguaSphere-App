# 🌍 LinguaSphere-App – Your Language Learning Companion

![Platform](https://img.shields.io/badge/Platform-Web-blue.svg)
![Tech](https://img.shields.io/badge/Frontend-Streamlit-orange.svg)
![Language](https://img.shields.io/badge/Language-Python-yellow.svg)
![APIs](https://img.shields.io/badge/APIs-GoogleTranslate%20%7C%20gTTS%20%7C%20MyMemory-green.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

**LinguaSphere-App** is a Python-based web application built with Streamlit, designed to assist language learners by providing seamless translation, text-to-speech, and language practice tools. Leveraging APIs like Google Translate, Google Text-to-Speech (gTTS), and MyMemory, this app offers an interactive platform for users to translate text, hear pronunciations, and enhance their language skills effortlessly.

---

## 🚀 Features

### 🌍 Text Translation

- Translate text across multiple languages using Google Translate and MyMemory APIs.
- Support for a wide range of languages with accurate translations.

### 🔊 Text-to-Speech

- Convert translated text to speech using Google Text-to-Speech (gTTS).
- Listen to pronunciations to improve speaking and listening skills.

### 🗂️ Flashcards for Language Practice
- Add new flashcards with words or phrases and their translations.  
- View existing flashcards to review and practice.  
- Remove flashcards when no longer needed.

### 🖥️ Interactive UI

- Clean and intuitive interface built with Streamlit.
- Easy input fields for text, language selection, and playback options.

### 📱 Responsive Design

- Streamlit’s responsive layout ensures usability on both desktop and mobile devices.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **APIs**: Google Translate, Google Text-to-Speech (gTTS), MyMemory API
- **Tools**: Python, pip

---

## 📂 Project Structure

```
LinguaSphere-App/
├── app.py                         # Main Streamlit app script for the UI and logic
├── requirements.txt               # Dependencies for the project (Streamlit, APIs, etc.)
├── config.py                      # API keys and configuration settings
├── assets/
│   ├── logo.png                   # App logo or branding image
│   └── background.jpg             # Background image for the app UI
└── utils/
    ├── translation.py             # Functions for Google Translate and MyMemory API
    └── text_to_speech.py          # Functions for Google Text-to-Speech API
```

---

## 🧪 Installation & Setup

### Prerequisites

- Python 3.8+ installed
- pip package manager

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/Preveen369/LinguaSphere-App.git
   cd LinguaSphere-App
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys**

   - Add your API keys (if required) to `config.py`.
   - Note: Google Translate and gTTS may not require API keys, but MyMemory API might need one for higher usage.

4. **Run the app**

   ```bash
   streamlit run app.py
   ```

🌐 Access your app locally at: `http://localhost:8501`

---

## 🤝 Contributing

Pull requests are welcome! Feel free to fork the repository and suggest improvements.

Steps to contribute:

```bash
# 1. Fork the repository
# 2. Create a feature branch
git checkout -b feature-name

# 3. Commit your changes
git commit -m "Add feature description"

# 4. Push to GitHub
git push origin feature-name

# 5. Open a Pull Request
```

---

## 📧 Contact

For queries or suggestions:

- 📩 Email: spreveen123@gmail.com
- 🌐 LinkedIn: www.linkedin.com/in/preveen-s-17250529b/

---

## 🌟 Show Your Support

If you like this project, please consider giving it a ⭐ on GitHub!
