import json
import openai
from server import file_server

openai.api_key = "YOUR_OPENAI_KEY"

def ask_ai(prompt, context=""):
    """LLM se response lena"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant with file access."},
            {"role": "user", "content": f"File Content: {context}\n\nQuestion: {prompt}"}
        ]
    )
    return response["choices"][0]["message"]["content"]

def main():
    print("🤖 AI File Reader (type 'exit' to quit)")
    while True:
        query = input("You: ")

        if query.lower() == "exit":
            break

        if "list files" in query:
            response = file_server.handle_request(json.dumps({"action": "list_files"}))
            print("AI:", response)

        elif "read" in query:
            filename = query.replace("read", "").strip()
            response = file_server.handle_request(json.dumps({"action": "read_file", "filename": filename}))
            data = json.loads(response)
            if "content" in data:
                answer = ask_ai("Summarize this file", context=data["content"])
                print("AI:", answer)
            else:
                print("AI:", data["error"])
        else:
            print("AI: Please say 'list files' or 'read <filename>'")

if __name__ == "__main__":
    main()
  
