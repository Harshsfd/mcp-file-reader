# ui/app.py
import streamlit as st
from client.client import list_files, ask_ai_about_file

st.set_page_config(page_title="MCP File Reader", layout="wide")
st.title("🤖 MCP File Reader Chatbot")

# List files from server
files = list_files()
if not files:
    st.warning("Koi files nahi mili. 'files/' folder check karo!")
else:
    selected_file = st.selectbox("File choose karo:", files)

    question = st.text_input("AI ko kya puchna hai? (e.g., summary banao)")

    if st.button("Submit"):
        if selected_file and question:
            with st.spinner("AI se response aa raha hai..."):
                answer = ask_ai_about_file(selected_file, question)
            st.subheader("AI Answer:")
            st.write(answer)
            
