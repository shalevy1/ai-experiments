# ai-experiments
AI Experiments   A public repository of AI/ML projects exploring generative models, NLP, computer vision, and autonomous agents. Includes code, documentation, and demos for educational purposes. 

# Chat with SQL

A Streamlit app that uses LangChain and Groq LLM to answer questions about a SQL database.

## Setup
1. Install dependencies:  
   pip install -r requirements.txt

2. Create a .env file with your credentials:
    DB_URI=mysql+pymysql://username:password@localhost/dbname
    GROQ_API_KEY=your_groq_api_key_here

3. Run the app:
    streamlit run sqlchatbot..py
