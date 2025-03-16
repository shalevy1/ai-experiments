import streamlit as st
from conversation import ConversationAgent
from shopping_team import ShoppingTeam
from image_processing import ProductImageProcesingAgent
from PIL import Image as PILImage
import asyncio


async def get_gemini_response(imageData,api_key):
        p = ProductImageProcesingAgent(api_key=api_key)
        resp =  p.process_image(image_data=imageData)
        return resp.content
        


st.set_page_config(
    page_title="E-commerce Shopping Assistant", 
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Report a bug": "https://github.com/vivekpathania/ai-experiments/issues"
    }
)

# Title and Header
st.title("🛒 AI-Powered Shopping Assistant")
st.write("Chat with our AI assistant to find the best products and compare them effortlessly.")

if "are_keys_avaibale" not in st.session_state:
    st.session_state["are_keys_avaibale"] = False 
        
image_container = st.container()

with st.sidebar:
    st.header("🔧 Configuration")
    llm_mode = st.radio("Select Model Provider", ["Groq", "OpenAI"], horizontal = True)
    
    api_key_llm = st.text_input(
        "Groq or OpenAI API Key - [Groq](https://console.groq.com/keys) | [OpenAI](https://console.groq.com/keys)", key="api_key_llm", type="password"
    )
   
   
    st.divider()
    web_search_mode = st.radio("Search & Scraping Tools", ["Tavily", "SerpApi"], horizontal = True)
    
    api_key_search_tool = st.text_input(
        "Travily Or SerpApi Key - [Tavily](https://app.tavily.com) | [SerpApi](https://serpapi.com/)", key="api_key_search_tool", type="password"
        
    )
   
    api_key_firecrawl = st.text_input(
        "Firecrawl API Key - [Firecrawl](https://www.firecrawl.dev/)", key="api_key_firecrawl", type="password",value=""
        
    )
    
    api_key_gemini = st.text_input(
        "Gemini API Key - [Gemini](https://aistudio.google.com/)", key="api_key_gemini", type="password",value=""
        
    )
    
   
    
    if st.button("Set keys"):
        
       
        st.session_state["conversation_agent"] = ConversationAgent(api_key=api_key_llm,llm_mode=llm_mode) 
        st.session_state["shopping_team"] = ShoppingTeam(api_key_llm=api_key_llm,api_key_search_tool=api_key_search_tool,search_tool=web_search_mode,llm_mode=llm_mode,firecrawl_api_key=api_key_firecrawl)
        st.session_state["gemini_key"] = api_key_gemini
        
        
            
        st.session_state["are_keys_avaibale"] = True
        
    if not st.session_state["are_keys_avaibale"]:
        st.warning("Please enter keys to get started.")
    else:
        st.success("API keys are avaibale.")
        
    st.divider()
     
    if st.button("Clear Conversation"):
        st.session_state.messages.clear() 
        if "conversation_agent" in st.session_state:
            st.session_state["conversation_agent"].reset()
        
      
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
user_query = st.chat_input("Ask anything about your shopping needs",accept_file=True,file_type=["jpg", "jpeg", "png"])

if user_query:
    # Append user message
    if len(user_query["files"]) > 0:
        f = user_query["files"][0]
       
        
        st.image(
            f,
            width = 200,
            use_container_width=False
        )
        bytes_data = f.getvalue()
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            user_query = loop.run_until_complete(get_gemini_response(bytes_data,st.session_state["gemini_key"]))
            
            
        except Exception as e:
            st.error(f"Analysis error: {e}")

    if st.session_state["are_keys_avaibale"]:
        
    
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)
        
        response =  st.session_state['conversation_agent'].process_query(user_query)
        
        # Append assistant response
        if response['have_further_conversation']:
            st.session_state.messages.append({"role": "assistant", "content": response["message"]})
            with st.chat_message("assistant"):
                st.markdown(response["message"])
        else:
            with st.chat_message("assistant"):
                st.markdown(response["message"])
        
            with st.spinner("Fetching product recommendations..."):
                shopping_result = st.session_state["shopping_team"].run(response['data'])
            with st.chat_message("assistant"):
                st.html(shopping_result.content)
               
    else:
        st.toast('Please enter both keys to get started.', icon='⚠️')
        
  

        

    
    
            

                



                    

