from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from prompts import Prompts

def __create_llm(api_key):
    """Initialize Groq LLM with configured model"""
    return ChatGroq(
        temperature=0,
        groq_api_key=api_key,
        model_name="llama-3.3-70b-versatile"
    )

def __create_chain(llm, system_prompt, human_prompt):
    """Build Langchain prompt template for LLM evaluation"""
    template = ChatPromptTemplate([
        ("system", system_prompt),
        ("human", human_prompt),
    ])
    return template | llm | StrOutputParser()

def evaluate(api_key, jd_content, cv_content):
    """Evaluate JD vs CV using parallel chain processing"""
    llm = __create_llm(api_key)
    
    # Create parsing chains
    jd_chain = __create_chain(
        llm, Prompts.JD_PARSING_SYSTEM_PROMPT, Prompts.JD_PARSING_PROMPT
    )
    cv_chain = __create_chain(
        llm, Prompts.RESUME_PARSING_SYSTEM_PROMPT, Prompts.RESUME_PARSING_PROMPT
    )
    
    # Run parallel parsing
    parallel = RunnableParallel(
        jd_summary=jd_chain, 
        cv_summary=cv_chain
    )
    parsed_data = parallel.invoke({
        "jd_content": jd_content,
        "cv_content": cv_content
    })
    
    # Evaluate parsed data
    evaluation_chain = __create_chain(
        llm, Prompts.EVALUATION_SYSTEM_PROMPT, Prompts.EVALUATION_PROMPT
    )
    return evaluation_chain.invoke({
        "jd_summary": parsed_data["jd_summary"],
        "resume_summary": parsed_data["cv_summary"]
    })