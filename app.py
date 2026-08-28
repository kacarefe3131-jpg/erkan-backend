import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

@app.get("/")
def home():
    return "Erkan backend çalışıyor."

@app.post("/chat")
def chat():
    try:
        data = request.get_json(silent=True) or {}
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"error": "Mesaj boş olamaz."}), 400

        response = client.responses.create(
            model="gpt-5.6-luna",
            input=[
                {
                    "role": "system",
                    "content": (
                        "Senin adın Erkan. "
                        "Türkçe konuşan kişisel bir mobil asistansın. "
                        "Doğal, kısa ve anlaşılır cevaplar ver."
                    )
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        return jsonify({
            "reply": response.output_text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
