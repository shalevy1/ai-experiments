# 🚀 AI Experiments Suite

[![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)](https://www.python.org/) [![Streamlit](https://img.shields.io/badge/Streamlit-1.25.0-orange.svg)](https://streamlit.io/) [![GitHub Issues](https://img.shields.io/github/issues/your-username/ai-experiments)](https://github.com/your-username/ai-experiments/issues)

A collection of AI/ML projects exploring generative models, NLP, and database interactions. Includes Streamlit apps for real-world use cases.

---

## Table of Contents

- [SQL Chat App](#sql-chat-app)
- [AI Resume & JD Analyzer](#ai-resume-jd-analyzer)


---

## SQL Chat App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-resume-jd-analyzer.streamlit.app/)

### Overview
A Streamlit application that allows users to ask questions about SQL databases using natural language. Leverages Groq LLM for query generation and LangChain for database interaction.

### Key Features
- Real-time SQL query generation
- Schema-aware responses
- Error handling for database interactions
- Context-aware conversations

### Tech Stack
- Python | Streamlit | LangChain | Groq LLM | MySQL

### Setup
**Install dependencies:**
 ```sh
 pip install -r requirements.txt
 ```
**Create .env file:**
env
 ```sh
DB_URI=mysql+pymysql://username:password@localhost/dbname
GROQ_API_KEY=your_groq_api_key_here
 ```
**Run the app:**
 ```sh
streamlit run sqlchatbot.py
 ```

## AI Resume & JD Analyzer

Automatically evaluate candidate fit for job roles using Groq LLM and Streamlit. Generates match scores, personalized improvement suggestions, and ATS-compliant CV rewrites.

---

### **Demo**
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-resume-jd-analyzer.streamlit.app/)

---

### Key Features
- **Score-Based Recommendations**:
  - Score ≥**8**: CV is aligned; no changes needed.
  - **5 ≤ Score <8**: Receive improvement suggestions and CV rewrite.
  - Score <**5**: Redirected to refine or find a better-fitting role.
- **Real-Time Analysis**: Instant feedback on CV-JD alignment.
- **ATS-Compliant CV Rewrite**: Structured for applicant tracking systems.
- **Loading Spinners**: Visual feedback during LLM processing.
- **Dynamic UI**: Tailored experiences based on evaluation scores.

---

### Tech Stack
- Python | Streamlit | LangChain | Groq LLM | PyMuPDF

---

### Setup

```sh
git clone https://github.com/your-username/ai-resume-jd-analyzer
cd ai-resume-jd-analyzer
```
**Install dependencies:**
```sh
 pip install -r requirements.txt
 ```
**Run the app:**
```sh
streamlit run app.py
```

### Usage
- **Upload Files:** Drag-and-drop PDFs for the job description and CV.
- **Select Mode:** Choose between Hiring or Candidate Mode.
- **Evaluate Fit:** Click "Evaluate Fit" to generate a report.
- **Improve CV:** Review suggestions and generate an updated CV (Score ≥5).

### License
This project is licensed under the Apache License.

### Acknowledgments
https://streamlit.io
https://groq.com
https://langchain.com
https://pymupdf.readthedocs.io



