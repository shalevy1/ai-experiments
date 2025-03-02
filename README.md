# 🚀 AI Experiments Suite

[![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)](https://www.python.org/) [![Streamlit](https://img.shields.io/badge/Streamlit-1.25.0-orange.svg)](https://streamlit.io/) [![GitHub Issues](https://img.shields.io/github/issues/vivekpathania/ai-experiments)](https://github.com/vivekpathania/ai-experiments/issues)

A collection of AI/ML projects exploring generative models, NLP, and database interactions. Includes Streamlit apps for real-world use cases.

---

## Table of Contents

- [SQL Chat App](#sql-chat-app)
- [AI Resume & JD Analyzer](#ai-resume-jd-analyzer)
- [AI Travel Planner](#ai-travel-planner)



---

## SQL Chat App

A Streamlit application that allows users to ask questions about SQL databases using natural language. Leverages Groq LLM for query generation and LangChain for database interaction.

### Key Features
- Real-time SQL query generation
- Schema-aware responses
- Error handling for database interactions
- Context-aware conversations

### Tech Stack
- Python | Streamlit | LangChain | Groq LLM | MySQL

### Setup

```sh
git clone https://github.com/vivekpathania/ai-experiments
cd sqlchatbot
```

**Virtual Environment:**

 ```sh
 pip install virtualenv
 python3 -m venv env
 source env/bin/activate
 ```

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
git clone https://github.com/vivekpathania/ai-experiments
cd hrapp
```

**Virtual Environment:**

 ```sh
 pip install virtualenv
 python3 -m venv env
 source env/bin/activate
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
- [Streamlit](https://streamlit.io)
- [GROQ](https://groq.com)
- [LangChain](https://langchain.com)
- [PyMuPDF](https://pymupdf.readthedocs.io)



## AI Travel Planner

### **Demo**
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://conversational-travel-planner.streamlit.app/)

### Overview
A conversational travel planning application that generates customized itineraries using AI. Supports both business and leisure trips with tailored recommendations.

### Key Features
- **Conversational Interface**: Natural language interaction to gather trip details
- **Real-Time Data Integration**: Uses Tavily/SerpApi to fetch up-to-date travel information
- **Customized Itineraries**: Generates Markdown-formatted itineraries with flight options, hotel recommendations, and daily schedules
- **Multi-Tool Support**: Integrates Groq LLM, Tavily, and SerpApi for comprehensive data processing
- **Visual Formatting**: Uses emojis, tables, and bullet points for clear presentation

### Tech Stack
- Python | Streamlit | Agno | Groq LLM | Tavily/SerpApi

### Setup

```sh
git clone https://github.com/vivekpathania/ai-experiments
cd travel-agent
```

**Virtual Environment:**

 ```sh
 pip install virtualenv
 python3 -m venv env
 source env/bin/activate
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
1. **Enter API Keys**: Provide Groq and Tavily/SerpApi keys in the sidebar
2. **Describe Your Trip**: Use natural language to specify trip details (e.g., "Family holiday from London to Paris for 4 days")
3. **Generate Itinerary**: The AI will create a detailed itinerary with options for flights, hotels, and activities

### Example Input
```sh
Business trip from New York to Tokyo from 2024-05-10 to 2024-05-15 for 1 traveler. Budget: $3000. Needs conference venues and after-work dining options.
```

### Example Output
```markdown
# **Tokyo Business Trip Itinerary**

## Trip Summary
- **Type:** Business
- **Dates:** May 10 - May 15, 2024
- **Travelers:** 1
- **Budget:** $3,000

## Flight Options
| Airline          | Price (Adult) | Details                  |
|------------------|---------------|--------------------------|
| JAL              | $1,200        | Non-stop, 8 AM departure |
| ANA              | $1,150        | 1 layover in Seoul       |

## Accommodation
| Hotel                | Price/Night | Amenities                |
|----------------------|-------------|--------------------------|
| Park Hyatt Tokyo     | $350        | Business center, WiFi    |
| Mandarin Oriental    | $290        | Fitness center, breakfast|

## Daily Schedule
- **May 10**: Business meeting at Conference Center X (10 AM)
- **May 11**: Networking dinner at Robata-tei (7 PM)

## Important Tips
- **Transportation**: Use the Tokyo Metro for easy access to business districts.
- **Culture**: Familiarize yourself with Japanese business etiquette.
```

### License
This project is licensed under the MIT License.

### Acknowledgments
- [Streamlit](https://streamlit.io)
- [Groq](https://groq.com)
- [Tavily](https://tavily.com)
- [SerpApi](https://serpapi.com)








