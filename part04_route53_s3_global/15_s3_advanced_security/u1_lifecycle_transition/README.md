# u1. Lifecycle Rules & Storage Class Transition

## 지도 확인

S3에 파일을 계속 쌓아두면 시간이 지나도 비싼 Storage Class에 남아 비용이 커질 수 있다.

Lifecycle Rule은 객체의 나이와 조건에 따라 **자동으로 Storage Class를 바꾸거나 삭제**하는 정책이다.

```text
업로드 직후
S3 Standard
   ↓ 30일
Standard-IA
   ↓ 90일
Glacier Flexible Retrieval
   ↓ 365일
삭제
```

여기서 `Lifecycle`은 객체의 생애주기, `Transition`은 한 Storage Class에서 다른 Class로 옮기는 것을 뜻한다.

## Transition과 Expiration

Lifecycle Rule의 대표 동작은 두 가지다.

```text
Transition
→ 객체를 다른 Storage Class로 이동

Expiration
→ 일정 시간이 지난 객체를 삭제
```

예를 들어 쇼핑몰의 주문 감사 로그를 생각해보자.

```text
최근 30일
→ 자주 조회하므로 Standard

30일~1년
→ 가끔 조회하므로 Standard-IA

1년 이후
→ 법적 보관만 필요하므로 Glacier
```

사람이 매일 직접 옮길 필요 없이 S3가 규칙에 따라 처리한다.

## Versioning과 Lifecycle

Versioning을 사용하면 현재 버전뿐 아니라 과거 버전도 계속 남는다.

예:

```text
product.jpg v3 ← 현재
product.jpg v2
product.jpg v1
```

과거 버전이 무한히 쌓이면 비용이 증가한다. 그래서 Lifecycle Rule은 noncurrent version에도 적용할 수 있다.

예:

```text
과거 버전이 된 뒤 30일
→ IA로 이동

90일
→ Glacier

365일
→ 삭제
```

## SAA 판단

```text
시간이 지나면 자동으로 저렴한 Storage Class로 이동
→ Lifecycle Transition

오래된 데이터 자동 삭제
→ Lifecycle Expiration

Versioning의 과거 버전 비용 최적화
→ Noncurrent version Lifecycle Rule
```

핵심은 "접근 빈도가 시간에 따라 줄어드는 데이터"가 나오면 Lifecycle을 떠올리는 것이다.
