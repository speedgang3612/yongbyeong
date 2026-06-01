import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# 화면(다른 포트)에서 이 API를 호출할 수 있게 허용 (CORS)
CORS(app)

# DB 파일 이름 (이 파일 하나가 곧 데이터베이스다. 서버를 껐다 켜도 데이터가 남는다.)
DB = "users.db"


def init_db():
    """서버 시작 시 users 테이블이 없으면 만든다."""
    con = sqlite3.connect(DB)
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_type TEXT NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            phone TEXT,
            regions TEXT,
            extra TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    con.commit()
    con.close()


@app.route("/")
def home():
    return "용병 백엔드 서버가 살아있습니다!"


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    # 필수값 확인
    user_type = data.get("userType")
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    if not user_type or not name or not email or not password:
        return jsonify({"ok": False, "error": "필수 항목이 비어 있습니다."}), 400

    phone = data.get("phone", "")
    regions = data.get("regions", "")
    extra = data.get("extra", "")

    con = sqlite3.connect(DB)
    try:
        # ? 자리표시자로 값을 따로 전달 → SQL 인젝션 방지 (보안)
        con.execute(
            "INSERT INTO users (user_type, name, email, password, phone, regions, extra) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_type, name, email, password, phone, regions, extra),
        )
        con.commit()
    except sqlite3.IntegrityError:
        # 이메일 UNIQUE 위반 = 이미 가입된 이메일
        con.close()
        return jsonify({"ok": False, "error": "이미 가입된 이메일입니다."}), 409

    total = con.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    con.close()

    # 응답에는 비밀번호를 빼고 돌려준다 (보안)
    safe = {k: v for k, v in data.items() if k != "password"}
    return jsonify({"ok": True, "user": safe, "total": total})


@app.route("/api/users")
def list_users():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        "SELECT id, user_type, name, email, phone, regions, extra, created_at "
        "FROM users ORDER BY id DESC"
    ).fetchall()
    con.close()
    # 비밀번호는 애초에 SELECT에서 빼서 가져온다 (보안)
    safe_list = [dict(r) for r in rows]
    return jsonify({"total": len(safe_list), "users": safe_list})


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
