# u5. Aurora Machine Learning, Database Cloning & SAA Selection

## 지도 확인

Aurora에는 기본적인 관계형 DB 기능 외에 시험에서 구분해야 하는 전용 기능이 있다.

```text
DB 데이터 기반 ML 호출
→ Aurora Machine Learning

기존 cluster를 빠르게 복제
→ Aurora Database Cloning
```

---

## 1. Aurora Machine Learning

강의에서는 Aurora가 **Amazon SageMaker와 Amazon Comprehend**를 이용해 ML 기능과 연동할 수 있다고 설명한다.

개념적으로:

```text
Application
   ↓
Aurora
   ↓
SageMaker / Comprehend
```

예를 들어 DB의 데이터를 기반으로 예측이나 텍스트 분석 기능을 호출하는 구조를 만들 수 있다.

이 단원에서 중요한 건 ML 모델을 직접 만드는 방법이 아니라:

> Aurora에서 데이터를 별도 애플리케이션 계층으로 크게 이동시키지 않고 AWS ML 서비스와 연동할 수 있다.

는 선택 기준이다.

---

## 2. Aurora Database Cloning

Database Cloning은 기존 Aurora cluster를 기반으로 새로운 cluster를 빠르게 만드는 기능이다.

```text
Production Aurora
      │
      └─ Clone
           ↓
      Test / Dev Aurora
```

강의에서는 Snapshot을 restore해서 전체 데이터를 새로 복사하는 방식보다 빠른 개발/테스트 환경 생성 용도로 설명한다.

대표 사용 사례:

```text
Production 데이터와 비슷한 환경으로 테스트
개발용 DB 빠르게 생성
실험용 cluster 분리
```

---

## 3. Aurora 전체 선택 지도

```text
MySQL/PostgreSQL compatible 관계형 DB
+ AWS-native HA/scale 기능
→ Aurora

Read workload 증가
→ Aurora Replicas + Reader Endpoint

Read replica 수를 workload에 맞춰 자동 조절
→ Aurora Auto Scaling

간헐적 / 예측 어려운 workload
→ Aurora Serverless

글로벌 read latency + DR
→ Aurora Global Database

DB에서 SageMaker/Comprehend 연동
→ Aurora Machine Learning

운영 cluster 기반으로 빠른 test/dev DB 생성
→ Aurora Database Cloning
```

---

## 4. RDS / Aurora / ElastiCache를 섞지 않기

```text
일반 관리형 관계형 DB
→ RDS

MySQL/PostgreSQL 호환 + Aurora 전용 분산 구조
→ Aurora

DB 앞에서 자주 읽는 데이터를 메모리에 캐시
→ ElastiCache
```

Aurora와 ElastiCache는 경쟁 관계라기보다 같이 사용할 수 있다.

```text
Application
   ↓
ElastiCache
   ↓ cache miss
Aurora
```

---

## 완료 체크

- [ ] Aurora의 compute/storage 분리를 설명할 수 있다.
- [ ] 3 AZ / 6 copies의 의미를 설명할 수 있다.
- [ ] Writer / Reader Endpoint를 구분할 수 있다.
- [ ] Aurora Serverless가 적합한 workload를 설명할 수 있다.
- [ ] Global Database의 Primary / Secondary 구조를 설명할 수 있다.
- [ ] Aurora Machine Learning과 Database Cloning의 용도를 구분할 수 있다.

## 기억만으로 설명하기

`Application → Endpoint → DB Instance → Shared Storage` 흐름을 그리고, RDS와 무엇이 다른지 설명한다.
