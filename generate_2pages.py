#!/usr/bin/env python3
import os, json, requests
from datetime import datetime

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")

MODEL = "gpt-4o"   # можно сменить на любую вашу модель

prompt = """Напиши связный текст длиной примерно 2 страницы (800–1000 слов).
Тема может быть любой, но избегай оскорблений, политики и откровенного контента.
Сделай заголовок и несколько абзацев."""

payload = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": "Ты — генератор креативных текстов."},
        {"role": "user", "content": prompt}
    ],
    "max_tokens": 2500,
    "temperature": 0.8,
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

resp = requests.post(
    "https://api.openai.com/v1/chat/completions",
    json=payload,
    headers=headers,
    timeout=60
)
data = resp.json()
content = data["choices"][0]["message"]["content"]

# сохраняем
ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
fname = f"two_pages_{ts}.txt"

with open(fname, "w", encoding="utf-8") as f:
    f.write(f"# Generated at {ts} UTC\n\n{content}")

print("Saved:", fname)
