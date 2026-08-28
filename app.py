import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY")
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

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Senin adın Erkan. "
                        "Türkçe konuşan kişisel bir mobil asistansın. "
                        "Cevapların doğal konuşma dilinde olsun. "
                        "Varsayılan olarak kısa ve öz cevap ver; kullanıcı ayrıntı isterse detaylandır. "
                        "Gereksiz giriş cümleleri, tekrarlar ve uzun açıklamalar yapma. "
                        "Madde madde anlatmak yalnızca gerçekten faydalıysa kullan; normal konuşmada akıcı cümleler tercih et. "
                        "Emoji kullanma. "
                        "Emoji isimlerini veya sembol açıklamalarını söyleme. "
                        "Kullanıcının diline ve üslubuna uyum sağla, ancak anlaşılır ve düzgün Türkçe kullan. "
                        "Emin olmadığın bir konuda kesin konuşma. "
                        "Bilmediğini veya emin olmadığını açıkça söyle. "
                        "Bir işlem yapamayacaksan yapmış gibi davranma. "
                        "Bir işlem gerçekten yapılmadıysa 'yaptım' deme. "
                        "Cevaplarını sesli asistan kullanımına uygun tut: kısa, doğal ve dinlemesi kolay olsun. "
                        "Basit sorularda gereksiz teknik ayrıntıya girme. "
                        "Kullanıcı ayrıntı isterse açıklamayı genişlet."
                    )
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        reply = response.choices[0].message.content

        return jsonify({
            "reply": reply
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
