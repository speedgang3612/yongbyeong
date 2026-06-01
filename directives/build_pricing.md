# 요금제 페이지 구축 지침 (build_pricing.md)

## 목표
용병 서비스의 요금제 페이지(`pages/pricing.html`)를 구축한다.

## 입력
- agent.md (요금제 스펙)

## 출력
- `pages/pricing.html`

## 요금제 스펙 (아래 값은 모두 임시값 — 코드 상단 변수/주석으로 분리)

```
# ==============================
# 요금제 임시값 (나중에 수정 가능)
# ==============================
PLAN_BASIC_NAME = "베이직"
PLAN_BASIC_PRICE = 29000       # 원/월
PLAN_BASIC_LIMIT = 10          # 월 요청 건수
PLAN_BASIC_FEATURES = "기본 매칭"

PLAN_STANDARD_NAME = "스탠다드"
PLAN_STANDARD_PRICE = 59000    # 원/월
PLAN_STANDARD_LIMIT = 30       # 월 요청 건수
PLAN_STANDARD_FEATURES = "우선 매칭 + 알림"
PLAN_STANDARD_POPULAR = True   # 인기 플랜

PLAN_PREMIUM_NAME = "프리미엄"
PLAN_PREMIUM_PRICE = 99000     # 원/월
PLAN_PREMIUM_LIMIT = "무제한"
PLAN_PREMIUM_FEATURES = "전담 지원 + 통계"
```

## 페이지 구성
- 상단: 페이지 제목 + 설명 (용병 라이더 무료, 지사 유료)
- 카드 3개: 베이직 / 스탠다드(인기) / 프리미엄
- 각 카드: 플랜명, 가격, 한도, 특징, "시작하기" 버튼
- VAT 별도 안내 문구
- 하단: 홈으로 돌아가기 링크

## 디자인
- 홈 랜딩페이지와 동일한 다크 테마
- 인기 플랜(스탠다드)에 레드 배지 + 강조 테두리

## 완료 조건
- HTML 문법 오류 없음
- 반응형 확인 (375px ~ 1440px)
