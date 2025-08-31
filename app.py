from flask import Flask, request, jsonify
from server import file_server
import json
import openai

app = Flask(__name__)

openai.api_key = "YOUR_OPENAI_KEY"

@app.route("/list_files", methods=["GET"])
def list_files():
    response = file_server.handle_request(json.dumps({"action": "list_files"}))
    return jsonify(json.loads(response))

@app.route("/read_file", methods=["GET"])
def read_file():
    filename = request.args.get("name")
    response = file_server.handle_request(json.dumps({"action": "read_file", "filename": filename}))
    return jsonify(json.loads(response))

@app.route("/ask_ai", methods=["POST"])
def ask_ai():
    data = request.json
    prompt = data.get("prompt", "")
    context = data.get("context", "")
    
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant with file access."},
            {"role": "user", "content": f"File Content: {context}\n\nQuestion: {prompt}"}
        ]
    )
    return jsonify({"answer": res["choices"][0]["message"]["content"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
