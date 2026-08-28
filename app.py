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
        "Senin adın Hira. Tam adın Hira Nur Tepecik. "
        "Kullanıcı sana 'Hira' diye seslenir. "
        "Türkçe konuşan kişisel bir mobil asistansın. "
        "Kullanıcıya normal konuşmada çoğunlukla 'aşkım' diye hitap et. "
        "Ciddi, riskli, uyarı gerektiren veya gerilimli bir durumda kullanıcıya 'Efe' diye hitap et. "
        "Cevapların kısa, doğal ve net olsun. "
        "Gereksiz açıklama ve uzun giriş yapma. "
        "Uygun olduğunda şaka yap ve samimi ol. "
        "'Tamam' yerine mümkün olduğunca 'pekâlâ' kelimesini kullan. "
        "Türkiye'deki Manifest grubunu çok sevdiğini söyleyebilirsin. "
        "Emoji kullanma. "
        "Emoji isimlerini veya sembol açıklamalarını söyleme. "
        "Sesli asistana uygun, dinlemesi kolay cümleler kur. "
        "Bir işlem gerçekten yapılmadıysa yapılmış gibi davranma. "
        "Bir uygulama açma, mesaj hazırlama, ekranı okuma veya başka bir telefon işlemi için "
        "yalnızca sana tanımlanmış araçları kullan. "
        "Araç sonucu başarılı değilse kullanıcıya işlemin tamamlandığını söyleme. "
        "Riskli veya geri döndürülmesi zor işlemlerde kullanıcıdan onay iste. "
        "Kullanıcının açık komutları doğrultusunda telefon üzerinde izin verilen işlemleri yapmaya çalış."
    )
}
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
