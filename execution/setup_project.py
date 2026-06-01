#!/usr/bin/env python3
"""
setup_project.py — 용병 프로젝트 초기 세팅 스크립트

실행 방법: python execution/setup_project.py
"""

import os
import pathlib

# ============================================================
# 프로젝트 루트 기준 생성할 디렉토리 목록
# ============================================================
DIRECTORIES = [
    "directives",
    "execution",
    "pages/rider",
    "pages/agency",
    ".tmp",
]

# ============================================================
# 생성할 빈 파일 목록 (아직 없는 경우)
# ============================================================
PLACEHOLDER_FILES = [
    "pages/index.html",
    "pages/pricing.html",
    "pages/login.html",
    "pages/register.html",
    "pages/rider/dashboard.html",
    "pages/rider/requests.html",
    "pages/rider/history.html",
    "pages/rider/profile.html",
    "pages/agency/dashboard.html",
    "pages/agency/request-new.html",
    "pages/agency/requests.html",
    "pages/agency/profile.html",
]

GITIGNORE_CONTENT = """.env
.tmp/
__pycache__/
*.pyc
*.pyo
.DS_Store
"""


def main():
    root = pathlib.Path(__file__).parent.parent.resolve()
    print(f"[setup] 프로젝트 루트: {root}")

    # 디렉토리 생성
    for d in DIRECTORIES:
        target = root / d
        target.mkdir(parents=True, exist_ok=True)
        print(f"[setup] 디렉토리 확인/생성: {target}")

    # 플레이스홀더 HTML 파일 생성 (없는 경우만)
    for f in PLACEHOLDER_FILES:
        target = root / f
        if not target.exists():
            target.write_text(
                f"<!-- TODO: {f} — agent.md directives 참고하여 구현 -->\n",
                encoding="utf-8",
            )
            print(f"[setup] 플레이스홀더 생성: {target}")
        else:
            print(f"[setup] 이미 존재, 스킵: {target}")

    # .gitignore 생성 (없는 경우만)
    gitignore = root / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text(GITIGNORE_CONTENT, encoding="utf-8")
        print(f"[setup] .gitignore 생성: {gitignore}")
    else:
        print(f"[setup] .gitignore 이미 존재, 스킵")

    print("\n[setup] 프로젝트 구조 초기화 완료!")


if __name__ == "__main__":
    main()
