# u7. S3 Lifecycle Rules

Lifecycle Rule은 Object가 오래될수록 **다른 Storage Class로 자동 이동시키거나 삭제**하도록 만드는 정책이다.

## 1. 왜 필요한가

모든 데이터를 계속 S3 Standard에 두면 관리하기는 쉽지만 오래된 데이터까지 비싼 Class에 남을 수 있다.

예:

```text
접속 로그
첫 30일: 자주 조회
30일 이후: 거의 조회 안 함
1년 이후: 보관 의무만 있음
7년 이후: 삭제 가능
```

사람이 매달 직접 파일을 옮기는 대신 Lifecycle Rule로 자동화한다.

---

## 2. Transition

Transition은 Object를 다른 Storage Class로 이동시키는 동작이다.

예:

```text
생성
 ↓
S3 Standard
 ↓ 30일
Standard-IA
 ↓ 90일
Glacier Flexible Retrieval
 ↓ 365일
Glacier Deep Archive
```

이렇게 데이터의 가치와 접근 빈도가 시간에 따라 떨어지는 패턴에 적합하다.

---

## 3. Expiration

Expiration은 일정 시간이 지나면 Object를 삭제하는 정책이다.

예:

```text
임시 업로드 파일
→ 7일 후 삭제

로그
→ 7년 후 삭제
```

즉 Lifecycle은 이동만 하는 기능이 아니라 삭제 자동화도 포함한다.

---

## 4. Versioning과 Lifecycle

Versioning이 켜져 있으면 이전 버전도 계속 저장 공간을 차지할 수 있다.

예:

```text
report.csv
├── current version
├── old version 1
├── old version 2
└── old version 3
```

Lifecycle Rule로 오래된 non-current version을 저렴한 Storage Class로 보내거나 일정 시간이 지나면 제거할 수 있다.

그래서 다음 조합이 자주 등장한다.

```text
Versioning
→ 실수 복구 가능

Lifecycle
→ 오래된 버전 비용 관리
```

---

## 5. Prefix/Tag 기준 적용

모든 Object에 같은 Lifecycle을 적용할 필요는 없다.

예:

```text
logs/
→ 30일 후 IA
→ 365일 후 Glacier

products/
→ Standard 유지
```

Key Prefix나 Tag 등을 기준으로 특정 Object 집합에 Rule을 적용할 수 있다.

---

## 6. Storage Class의 최소 보관 기간 고려

Lifecycle Transition을 너무 빠르게 설정하면 Storage Class의 minimum storage duration 조건 때문에 기대와 다른 비용이 발생할 수 있다.

즉:

```text
저렴한 Class로 빨리 옮기면 무조건 이득
```

은 아니다.

보관 기간과 Retrieval 비용까지 함께 봐야 한다.

---

## 예시 — 쇼핑몰 로그

요구사항:

```text
최근 30일 로그는 자주 조회
1년 이내 로그는 장애 분석용으로 가끔 조회
1년 이후는 규정상 보관만 필요
7년 이후 삭제
```

가능한 설계 예:

```text
0~30일
→ S3 Standard

30일 이후
→ Standard-IA

1년 이후
→ Glacier Deep Archive

7년 이후
→ Expiration
```

핵심은 정확한 날짜 조합을 외우는 것이 아니라 Lifecycle이 **시간에 따른 비용 최적화 정책**이라는 점이다.

## SAA 포인트

```text
오래된 Object를 자동으로 저렴한 Class로 이동
→ Lifecycle Transition

일정 기간 후 자동 삭제
→ Expiration

오래된 Version 비용 절감
→ non-current version Lifecycle

특정 종류의 Object만 정책 적용
→ Prefix/Tag Filter
```
