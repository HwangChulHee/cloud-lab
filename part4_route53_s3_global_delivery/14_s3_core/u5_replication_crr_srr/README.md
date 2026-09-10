# u5. S3 Replication — CRR / SRR

S3 Replication은 한 Bucket의 Object를 다른 Bucket으로 **자동 복제**하는 기능이다.

## 1. CRR과 SRR

```text
CRR = Cross-Region Replication
→ 다른 Region으로 복제

SRR = Same-Region Replication
→ 같은 Region의 다른 Bucket으로 복제
```

### 예시 — CRR

```text
Seoul Bucket
   ↓ replication
Tokyo Bucket
```

재해복구, 지리적으로 가까운 데이터 제공, 규정상 다른 Region에 복사본이 필요한 상황 등에 사용할 수 있다.

### 예시 — SRR

```text
Production Bucket
   ↓ replication
Analytics Bucket
```

같은 Region에서 로그 집계, 계정/부서 분리, 테스트 데이터 복제 같은 용도로 생각할 수 있다.

---

## 2. Versioning이 필요하다

Replication을 사용하려면 Source와 Destination Bucket 모두 Versioning이 활성화되어 있어야 한다.

```text
Source Bucket: Versioning ON
Destination Bucket: Versioning ON
```

이유는 복제 대상 Object의 버전을 추적해야 하기 때문이다.

---

## 3. 복제는 비동기다

Object를 Source Bucket에 PUT했다고 Destination에 같은 순간 생기는 것은 아니다.

```text
PUT source
→ source 저장 완료
→ replication 진행
→ destination에 복사
```

즉 일반적인 Replication은 asynchronous하게 진행된다.

이 점은 "두 Bucket에 동시에 강한 일관성으로 쓰기" 같은 개념과 다르다.

---

## 4. 기존 Object는 어떻게 되나

Replication Rule을 만든다고 과거의 모든 Object가 자동으로 즉시 복제된다고 단순히 생각하면 안 된다.

기본적인 Replication은 Rule이 적용된 뒤 생성/변경되는 Object를 중심으로 동작하며, 기존 Object를 복제해야 하는 경우 별도의 Batch Replication 같은 기능을 고려할 수 있다.

---

## 5. 삭제와 복제

삭제 동작도 설정과 유형에 따라 복제 여부가 달라질 수 있다. 시험에서는 세부 API보다 "Replication은 단순 파일 복사가 아니라 Versioning과 Rule을 기반으로 동작한다"는 점을 우선 잡는다.

---

## 사용 사례 비교

```text
다른 Region에 DR 복사본
→ CRR

Compliance 때문에 다른 Region 보관
→ CRR

같은 Region의 분석용 Bucket으로 복제
→ SRR

Production과 Test/Analytics Bucket 분리
→ SRR
```

## SAA 포인트

```text
Cross-Region
→ CRR

Same-Region
→ SRR

Replication 전제
→ 양쪽 Bucket Versioning 활성화

복제 시점
→ 비동기
```
