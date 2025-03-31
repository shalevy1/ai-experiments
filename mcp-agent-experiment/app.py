import streamlit as st
from agent import run_agent
import asyncio

st.set_page_config(
    page_title="MCP SQL Chatbot",  
    page_icon="🧊",  
    layout="wide",
    initial_sidebar_state="expanded",  
    menu_items={
        "Report a bug": "https://github.com/vivekpathania/ai-experiments/issues"
    }
)

# Title and Header
st.title("🧊 MCP SQL Chatbot")  # Updated title
st.write(
    "Interact with an SQL database using natural language. "
    "This app connects to an MCP SQL server to execute your queries and provide results."
)  # Updated description

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown(
        "This application allows you to interact with an SQL database using natural language. "
        "It leverages the MCP (Modular Control Protocol) to connect to an SQL server, "
        "execute your queries, and present the results in a user-friendly format."
    )
    st.markdown(
        "**How to use:**\n"
        "1. Ensure the MCP SQL server is running.\n"
        "2. Ask your questions in the chat box below.\n"
        "3. The app will generate and execute the appropriate SQL query.\n"
        "4. The results will be displayed in the chat."
    )
    st.markdown("👨‍💻 Developed as an AI experiment. Contribute on [GitHub](https://github.com/vivekpathania/ai-experiments)")

# Main App Logic
# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_state" not in st.session_state:
    st.session_state.conversation_state = {}

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_query = st.chat_input("Ask a question about the database (e.g., 'List all employees')")  

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.spinner("Fetching response from the database..."):  
        try:
            resp = asyncio.run(run_agent(user_query))
            
            
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
            resp = None

    if resp:
        with st.chat_message("assistant"):
            st.markdown(resp.content)
