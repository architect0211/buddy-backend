# sovereign_llm.py
# Sovereign Fallback Interface to Local LLaMA3 via Ollama

import requests

def call_llama(prompt, model="llama3", stream=False):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream,
        "temperature": 0.5,
        "num_predict": 600
    }

    try:
        response = requests.post(url, json=payload, timeout=20)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "[⚠️ No response from local model]")
    except requests.exceptions.RequestException as e:
        return f"[⚠️ Local LLaMA call failed: {str(e)}]"
