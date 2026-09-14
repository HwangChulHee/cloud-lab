# 11. Amazon Aurora

SAA 강의의 `RDS, Aurora & ElastiCache` 섹션 중 **Amazon Aurora** 부분을 정리한다.

Aurora는 MySQL / PostgreSQL 호환 API를 제공하는 AWS의 관계형 데이터베이스다. 강의에서는 **Compute와 Storage의 분리**, **3개 AZ에 6개 데이터 복제본**, **Writer / Reader Endpoint**, **Read Replica Auto Scaling**, **Serverless**, **Global Database**, **Machine Learning**, **Database Cloning**을 핵심으로 다룬다.

## Units

- [ ] u1. Aurora Architecture & Storage
- [ ] u2. Writer, Reader & Read Replicas
- [ ] u3. High Availability, Failover & Auto Scaling
- [ ] u4. Aurora Serverless & Global Database
- [ ] u5. Machine Learning, Cloning & SAA Selection

## 전체 지도

```text
Application
    │
    ├── Write
    │     ↓
    │  Writer Endpoint
    │     ↓
    │  Writer Instance
    │
    └── Read
          ↓
      Reader Endpoint
       ├─ Reader 1
       ├─ Reader 2
       └─ Reader N

            ↓
      Shared Aurora Storage
      6 copies across 3 AZ
```

Aurora에서 중요한 관점은 **DB Instance와 Storage를 하나로 보지 않는 것**이다.

```text
Compute
→ Writer / Reader DB Instances

Storage
→ 여러 AZ에 복제되는 shared cluster storage
```

## 가장 중요한 SAA 구분

```text
MySQL/PostgreSQL 호환 + 더 높은 가용성/확장성
→ Aurora

읽기 요청 분산
→ Reader Endpoint + Aurora Replicas

예측하기 어려운 간헐적 DB workload
→ Aurora Serverless

여러 Region에서 낮은 read latency + DR
→ Aurora Global Database

기존 Aurora cluster에서 빠르게 테스트/개발용 복제본 생성
→ Aurora Database Cloning

DB 데이터를 기반으로 ML 예측 호출
→ Aurora Machine Learning
```

## RDS와 연결해서 보기

```text
RDS
→ 일반적인 관리형 관계형 DB
→ engine별 구조와 instance/storage 관리

Aurora
→ MySQL/PostgreSQL 호환
→ compute와 storage 분리
→ shared distributed storage
→ cluster endpoint / reader endpoint
→ Aurora 전용 확장 기능
```

Aurora도 RDS 계열에서 배운 보안, 모니터링, 백업/복구 개념과 연결해서 이해한다.

## 대표 예시

쇼핑몰 DB가 다음처럼 커졌다고 하자.

```text
주문/결제 Write
→ Writer Endpoint

상품/리뷰 Read
→ Reader Endpoint
```

읽기 부하가 증가하면 Reader를 추가하고, 애플리케이션은 Reader Endpoint를 통해 읽기 트래픽을 분산할 수 있다.

다음 단원은 ElastiCache로 이어진다.
