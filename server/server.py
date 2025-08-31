# server/server.py
from flask import Flask, request, jsonify
import os
from PyPDF2 import PdfReader
import docx

app = Flask(__name__)
BASE_FOLDER = os.path.join(os.path.dirname(__file__), "../files")  # files folder

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
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

@app.route("/list-files", methods=["GET"])
def list_files():
    files = os.listdir(BASE_FOLDER)
    return jsonify({"files": files})

@app.route("/read-file", methods=["POST"])
def read_file():
    data = request.json
    filename = data.get("filename")
    file_path = os.path.join(BASE_FOLDER, filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    try:
        if filename.endswith(".txt"):
            content = read_txt(file_path)
        elif filename.endswith(".pdf"):
            content = read_pdf(file_path)
        elif filename.endswith(".docx"):
            content = read_docx(file_path)
        else:
            return jsonify({"error": "Unsupported file type"}), 400

        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5001, debug=True)
  
