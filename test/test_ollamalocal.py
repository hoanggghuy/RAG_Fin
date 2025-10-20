import requests
import json

def call_ollama(prompt, model="gemma3:1b"):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False  # Để nhận full kết quả một lần (không streaming)
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        data = response.json()
        return data.get("response")
    else:
        print("Error:", response.status_code, response.text)
        return None

if __name__ == "__main__":
    answer = call_ollama("Xin chào, bạn là AI gì?", model="gemma3:1b")
    print("Kết quả từ Ollama:")
    print(answer)
