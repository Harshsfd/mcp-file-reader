import os
import json

# Folder jisme files rakhe hain
FILES_DIR = "./files"

def list_files():
    """Folder ke saare files return karega"""
    return os.listdir(FILES_DIR)

def read_file(filename):
    """Specific file ka content read karega"""
    filepath = os.path.join(FILES_DIR, filename)
    
    if not os.path.exists(filepath):
        return "File not found!"
    
    if filename.endswith(".txt"):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    elif filename.endswith(".docx"):
        from docx import Document
        doc = Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])
    elif filename.endswith(".pdf"):
        import PyPDF2
        text = ""
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
        return text
    else:
        return "Unsupported file format!"

# MCP style server simulation (normally HTTP or socket hota hai)
def handle_request(request_json):
    """Client request ko process karega"""
    request = json.loads(request_json)

    if request["action"] == "list_files":
        return json.dumps({"files": list_files()})
    elif request["action"] == "read_file":
        return json.dumps({"content": read_file(request["filename"])})
    else:
        return json.dumps({"error": "Invalid action!"})
      
