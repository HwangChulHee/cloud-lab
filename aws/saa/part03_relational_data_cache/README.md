# Part 03 — Relational Data & Cache

SAA 강의의 `RDS, Aurora & ElastiCache` 섹션을 세 단원으로 나눈다.

```text
10. RDS
→ 일반적인 관리형 관계형 DB

11. Aurora
→ MySQL/PostgreSQL compatible + distributed storage / cluster architecture

12. ElastiCache
→ Redis/Memcached 기반 in-memory cache
```

## 학습 순서

1. [10. Amazon RDS](./10_rds/README.md)
2. [11. Amazon Aurora](./11_aurora/README.md)
3. [12. Amazon ElastiCache](./12_elasticache/README.md)

## 가장 중요한 구분

```text
읽기 확장을 위해 DB 복제본 사용
→ RDS Read Replica / Aurora Reader

DB 장애 자동 복구
→ RDS Multi-AZ / Aurora HA 구조

MySQL/PostgreSQL compatible + Aurora 전용 distributed storage
→ Aurora

반복 조회 결과를 메모리에 저장해 DB 부하 감소
→ ElastiCache

여러 App Instance의 session 공유
→ ElastiCache Session Store
```

이 파트의 목표는 서비스 이름을 외우는 것이 아니라 **DB 원본 저장, 읽기 확장, 고가용성, cache**가 서로 어떤 문제를 해결하는지 구분하는 것이다.
