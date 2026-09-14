# u2. Writer, Reader & Aurora Replicas

## 지도 확인

Aurora Cluster에서는 쓰기와 읽기의 진입점을 구분해서 보는 것이 중요하다.

```text
Write
Application
   ↓
Writer Endpoint
   ↓
Writer Instance

Read
Application
   ↓
Reader Endpoint
   ↓
Aurora Replicas
```

---

## 1. Writer Endpoint

Writer Endpoint는 현재 **Writer DB Instance**로 연결되는 cluster endpoint다.

```text
INSERT
UPDATE
DELETE
→ Writer Endpoint
→ Writer Instance
```

애플리케이션은 특정 Writer Instance의 주소를 직접 기억하기보다 Writer Endpoint를 사용한다.

이렇게 해야 failover로 Writer가 바뀌더라도 애플리케이션의 연결 대상 개념을 유지하기 쉽다.

---

## 2. Reader Endpoint

Reader Endpoint는 읽기 전용 Replica 쪽으로 연결하기 위한 endpoint다.

```text
SELECT
→ Reader Endpoint
→ Reader 1 / Reader 2 / ...
```

강의의 핵심은 **Reader Endpoint가 read workload를 여러 Reader에 분산하는 진입점**이라는 점이다.

RDS Read Replica와 비교하면:

```text
일반 RDS Read Replica
→ 각 Replica endpoint를 앱이 직접 선택하는 경우가 많음

Aurora
→ Reader Endpoint를 통해 Reader 계층으로 접근
```

---

## 3. Aurora Replicas

Aurora는 여러 Read Replica를 둘 수 있다.

```text
Writer
  │
  ├─ Reader 1
  ├─ Reader 2
  └─ Reader N
```

Read Replica를 여러 AZ에 둘 수 있고, 읽기 부하를 분산하는 데 사용한다.

강의에서는 Aurora compute 계층에서 Read Replica Auto Scaling도 다룬다.

---

## 4. Read Replica Auto Scaling

읽기 부하가 증가하면 Reader Instance 수를 늘리는 구조를 사용할 수 있다.

```text
Read traffic 증가
      ↓
Aurora Replica Auto Scaling
      ↓
Reader 추가
      ↓
Reader Endpoint를 통한 분산
```

여기서 중요한 건 **Storage 자체를 scale-out하는 것과 Reader compute를 scale-out하는 것이 다른 문제**라는 점이다.

---

## 5. Custom Endpoint

강의에서는 Aurora cluster가 Writer / Reader endpoint 외에도 custom endpoint를 사용할 수 있다고 설명한다.

예를 들어 일부 고성능 Reader만 분석 쿼리에 사용하고 싶다면:

```text
Reporting App
   ↓
Custom Endpoint
   ↓
Large Reader Instances
```

처럼 특정 DB Instance 그룹을 대상으로 endpoint를 만들 수 있다.

---

## SAA 판단

```text
쓰기 요청
→ Writer Endpoint

읽기 요청을 여러 Aurora Replica로 분산
→ Reader Endpoint

특정 Reader 그룹만 별도 workload에 사용
→ Custom Endpoint

읽기 부하가 계속 증가
→ Aurora Replica Auto Scaling 고려
```

## Recall Check

- Writer Endpoint는 어디로 연결되는가?
- Reader Endpoint는 무엇을 해결하는가?
- RDS Read Replica와 Aurora Reader Endpoint의 사용 경험은 어떻게 다른가?
- Reader Auto Scaling과 Storage Auto Scaling은 같은 개념인가?
