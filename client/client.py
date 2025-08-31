# client/client.py
import requests
import openai

MCP_SERVER = "http://127.0.0.1:5001"  # MCP server URL

openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your OpenAI API key

def list_files():
    res = requests.get(f"{MCP_SERVER}/list-files")
    return res.json().get("files", [])

def read_file(filename):
    res = requests.post(f"{MCP_SERVER}/read-file", json={"filename": filename})
    if "error" in res.json():
        return None
    return res.json().get("content", "")

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

# Example usage
if __name__ == "__main__":
    print("Available files:", list_files())
    filename = input("Kaunsi file padhna hai? ")
    answer = ask_ai_about_file(filename, "Iska short summary do")
    print("\nAI Answer:\n", answer)
  
