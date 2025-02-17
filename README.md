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
1. Install dependencies:
 ```sh
 pip install -r requirements.txt
 ```
Create .env file:
env
 ```sh
DB_URI=mysql+pymysql://username:password@localhost/dbname
GROQ_API_KEY=your_groq_api_key_here
 ```
Run the app:
 ```sh
streamlit run sqlchatbot.py
 ```

## AI Resume & JD Analyzer
https://ai-resume-jd-analyzer.streamlit.app/

### Overview
    Automatically evaluate candidate fit for job roles using Groq LLM and Streamlit. Generates match scores and detailed reports.
### Key Features
    LLM-powered resume/JD parsing
    Automated scoring system
    Penalty rules for overqualification
    Real-time analysis
    Deployable on Streamlit Cloud

### Tech Stack
    Python | Streamlit | LangChain | Groq LLM | PyMuPDF

### Setup
    
Install dependencies:
 ```sh
pip install -r requirements.txt
 ```

Create .env file:
 ```sh
GROQ_API_KEY=your_groq_api_key_here
 ```

Run the app:
 ```sh
streamlit run app.py
 ```
### General Setup Instructions

Prerequisites
Python 3.9+
Streamlit
Groq API Key (https://console.groq.com/keys)

### Environment Setup

Create virtual environment
 ```sh
python -m venv .venv
source .venv/bin/activate
 ```

Install dependencies
 ```sh
pip install -r requirements.txt
 ```

### License
This project is licensed under the MIT License.

### Acknowledgments
Streamlit - For the amazing UI framework
Groq - For powerful LLM capabilities
LangChain - For LLM integration tools
PyMuPDF - For PDF text extraction




