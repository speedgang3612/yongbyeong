from flask import Flask, request, jsonify

app = Flask(__name__)

# 임시 저장소(메모리) — 서버를 끄면 사라진다. 진짜 DB 저장은 다음 단계에서 붙인다.
users = []


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

    # 이메일 중복 확인
    if any(u.get("email") == email for u in users):
        return jsonify({"ok": False, "error": "이미 가입된 이메일입니다."}), 409

    # 저장 (받은 값 그대로 보관)
    users.append(dict(data))

    # 응답에는 비밀번호를 빼고 돌려준다 (보안)
    safe = {k: v for k, v in data.items() if k != "password"}
    return jsonify({"ok": True, "user": safe, "total": len(users)})


@app.route("/api/users")
def list_users():
    # 확인용: 가입된 사용자 목록 (비밀번호 제외)
    safe_list = [{k: v for k, v in u.items() if k != "password"} for u in users]
    return jsonify({"total": len(safe_list), "users": safe_list})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
