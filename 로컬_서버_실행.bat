@echo off
title 용병 로컬 서버 실행기
echo ==========================================================
echo   용병 (Yongbyeong) MVP 로컬 웹 서버 실행기
echo   (이 창을 닫으면 로컬 서버 구동이 중단됩니다.)
echo ==========================================================
echo.
echo 1. 기본 웹 브라우저에서 용병 플랫폼 주소(http://localhost:8000)를 엽니다...
start http://localhost:8000

echo.
echo 2. pages 폴더를 루트로 하여 파이썬 로컬 서버를 가동합니다...
cd /d "%~dp0pages"
python -m http.server 8000
pause
