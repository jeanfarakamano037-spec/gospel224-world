from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1 style='text-align:center;padding:50px'>GOSPEL224 WORLD EST EN LIGNE! 🎤<br><br>AIMEZ PRECHER JESUS - Jean Farakamano<br><br>Site deploye avec succes!</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
