from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "용병 백엔드 서버가 살아있습니다!"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
