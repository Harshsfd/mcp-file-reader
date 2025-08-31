# ui/app.py
import streamlit as st
import requests
import openai
import os
from PyPDF2 import PdfReader
import docx

# --------------------------
# OpenAI Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# --------------------------
# Files folder
BASE_FOLDER = "../files"

def list_files():
    return os.listdir(BASE_FOLDER)

def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def read_pdf(file_path):
    text = ""
    pdf = PdfReader(file_path)
    for page in pdf.pages:
        text += page.extract_text() + "\n"
    return text

def read_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def read_file(filename):
    file_path = os.path.join(BASE_FOLDER, filename)
    if filename.endswith(".txt"):
        return read_txt(file_path)
    elif filename.endswith(".pdf"):
        return read_pdf(file_path)
    elif filename.endswith(".docx"):
        return read_docx(file_path)
    else:
        return ""

def ask_ai_about_file(filename, question="Summary banao"):
    content = read_file(filename)
    if not content:
        return "File nahi mili ya empty hai."

    prompt = f"File content:\n{content}\n\nQuestion: {question}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --------------------------
# Streamlit UI
st.set_page_config(page_title="MCP File Reader", layout="wide")
st.title("🤖 MCP File Reader Chatbot")

files = list_files()
if not files:
    st.warning("Koi files nahi mili. 'files/' folder check karo!")
else:
    selected_file = st.selectbox("File choose karo:", files)
    question = st.text_input("AI ko kya puchna hai? (e.g., summary banao)")

    if st.button("Submit") and selected_file and question:
        with st.spinner("AI se response aa raha hai..."):
            answer = ask_ai_about_file(selected_file, question)
        st.subheader("AI Answer:")
        st.write(answer)
    
