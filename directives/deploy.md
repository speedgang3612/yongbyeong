# 배포 지침 (deploy.md)

## 목표
용병 서비스를 PythonAnywhere 또는 Vercel에 배포한다.

## 사전 조건
- `pages/` 폴더 내 모든 HTML 파일 완성
- `.env` 파일 준비 (커밋 금지)
- `execution/deploy.py` 실행 가능 상태

## 배포 옵션

### 옵션 A: PythonAnywhere (Flask 백엔드 포함 시)
1. PythonAnywhere 계정 준비
2. Git push → PythonAnywhere pull
3. 환경변수 설정 (`.env` 내용을 PythonAnywhere 환경변수로 등록)
4. WSGI 설정 확인

### 옵션 B: Vercel (정적 HTML만)
1. Vercel CLI 설치: `npm i -g vercel`
2. `vercel deploy --prod` 실행
3. 도메인 연결

## 주의사항
- `.env` 절대 커밋 금지 (`.gitignore`에 등록 확인)
- 배포 전 로컬 테스트 완료 필수
- `execution/deploy.py` 실행 전 사용자 확인 받을 것

## 완료 조건
- 배포 URL 접속 확인
- 홈 → 요금제 → 회원가입 흐름 동작 확인
