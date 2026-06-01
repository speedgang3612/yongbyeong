#!/usr/bin/env python3
"""
generate_mock_data.py — 샘플 데이터 생성 스크립트

SQLite DB에 테스트용 라이더/지사/요청 데이터를 삽입한다.
실행 방법: python execution/generate_mock_data.py
"""

import sqlite3
import pathlib
import datetime

DB_PATH = pathlib.Path(__file__).parent.parent / "yongbyeong.db"

# ============================================================
# 샘플 데이터 (임시값)
# ============================================================
MOCK_RIDERS = [
    {
        "name": "김철수",
        "phone": "010-1234-5678",
        "email": "chulsoo@example.com",
        "region": "서울 강남,서울 송파",
        "experience": "3년 이상",
        "password_hash": "PLACEHOLDER_HASH",
        "status": "active",
    },
    {
        "name": "이영희",
        "phone": "010-2345-6789",
        "email": "younghee@example.com",
        "region": "서울 마포,서울 용산",
        "experience": "1~3년",
        "password_hash": "PLACEHOLDER_HASH",
        "status": "active",
    },
]

MOCK_AGENCIES = [
    {
        "agency_name": "강남 플러스 지사",
        "business_number": "123-45-67890",
        "manager_name": "박지수",
        "phone": "010-3456-7890",
        "email": "gangnam@example.com",
        "password_hash": "PLACEHOLDER_HASH",
        "plan": "standard",
        "status": "active",
    },
]

MOCK_REQUESTS = [
    {
        "agency_id": 1,
        "region": "서울 강남",
        "date": (datetime.date.today() + datetime.timedelta(days=1)).isoformat(),
        "time_start": "10:00",
        "time_end": "18:00",
        "riders_needed": 3,
        "pay_type": "일당",
        "pay_amount": 150000,
        "status": "open",
        "description": "내일 세트 위기 예상. 숙련 라이더 3명 긴급 필요.",
    },
]


def init_db(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS riders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT UNIQUE NOT NULL,
            region TEXT,
            experience TEXT,
            password_hash TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS agencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agency_name TEXT NOT NULL,
            business_number TEXT,
            manager_name TEXT,
            phone TEXT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            plan TEXT DEFAULT 'basic',
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agency_id INTEGER NOT NULL,
            region TEXT,
            date TEXT,
            time_start TEXT,
            time_end TEXT,
            riders_needed INTEGER DEFAULT 1,
            pay_type TEXT,
            pay_amount INTEGER,
            status TEXT DEFAULT 'open',
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (agency_id) REFERENCES agencies(id)
        );
    """)
    conn.commit()
    print("[mock] DB 스키마 초기화 완료")


def insert_mock_data(conn):
    for r in MOCK_RIDERS:
        try:
            conn.execute(
                "INSERT INTO riders (name,phone,email,region,experience,password_hash,status) "
                "VALUES (:name,:phone,:email,:region,:experience,:password_hash,:status)",
                r,
            )
            print(f"[mock] 라이더 삽입: {r['name']}")
        except sqlite3.IntegrityError:
            print(f"[mock] 이미 존재, 스킵: {r['email']}")

    for a in MOCK_AGENCIES:
        try:
            conn.execute(
                "INSERT INTO agencies (agency_name,business_number,manager_name,phone,email,password_hash,plan,status) "
                "VALUES (:agency_name,:business_number,:manager_name,:phone,:email,:password_hash,:plan,:status)",
                a,
            )
            print(f"[mock] 지사 삽입: {a['agency_name']}")
        except sqlite3.IntegrityError:
            print(f"[mock] 이미 존재, 스킵: {a['email']}")

    for req in MOCK_REQUESTS:
        conn.execute(
            "INSERT INTO requests (agency_id,region,date,time_start,time_end,riders_needed,pay_type,pay_amount,status,description) "
            "VALUES (:agency_id,:region,:date,:time_start,:time_end,:riders_needed,:pay_type,:pay_amount,:status,:description)",
            req,
        )
        print(f"[mock] 요청 삽입: {req['region']} {req['date']}")

    conn.commit()


def main():
    print(f"[mock] DB 경로: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)
    insert_mock_data(conn)
    conn.close()
    print("\n[mock] ✅ 샘플 데이터 생성 완료!")


if __name__ == "__main__":
    main()
