import streamlit as st
import os
import docx
import PyPDF2

st.set_page_config(page_title="📂 MCP File Reader", layout="wide")

st.title("📂 MCP File Reader")
st.write("Upload your files (TXT, PDF, DOCX) and read them easily!")

uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx"])

if uploaded_file:
    file_extension = uploaded_file.name.split(".")[-1].lower()
    
    content = ""

    if file_extension == "txt":
        content = uploaded_file.read().decode("utf-8")

    elif file_extension == "pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        content = ""
        for page in reader.pages:
            content += page.extract_text() + "\n"

    elif file_extension == "docx":
        doc = docx.Document(uploaded_file)
        content = "\n".join([para.text for para in doc.paragraphs])

    st.subheader("📖 File Content")
    st.text_area("Content", content, height=400)

    # Optional: Save file in server
    save_path = os.path.join("files", uploaded_file.name)
    os.makedirs("files", exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ File saved at {save_path}")
