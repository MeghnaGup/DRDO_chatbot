import requests

MISTRAL_API_KEY = "3Kid2WgrFVgojoiZd3n0iYUodfM93o8B"  # Replace with your real key
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

def get_mistral_response(prompt, model="mistral-tiny"):
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(MISTRAL_API_URL, headers=headers, json=data)
    # Return the answer text directly (string)
    return response.json()["choices"][0]["message"]["content"]