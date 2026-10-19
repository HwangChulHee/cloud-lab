# u3. Durability, Availability와 S3 Standard

S3 Storage Class를 비교할 때 `Durability`와 `Availability`가 계속 나온다. 둘은 비슷해 보이지만 다른 개념이다.

## 1. Durability — 데이터가 안 사라지는 정도

Durability는 저장한 Object가 **유실되지 않고 보존될 가능성**을 의미한다.

S3는 매우 높은 내구성을 제공한다.

```text
99.999999999%
= 11 9's durability
```

쉽게 말하면 하드웨어 하나가 고장 났다고 Object가 바로 사라지는 구조가 아니라는 뜻이다.

### 비유

```text
Durability
→ 내 사진 파일이 영구적으로 사라질 위험이 얼마나 낮은가?
```

---

## 2. Availability — 지금 접근 가능한 정도

Availability는 서비스나 Object에 **필요한 순간 접근할 수 있는 가능성**이다.

### 비유

```text
Durability
→ 사진이 없어지지 않았는가?

Availability
→ 지금 당장 그 사진을 열 수 있는가?
```

파일이 안전하게 보존되어 있어도 일시적 서비스 장애 때문에 잠깐 접근하지 못할 수 있다. 이 경우 Durability 문제와 Availability 문제는 다르다.

---

## 3. S3 Standard

S3 Standard는 일반적인 기본 Storage Class다.

특징:

```text
자주 접근하는 데이터
낮은 latency
높은 throughput
여러 AZ에 저장되는 높은 내구성
99.99% Availability
```

### 사용 사례

```text
웹사이트 콘텐츠
상품 이미지
모바일/게임 데이터
Big Data 원본
자주 사용하는 애플리케이션 파일
```

---

## 4. 예시

쇼핑몰 메인 상품 이미지는 사용자가 계속 조회한다.

```text
products/1001/main.jpg
```

매 요청마다 빠르게 접근해야 하므로 처음부터 장기 보관용 Glacier에 넣는 것은 적합하지 않다.

```text
자주 접근
+ 즉시 응답 필요
→ S3 Standard
```

반대로 7년 동안 보관만 하는 오래된 감사 로그라면 더 저렴한 Archive 계열을 검토할 수 있다.

---

## 5. Storage Class 선택의 기본 사고

가격만 보고 가장 싼 Class를 고르는 것이 아니다.

다음을 같이 본다.

```text
얼마나 자주 접근하는가?
접근할 때 얼마나 빨리 필요하나?
여러 AZ 보호가 필요한가?
얼마나 오래 보관하는가?
검색/복구 비용을 감수할 수 있는가?
```

## SAA 포인트

```text
데이터 자체가 사라지지 않는 정도
→ Durability

필요할 때 접근 가능한 정도
→ Availability

자주 접근하는 일반 데이터
→ S3 Standard
```
