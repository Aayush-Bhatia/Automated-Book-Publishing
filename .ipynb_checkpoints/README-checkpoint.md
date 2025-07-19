# 📚 Automated Book Publishing System

An end-to-end AI-powered pipeline that scrapes book content from a given URL, generates multiple "spun" versions using LLMs, performs AI-based reviewing, allows human editing, and scores the final output using a basic reinforcement learning reward model.

---

## 🌐 Live URL Used
> `https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1`

---

## 🛠️ Features

- ✅ Web scraping with screenshots using **Playwright**
- ✍️ AI writing (LLM-based chapter spinning using Groq/Gemini)
- 🧠 AI-based reviewer agent for refining the spun content
- 👤 Human-in-the-loop editing with versioning
- 📊 RL-inspired reward scoring to rate human edits
- 📁 Final book merge with version support
- 🔎 ChromaDB-based semantic search engine (optional)
- 🎙️ Voice-based query handling (optional integration)
- 📄 PDF generation support (if enabled)

---

## 🧰 Tech Stack

| Tool | Use |
|------|-----|
| Python | Core development |
| Playwright | Web scraping & screenshots |
| Groq / Gemini | LLMs for text generation |
| ChromaDB | Version storage & retrieval |
| Streamlit | Optional GUI |
| FPDF | PDF generation |
| SpeechRecognition, PyAudio | Voice support |
| dotenv | API key management |
| RL-style scoring | Reward-based feedback loop |

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/Aayush-Bhatia/Automated-Book-Publishing.git
cd Automated-Book-Publishing

# Create virtual environment (optional)
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install all required packages
pip install -r requirements.txt
