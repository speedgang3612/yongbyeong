# Agent Instructions — 용병 (Yongbyeong)
>
> This file is mirrored across CLAUDE.md, AGENTS.md, and GEMINI.md so the same instructions load in any AI environment.
> AI 에이전트는 코드 작성, 파일 생성, 어떤 결정을 내리기 전에 반드시 이 파일을 먼저 읽어야 한다.

---

## 1. Project Overview

| 항목 | 내용 |
|------|------|
| **서비스명** | 용병 (Yongbyeong) |
| **한 줄 설명** | 플러스 지사의 세트 위기를 구하는 긴급 라이더 매칭 플랫폼 |
| **슬로건** | 세트가 무너지기 전에, 용병을 부르세요 |
| **디자인 레퍼런스** | <https://sgmatch.co.kr> |

### 핵심 컨셉

- 플러스 지사(쿠팡이츠/배민 플러스)는 하루 배달 물량(세트)을 정해진 시간 내에 소화해야 함
- 소화 못하면 **세트 붕괴** → 플랫폼 관리비/프로모션 수령 불가
- 소속 없는 숙련 라이더(**용병**)가 긴급 투입되어 세트 사수
- 지사는 용병에게 일당/건당 보수 지급

---

## 2. User Types

### 용병 라이더

- 플러스 지사 미소속 자유 라이더
- 숙련된 베테랑 배달 라이더
- 원하는 날짜/시간/지역에 자유롭게 출동 가능
- 일당 또는 건당으로 수익 창출
- **무료 가입**

### 플러스 지사

- 쿠팡이츠 플러스, 배민 플러스 등 플랫폼 지사
- 세트 물량 위기 시 용병 라이더 긴급 요청
- 필요 인원, 시간, 지역, 보수 조건 등록
- **유료 구독** (요금제 참고)

---

## 3. The 3-Layer Architecture

**Layer 1: Directive (What to do)**

- SOPs written in Markdown, live in `directives/`
- Define goals, inputs, tools/scripts, outputs, and edge cases
- Natural language instructions, like you'd give a mid-level employee

**Layer 2: Orchestration (Decision making)**

- This is you. Your job: intelligent routing.
- Read directives → call execution tools in order → handle errors → update directives
- Do NOT try doing everything manually; delegate complex work to execution scripts

**Layer 3: Execution (Doing the work)**

- Deterministic Python scripts in `execution/`
- Environment variables and API tokens stored in `.env`
- Handle API calls, data processing, file operations, DB interactions

> **Why this works:** 90% accuracy per step = 59% success over 5 steps. Push complexity into deterministic code. Focus on decision-making.

---

## 4. Page Map

```
/ (홈 — 랜딩)
├── /login                        로그인
├── /register                     회원가입 (라이더 / 지사 선택)
│
├── [라이더 영역]
│   ├── /rider/dashboard          내 대시보드
│   ├── /rider/requests           긴급 요청 목록
│   ├── /rider/history            출동 이력
│   └── /rider/profile            내 프로필
│
├── [지사 영역]
│   ├── /agency/dashboard         내 대시보드
│   ├── /agency/request/new       긴급 요청 등록
│   ├── /agency/requests          내 요청 목록
│   └── /agency/profile           지사 프로필
│
└── /pricing                      요금제
```

---

## 5. Page Specifications

### 5-1. 홈 랜딩페이지 (`/`)

#### Hero 섹션

- **헤드라인:** "세트가 무너지기 전에, 용병을 부르세요"
- **서브카피:** "숙련된 배달 라이더가 빠르게 출동합니다"
- **CTA 버튼 2개:**
  - Primary (레드): `용병 라이더로 가입`
  - Secondary (아웃라인): `긴급 라이더 요청`

#### 작동 방식 섹션 (How It Works)

- **지사 흐름:** 요청 등록 → 용병 매칭 → 출동 → 세트 사수
- **라이더 흐름:** 프로필 등록 → 요청 확인 → 지원 → 출동 → 수익

#### 숫자로 보는 플랫폼 섹션

- 등록 용병 수
- 매칭 완료 건수
- 세트 사수율

#### 요금제 섹션 (간략 티저)

- 지사용 요금제 요약
- "자세히 보기" → `/pricing` 링크

#### 하단 CTA 섹션

- "지금 바로 시작하세요"

---

### 5-2. 요금제 페이지 (`/pricing`)

**과금 대상:** 지사만 유료 (용병 라이더는 무료)

| 플랜 | 가격 | 월 요청 한도 | 특징 |
|------|------|------------|------|
| 베이직 | 29,000원/월 | 10건 | 기본 매칭 |
| 스탠다드 | 59,000원/월 | 30건 | 우선 매칭 + 알림 ⭐인기 |
| 프리미엄 | 99,000원/월 | 무제한 | 전담 지원 + 통계 |

> ⚠️ 위 금액, 한도, 특징은 모두 **임시값**입니다. 코드에 변수/주석으로 표시해 쉽게 수정 가능하도록 작성하세요.

- VAT 별도
- 각 플랜에 "시작하기" 버튼 포함
- 14일 무료체험: 보류 (현재 미포함)

---

### 5-3. 회원가입 페이지 (`/register`)

#### 가입 유형 선택 (첫 화면)

- `용병 라이더로 가입` 버튼
- `플러스 지사로 가입` 버튼

#### 용병 라이더 가입 폼

```
- 이름
- 연락처
- 활동 지역 (복수 선택)
- 배달 경력: 1년 미만 / 1~3년 / 3년 이상
- 이메일
- 비밀번호 / 비밀번호 확인
```

#### 플러스 지사 가입 폼

```
- 지사명
- 사업자등록번호
- 담당자 이름
- 연락처
- 이메일
- 비밀번호 / 비밀번호 확인
```

---

## 6. Core Features

### 용병 라이더

- 회원가입 / 프로필 등록 (경력, 활동 지역, 보유 장비)
- 출동 가능 일정 등록
- 지사 긴급 요청 목록 조회 및 지원
- 출동 이력 / 수익 내역 확인
- 평점 및 리뷰 수신

### 플러스 지사

- 회원가입 / 지사 정보 등록
- 긴급 라이더 요청 등록 (날짜, 시간, 지역, 필요 인원, 보수 조건)
- 지원한 용병 라이더 프로필 확인 및 수락/거절
- 출동 완료 확인 및 평점 등록
- 요청 이력 관리

### 공통

- 로그인 / 로그아웃
- 알림 (요청 등록, 지원, 수락, 출동 확정)
- 채팅 또는 연락처 공유 (매칭 후)

---

## 7. MVP Scope

### ✅ 1차 오픈 포함

- 홈 랜딩페이지
- 회원가입 (라이더 / 지사 구분)
- 로그인
- 지사: 긴급 요청 등록
- 라이더: 요청 목록 조회 및 지원
- 요금제 페이지

### ⏳ 2차 (제외)

- 실시간 알림
- 채팅
- 평점 / 리뷰
- 정산 자동화 연동 (sgnext.co.kr 연동)

---

## 8. Design Direction

| 항목 | 내용 |
|------|------|
| **분위기** | 긴박감, 속도감, 신뢰 |
| **배경** | 다크 (`#0a0a0a` ~ `#1a1a1a`) |
| **포인트 컬러** | 레드 (`#E53935` 또는 유사) |
| **서브 컬러** | 화이트 `#ffffff`, 그레이 `#888888` |
| **이미지 방향** | 배달 라이더 / 오토바이 / 도시 야경 |
| **레퍼런스** | sgmatch.co.kr |

**UI 패턴 (sgmatch.co.kr 참고):**

- 히어로: 풀스크린 배경 + 대형 헤딩 + CTA 버튼 2개
- 카드: 다크 카드 (`#1a1a1a`) + 레드 뱃지/아이콘
- 버튼: 레드 채움 (Primary) + 아웃라인 (Secondary)
- 통계 숫자: 굵고 크게, 신뢰감 부여
- 반응형: 모바일 우선 (375px ~ 1440px)

---

## 9. Tech Stack

| 항목 | 선택 | 비고 |
|------|------|------|
| **프론트엔드** | HTML + CSS + JS (단일 파일) | MVP 기준; React 전환 가능 |
| **백엔드** | Python Flask | sgnext.co.kr과 동일 스택 |
| **DB** | SQLite → PostgreSQL 전환 예정 | |
| **호스팅** | PythonAnywhere 또는 Vercel | |
| **결제** | 토스페이먼츠 | |

> MVP는 HTML/CSS/JS 단일 파일로 시작. 각 페이지별 1개 파일로 구성.

---

## 10. File & Directory Structure

```
yongbyeong/
├── agent.md                        ← 이 파일 (AI 지침서)
├── CLAUDE.md                       ← agent.md 미러
├── AGENTS.md                       ← agent.md 미러
├── GEMINI.md                       ← agent.md 미러
├── .env                            ← API 키, 환경변수 (커밋 금지)
│
├── directives/
│   ├── build_landing.md            ← 홈 랜딩페이지 구축 지침
│   ├── build_pricing.md            ← 요금제 페이지 구축 지침
│   ├── build_register.md           ← 회원가입 페이지 구축 지침
│   ├── build_rider_dashboard.md    ← 라이더 대시보드 구축 지침
│   ├── build_agency_dashboard.md   ← 지사 대시보드 구축 지침
│   └── deploy.md                   ← 배포 지침
│
├── execution/
│   ├── setup_project.py            ← 프로젝트 초기 세팅
│   ├── generate_mock_data.py       ← 샘플 데이터 생성
│   ├── build_pages.py              ← 페이지 빌드 스크립트
│   └── deploy.py                   ← 배포 스크립트
│
├── pages/
│   ├── index.html                  ← 홈 랜딩
│   ├── pricing.html                ← 요금제
│   ├── login.html                  ← 로그인
│   ├── register.html               ← 회원가입
│   ├── rider/
│   │   ├── dashboard.html
│   │   ├── requests.html
│   │   ├── history.html
│   │   └── profile.html
│   └── agency/
│       ├── dashboard.html
│       ├── request-new.html
│       ├── requests.html
│       └── profile.html
│
└── .tmp/                           ← 임시 파일 (커밋 금지, 재생성 가능)
```

---

## 11. Antigravity Build Prompts

> 아래 프롬프트를 안티그래비티(또는 다른 AI 코딩 툴)에 그대로 붙여넣어 시작하세요.

### Prompt 1 — 홈 랜딩페이지

```
서비스명: 용병

배달 라이더 긴급 매칭 플랫폼의 홈 랜딩페이지를 만들어줘.

서비스 개념:
- 플러스 지사(쿠팡이츠/배민 플러스 지사)가 하루 배달 물량(세트)을 못 소화할 것 같을 때
- 소속 없는 숙련 배달 라이더(용병)를 긴급으로 매칭해주는 플랫폼
- 용병 라이더가 투입되어 세트를 사수하면 지사는 플랫폼 관리비/프로모션 수령 가능

페이지 구성:
1. Hero 섹션
   - 헤드라인: "세트가 무너지기 전에, 용병을 부르세요"
   - 서브: "숙련된 배달 라이더가 빠르게 출동합니다"
   - 버튼 2개: "용병 라이더로 가입" / "긴급 라이더 요청"

2. 작동 방식 섹션
   - 지사 흐름: 요청 등록 → 용병 매칭 → 출동 → 세트 사수
   - 라이더 흐름: 프로필 등록 → 요청 확인 → 지원 → 수익

3. 숫자 섹션
   - 등록 용병 수 / 매칭 완료 건수 / 세트 사수율

4. CTA 섹션
   - "지금 바로 시작하세요"

디자인 방향:
- 다크 배경 (검정/짙은 회색 계열)
- 레드 포인트 컬러 (#E53935 또는 유사)
- 강렬하고 긴박감 있는 느낌
- 배달 라이더/오토바이 분위기
- 반응형 (모바일 대응)

기술: HTML + CSS + JS 단일 파일로 만들어줘.
완성 후 스스로 오류 점검하고 "완료" 보고해줘.
```

---

### Prompt 2 — 요금제 페이지

```
서비스명: 용병

배달 라이더 긴급 매칭 플랫폼의 요금제 페이지를 만들어줘.

과금 구조:
- 용병 라이더: 무료
- 플러스 지사: 유료 구독

요금제 3가지 (아래 금액과 조건은 임시값 — 나중에 쉽게 수정 가능하도록 변수나 주석으로 표시해줘):
- 베이직: 29,000원/월, 월 요청 10건, 기본 매칭
- 스탠다드: 59,000원/월, 월 요청 30건, 우선 매칭 + 알림 (인기 표시)
- 프리미엄: 99,000원/월, 무제한, 전담 지원 + 통계

공통사항:
- VAT 별도
- 각 플랜에 "시작하기" 버튼

디자인: 홈 랜딩페이지와 동일한 다크 테마 유지
기술: HTML + CSS + JS 단일 파일
완성 후 스스로 오류 점검하고 "완료" 보고해줘.
```

---

### Prompt 3 — 회원가입 페이지

```
서비스명: 용병

배달 라이더 긴급 매칭 플랫폼의 회원가입 페이지를 만들어줘.

가입 유형 선택:
- 용병 라이더로 가입
- 플러스 지사로 가입

용병 라이더 가입 폼:
- 이름
- 연락처
- 활동 지역 (복수 선택)
- 배달 경력 (1년 미만 / 1~3년 / 3년 이상)
- 이메일
- 비밀번호 / 비밀번호 확인

플러스 지사 가입 폼:
- 지사명
- 사업자등록번호
- 담당자 이름
- 연락처
- 이메일
- 비밀번호 / 비밀번호 확인

디자인: 홈 랜딩페이지와 동일한 다크 테마 유지
기술: HTML + CSS + JS 단일 파일
완성 후 스스로 오류 점검하고 "완료" 보고해줘.
```

---

## 12. Operating Principles (AI Agent Rules)

### 1. Check for tools first

- 스크립트 작성 전 `execution/` 폴더 먼저 확인
- 기존 스크립트가 있으면 재사용, 없을 때만 신규 생성

### 2. Self-anneal when things break

1. 에러 메시지 + 스택 트레이스 읽기
2. 스크립트 수정 후 재테스트
3. directive 업데이트 (학습 내용 반영)
4. 유료 API / 토큰 사용 전 사용자에게 반드시 확인

### 3. Update directives as you learn

- Directive는 살아있는 문서
- API 제한, 더 좋은 접근법, 엣지케이스 발견 시 → 즉시 업데이트
- 사용자 허락 없이 directive를 새로 만들거나 덮어쓰지 말 것

### 4. Deliverables vs Intermediates

- **Deliverables:** 배포된 URL, 완성된 HTML 파일
- **Intermediates:** `.tmp/` 폴더에만 저장, 절대 커밋 금지

---

## 13. Self-Annealing Loop

에러 발생 시:

1. 에러 분석 → 원인 파악
2. 스크립트 수정
3. 테스트 통과 확인
4. directive 업데이트
5. 시스템이 더 강해짐 ✓

---

## 14. Edge Cases & Known Constraints

| 항목 | 내용 |
|------|------|
| **이미지 리소스** | 히어로 배경 없으면 Unsplash "배달 라이더 야경" 키워드로 대체 |
| **가격 정보** | 모두 임시값. 코드 상단 변수/주석으로 분리해 수정 용이하게 |
| **DB** | MVP는 SQLite, 이후 PostgreSQL 전환 |
| **반응형** | 모바일 우선 375px ~ 1440px 지원 필수 |
| **언어** | 초기 버전 한국어 전용. i18n은 추후 추가 |
| **결제** | 토스페이먼츠 연동 (2차) |
| **알림/채팅** | 2차 기능, MVP 제외 |

---

## Summary

**용병**은 플러스 지사의 세트 위기를 숙련 라이더(용병)로 해결하는 긴급 매칭 플랫폼이다.
AI 에이전트는 이 지침서를 읽고, directive를 확인하고, execution 스크립트를 실행하는 방식으로 동작한다.
직접 모든 것을 하려 하지 말고, 복잡한 작업은 결정론적 스크립트에 위임하라.

**Be pragmatic. Be reliable. Self-anneal.**
