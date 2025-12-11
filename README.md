# URL & YouTube Summarizer (LangChain + Groq + Streamlit)

A Streamlit application that summarizes content from **any website URL or YouTube video** using  
**LangChain**, **Groq Llama models**, and **Map–Reduce summarization**.

This tool loads webpage text or YouTube transcripts, cleans the text, splits it into chunks, summarizes each chunk, and combines everything into one meaningful final summary.

---

## 🚀 Features

### 🔹 **Summarization Techniques Included**
This project uses **Map–Reduce Summarization**, which includes:

- **Map Step:** Each chunk of text is summarized individually  
- **Reduce Step:** All chunk summaries are merged into one final summary  
- Handles **long webpages** and **long YouTube transcripts**

### 🔹 What the app can do:
- Summarize **YouTube videos** via transcript loading  
- Summarize **any website URL**  
- Remove emojis and non-ASCII text  
- Split long documents using `RecursiveCharacterTextSplitter`  
- Perform LLM summarization using **Groq's Llama-3 models**  
- Simple, clean, fast UI using Streamlit  

---

## 📁 Project Structure

project-folder/
│
├── app.py # Main Streamlit application
├── requirements.txt # Dependencies
├── .env.example # Example environment file
├── .gitignore
└── README.md

yaml
Copy code

---

## 🔧 Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Shehjad2019/web-youtube-summarizer-llm.git
cd web-youtube-summarizer-llm
2️⃣ Create Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows
3️⃣ Install Requirements
bash
Copy code
pip install -r requirements.txt
4️⃣ Add Groq API Key
Copy .env.example → .env:

bash
Copy code
cp .env.example .env
Edit .env:

ini
Copy code
GROQ_API_KEY=your_groq_api_key_here
▶️ Running the App
Run Streamlit:

bash
Copy code
streamlit run app.py
The application will open in your browser.

Paste any:

YouTube URL

Website URL

Then click Summarize Content.

🧠 How It Works
Detects YouTube or website

Loads data using:

YoutubeLoader for YouTube

UnstructuredURLLoader for normal webpages

Removes emojis & non-ASCII text

Splits text into smaller chunks

Runs map summarization on each chunk

Combines chunk summaries using reduce prompt

Outputs a clean, concise final summary

🧰 Technologies Used
Python

Streamlit

LangChain

Groq ChatGroq Llama Models

YoutubeLoader & UnstructuredURLLoader

RecursiveCharacterTextSplitter

🔑 Environment Variables
ini
Copy code
GROQ_API_KEY=your_groq_key_here
👤 Author
Shehjad Patel
GitHub: https://github.com/Shehjad2019