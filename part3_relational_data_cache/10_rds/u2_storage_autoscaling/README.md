# u2. Storage & Storage Auto Scaling

## 1. RDS의 Storage

RDS도 데이터를 어딘가에 저장해야 한다.

개념적으로는:

```text
RDS DB Instance
   │
   ▼
Persistent Storage
```

구조로 생각하면 된다.

DB Instance는 CPU/Memory를 제공하고 Storage는 실제 테이블과 인덱스 데이터를 저장한다.

---

## 2. Instance 크기와 Storage 크기는 다른 문제다

처음에 자주 헷갈리는 부분이다.

```text
DB Instance
→ CPU / Memory 성능

Storage
→ 데이터를 얼마나 저장할 수 있는지 + I/O 특성
```

예를 들어:

```text
CPU는 충분한데
DB 디스크가 거의 가득 참
```

이면 큰 DB Instance로 바꾸는 것만으로 저장 공간 문제가 해결되는 것은 아니다.

반대로:

```text
저장 공간은 많이 남았지만
쿼리 처리 CPU가 항상 100%
```

이면 Storage보다 Instance 성능을 고민해야 한다.

---

## 3. Storage Auto Scaling

`Auto Scaling`은 필요한 만큼 자동으로 늘린다는 뜻이다.

RDS Storage Auto Scaling은 DB 저장 공간이 부족해질 때 설정한 범위 안에서 Storage를 자동으로 확장하는 기능이다.

예:

```text
현재 Storage: 100 GB
Maximum Storage Threshold: 500 GB
```

서비스가 성장하면서 데이터가 쌓인다.

```text
상품
주문
로그성 데이터
사용자 데이터
```

Storage가 부족해질 조짐이 보이면 AWS가 자동으로 공간을 늘릴 수 있다.

```text
100 GB
→ 130 GB
→ 이후 필요 시 더 증가
```

정확한 증가량을 암기하기보다 시험에서는:

> **예상하지 못한 데이터 증가 때문에 RDS가 저장 공간 부족으로 멈추는 위험을 줄이는 기능**

으로 이해하면 된다.

---

## 4. 왜 Maximum Threshold를 두나

무한정 자동 확장되면 비용도 계속 증가할 수 있다.

그래서 최대 Storage를 지정한다.

예:

```text
초기: 100 GB
최대: 1 TB
```

이렇게 하면:

```text
100 GB → 자동 증가 가능 → 최대 1 TB
```

까지만 허용한다.

즉 Auto Scaling은:

```text
"무제한으로 늘려줘"
```

가 아니라:

```text
"필요하면 이 한도까지 자동으로 늘려줘"
```

라는 의미다.

---

## 5. 예시 — 쇼핑몰 주문 DB

처음 예상:

```text
하루 주문 1,000건
Storage 50 GB면 충분
```

그런데 이벤트가 터져서 주문과 이력 데이터가 급격히 증가했다고 해보자.

Storage Auto Scaling이 없다면 운영자가 직접 용량을 확인하고 확장해야 한다.

```text
Storage 95%
→ 운영자가 늦게 발견
→ 공간 부족 위험
```

Auto Scaling을 설정했다면:

```text
Storage 부족 예상
→ RDS가 자동 확장
→ 운영 여유 확보
```

이런 용도다.

---

## SAA 판단

```text
DB 데이터 크기가 계속 증가하지만 정확한 증가량을 예측하기 어렵다
→ RDS Storage Auto Scaling

CPU/Memory 부족
→ 더 큰 DB Instance Class 검토

읽기 요청 자체가 너무 많다
→ Storage Auto Scaling이 아니라 Read Replica 검토
```

특히 마지막 세 가지를 구분해야 한다.

```text
저장 공간 부족
→ Storage 확장

DB 자체 연산 성능 부족
→ Vertical Scaling

Read Traffic 과다
→ Read Replica
```
