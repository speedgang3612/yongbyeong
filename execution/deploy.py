#!/usr/bin/env python3
"""
deploy.py — 배포 스크립트

⚠️  이 스크립트는 반드시 사용자 확인 후 실행해야 합니다.
실행 방법: python execution/deploy.py

지원 플랫폼:
  - vercel: Vercel 정적 배포
  - pythonanywhere: PythonAnywhere Flask 배포 (추후 구현)
"""

import subprocess
import sys
import pathlib

ROOT = pathlib.Path(__file__).parent.parent.resolve()


def check_build():
    """배포 전 빌드 상태 점검"""
    result = subprocess.run(
        [sys.executable, str(ROOT / "execution" / "build_pages.py")],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print("[deploy] ❌ 빌드 점검 실패. 배포를 중단합니다.")
        print(result.stderr)
        sys.exit(1)


def deploy_vercel():
    """Vercel 배포"""
    print("[deploy] Vercel 배포를 시작합니다...")
    result = subprocess.run(["vercel", "--prod"], cwd=ROOT)
    if result.returncode == 0:
        print("[deploy] ✅ Vercel 배포 완료!")
    else:
        print("[deploy] ❌ Vercel 배포 실패")
        sys.exit(1)


def main():
    platform = sys.argv[1] if len(sys.argv) > 1 else "vercel"

    print("=" * 50)
    print(f"[deploy] 용병 배포 시작 — 플랫폼: {platform}")
    print("⚠️  배포 전 사용자 확인이 완료된 경우에만 실행하세요.")
    print("=" * 50)

    # 1. 빌드 상태 점검
    check_build()

    # 2. 배포 실행
    if platform == "vercel":
        deploy_vercel()
    elif platform == "pythonanywhere":
        print("[deploy] PythonAnywhere 배포는 수동 진행이 필요합니다.")
        print("  1. git push origin main")
        print("  2. PythonAnywhere 콘솔에서 git pull 및 WSGI 재시작")
    else:
        print(f"[deploy] ❌ 알 수 없는 플랫폼: {platform}")
        sys.exit(1)


if __name__ == "__main__":
    main()
