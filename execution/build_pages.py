#!/usr/bin/env python3
"""
build_pages.py — 페이지 빌드 스크립트

directives/ 폴더의 지침을 바탕으로 pages/ 폴더의 HTML을 검증한다.
실행 방법: python execution/build_pages.py
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).parent.parent.resolve()

# ============================================================
# MVP 필수 페이지 목록
# ============================================================
REQUIRED_PAGES = [
    "pages/index.html",
    "pages/pricing.html",
    "pages/login.html",
    "pages/register.html",
]

OPTIONAL_PAGES = [
    "pages/rider/dashboard.html",
    "pages/rider/requests.html",
    "pages/rider/history.html",
    "pages/rider/profile.html",
    "pages/agency/dashboard.html",
    "pages/agency/request-new.html",
    "pages/agency/requests.html",
    "pages/agency/profile.html",
]


def check_page(path: pathlib.Path, required: bool = True) -> bool:
    label = "[필수]" if required else "[선택]"
    if not path.exists():
        status = "[X] 없음"
        ok = False
    else:
        content = path.read_text(encoding="utf-8", errors="ignore")
        if "TODO" in content and len(content.strip()) < 200:
            status = "[!] 플레이스홀더"
            ok = False
        else:
            status = "[OK] 완료"
            ok = True
    print(f"  {label} {path.relative_to(ROOT)} : {status}")
    return ok


def main():
    print("=" * 50)
    print("[build] 용병 페이지 빌드 상태 점검")
    print("=" * 50)

    all_ok = True

    print("\n[필수 페이지]")
    for p in REQUIRED_PAGES:
        ok = check_page(ROOT / p, required=True)
        if not ok:
            all_ok = False

    print("\n[선택 페이지 (2차 기능 포함)]")
    for p in OPTIONAL_PAGES:
        check_page(ROOT / p, required=False)

    print("\n" + "=" * 50)
    if all_ok:
        print("[build] [OK] 모든 필수 페이지 완료! 배포 가능합니다.")
    else:
        print("[build] [!] 미완성 페이지가 있습니다. 위 목록을 확인하세요.")
        sys.exit(1)


if __name__ == "__main__":
    main()
