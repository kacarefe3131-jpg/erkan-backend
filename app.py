from flask import Flask

app = Flask(__name__)

@app.get("/")
def home():
    return "Erkan backend çalışıyor."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
