
# 📜 Streamlit YouTube & Website Summarizer

This project is a **Streamlit application** that allows you to summarize text content from **YouTube videos** (via transcripts) or **website URLs** into a concise 300-word summary using **Groq LLMs**.  
It uses `langchain`, `streamlit`, and Groq’s `ChatGroq` model (`gemma2-9b-it`) to process and summarize the text.

---

## 🚀 Features
- Summarize content from **YouTube videos** (with transcript support).
- Summarize content from **any website URL**.
- Uses **LangChain summarization chains** with Groq LLMs.
- Handles long documents with **token-based trimming** (max 3000 tokens).
- Simple and interactive **Streamlit UI**.

---

## 📂 Project Structure
```
.
├── app.py              # Main Streamlit app
├── requirements.txt    # Dependencies
└── README.txt          # Documentation
```

---

## 🛠️ Requirements

Create a `requirements.txt` file with the following dependencies:

```
streamlit
langchain
langchain-community
langchain-groq
validators
youtube-transcript-api
pytube
unstructured
requests
```

---

## ⚙️ Installation & Setup

1. **Clone the repository** (or download the script files):
   ```bash
   git clone <your-repo-link>
   cd <your-repo-folder>
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate    # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

---

## 🔑 API Key Setup
This app requires a **Groq API key**.

- Get your API key from [Groq](https://groq.com/).
- Enter it into the **sidebar input box** in the app.

---

## 📖 How to Use
1. Launch the app using:
   ```bash
   streamlit run app.py
   ```
2. Enter your **Groq API key** in the sidebar.
3. Paste a **YouTube video link** or a **website URL** in the input field.
4. Click **"Summarize the Content"**.
5. The app will:
   - Extract transcript/text from the source.
   - Trim the text to **3000 tokens**.
   - Summarize the content into **~300 words** using the `gemma2-9b-it` model.
6. The final summary will be displayed on the screen.

---

## 🧩 Explanation of the Code
- **`YoutubeLoader` / `UnstructuredURLLoader`** → Extract text from YouTube or website.
- **Token Trimming** → Uses `TokenTextSplitter` to avoid exceeding token limits.
- **PromptTemplate** → Defines the summarization prompt (`300 words summary`).
- **Groq LLM (`ChatGroq`)** → Runs the summarization with the Gemma model.
- **Streamlit UI** → Provides inputs for API key and URL, with results shown interactively.

---

## 📝 Example
- Input: YouTube link → `https://www.youtube.com/watch?v=JcVHf4X_dqY`
- Output: A clean, ~300 word summary of the video transcript.

---

## ⚠️ Notes
- Some YouTube videos may not have transcripts → summaries won’t work in those cases.
- If the content is too long, only the first **3000 tokens** are summarized.
- Make sure your API key is valid and has sufficient quota.

---

## 📌 Author
Developed as a learning project to combine **LangChain**, **Groq LLMs**, and **Streamlit** for real-world text summarization.

