import pymupdf
import streamlit as st
from scripts import evaluate

st.set_page_config(
    page_title="AI Resume & JD Analyzer",
    page_icon="👩🏻‍💻",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Report a bug": "https://github.com/vivekpathania/ai-experiments/issues"
    }
)

st.title("AI Resume & JD Analyzer")
st.caption("Automatically match candidates to job roles.")

container = st.container(border=False)
with st.sidebar:
    groq_api_key = st.text_input(
        "Groq API Key", key="groq_api_key", type="password",
        help="Get your API key from [Groq Platform](https://console.groq.com/keys)"
    )
    "[Get your free Groq API key](https://console.groq.com/keys)"
    "[View the source code](https://github.com/vivekpathania/ai-experiments/blob/main/hrapp/app.py)"
    uploaded_jd_file = st.file_uploader("Upload Job Description (PDF)", key="jd")
    uploaded_cv_file = st.file_uploader("Upload Candidate CV (PDF)", key="cv")
    submitted = st.button("Evaluate Fit")

if submitted:
    if not groq_api_key:
        st.info("Please add your Groq API key to continue.")
        st.stop()
        
    if not uploaded_jd_file or not uploaded_cv_file:
        missing = []
        if not uploaded_jd_file: missing.append("JD")
        if not uploaded_cv_file: missing.append("CV")
        st.info(f"Please upload the {' and '.join(missing)}.")
        st.stop()

    try:
        # Extract JD Content
        with pymupdf.open(stream=uploaded_jd_file.read(), filetype="pdf") as pdf:
            jd_content = "\n\n".join(page.get_text("text") for page in pdf)

        # Extract CV Content
        with pymupdf.open(stream=uploaded_cv_file.read(), filetype="pdf") as pdf:
            cv_content = "\n\n".join(page.get_text("text") for page in pdf)

        result = evaluate(groq_api_key, jd_content, cv_content)
        container.write(result)

    except Exception as e:
        st.error(f"File processing error: {e}")
    
    
            
        

