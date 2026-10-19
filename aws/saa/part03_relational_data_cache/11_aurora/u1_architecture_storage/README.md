# u1. Aurora Architecture & Storage

## 지도 확인

Aurora를 이해할 때 가장 먼저 봐야 할 것은 **Compute와 Storage가 분리되어 있다는 점**이다.

```text
DB Instances
Writer / Readers
      │
      ▼
Shared Aurora Storage
6 copies across 3 AZ
```

강의에서는 Aurora Storage를 **3개 Availability Zone에 걸쳐 6개의 복제본을 유지하는 구조**로 설명한다.

---

## 1. MySQL / PostgreSQL 호환

Aurora는 MySQL과 PostgreSQL 호환 API를 제공한다.

즉 애플리케이션 관점에서는 익숙한 관계형 DB 방식으로 접근하면서, 내부 구조는 Aurora 전용 분산 스토리지를 사용한다.

```text
Application
   ↓ SQL
Aurora MySQL-compatible
또는
Aurora PostgreSQL-compatible
```

---

## 2. Compute와 Storage 분리

일반적으로 DB를 생각하면 하나의 DB 서버 안에 compute와 disk가 함께 있다고 떠올리기 쉽다.

Aurora는 개념적으로 다음처럼 나눈다.

```text
Compute
→ Writer / Reader DB Instance

Storage
→ Cluster가 공유하는 Aurora Storage
```

그래서 Reader Instance를 추가해도 각 Reader가 별도 데이터 사본을 독립적으로 운영하는 그림보다, **여러 DB Instance가 같은 distributed cluster storage를 사용하는 구조**로 이해하는 것이 중요하다.

---

## 3. 6 Copies across 3 AZ

강의의 핵심 숫자:

```text
3 AZ
6 copies
```

개념적으로:

```text
AZ-A   copy 1 / copy 2
AZ-B   copy 3 / copy 4
AZ-C   copy 5 / copy 6
```

이 구조는 Aurora가 높은 가용성과 self-healing storage를 제공하는 기반이 된다.

시험에서는 정확한 내부 구현을 계산하기보다:

> Aurora storage는 여러 AZ에 분산 복제되고 높은 내구성/가용성을 갖는다.

를 기억하는 것이 핵심이다.

---

## 4. Storage Auto Scaling

Aurora Storage는 데이터 증가에 따라 자동으로 확장되는 구조로 강의에서 설명한다.

따라서 RDS에서 배운 것처럼 애플리케이션이 매번 디스크 크기를 직접 늘리는 그림보다는:

```text
Data grows
   ↓
Aurora storage automatically expands
```

로 이해한다.

---

## 5. Self-Healing Storage

여러 복제본 중 일부에 문제가 생겨도 Aurora가 storage replica를 관리하고 복구한다.

사용자는 개별 storage server를 직접 관리하지 않는다.

```text
Storage copy failure
→ Aurora detects it
→ replica repair/recovery
```

---

## RDS와 비교

```text
RDS
→ DB Instance + engine별 storage 구조를 관리형으로 제공

Aurora
→ MySQL/PostgreSQL compatible
→ compute / storage separation
→ shared distributed storage
→ 3 AZ / 6 copies
```

---

## SAA 판단

```text
MySQL/PostgreSQL 계열 관계형 DB가 필요
+ 높은 가용성과 확장성
+ AWS-native distributed storage
→ Aurora 고려
```

## Recall Check

- Aurora가 지원하는 호환 API는?
- Compute와 Storage가 어떻게 분리되는가?
- `3 AZ / 6 copies`는 무엇을 의미하는가?
- Reader를 추가한다고 storage 전체를 별도로 복제하는 그림이 아닌 이유는?
