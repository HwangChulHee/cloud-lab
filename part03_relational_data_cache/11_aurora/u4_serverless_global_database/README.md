# u4. Aurora Serverless & Global Database

## 지도 확인

Aurora에는 일반 provisioned cluster 외에도 workload 패턴과 글로벌 요구사항에 맞춘 확장 옵션이 있다.

```text
예측하기 어려운 / 간헐적 workload
→ Aurora Serverless

여러 Region의 read latency 감소 + DR
→ Aurora Global Database
```

---

## 1. Aurora Serverless

강의에서는 Aurora Serverless를 **예측하기 어렵거나 간헐적인 workload에 적합하고 capacity planning 부담을 줄이는 옵션**으로 설명한다.

예:

```text
사내 관리 시스템
평소 사용 적음
월말에만 급증
```

이런 경우 항상 큰 DB Instance를 provision해 둘 필요를 줄이는 방향으로 생각할 수 있다.

핵심은:

```text
workload가 일정하고 예측 가능
→ Provisioned Aurora

workload가 간헐적 / 변동 폭 큼
→ Aurora Serverless 고려
```

---

## 2. Aurora Global Database

Aurora Global Database는 여러 Region에 Aurora cluster를 구성하는 기능이다.

강의의 그림:

```text
Primary Region
Read / Write
      │
      │ storage replication
      ▼
Secondary Region
Read Only
```

Primary Region은 쓰기를 담당하고 Secondary Region은 읽기 전용으로 사용할 수 있다.

---

## 3. 왜 Global Database를 쓰는가

대표 목적은 두 가지다.

```text
1. 글로벌 사용자 read latency 감소
2. Region 장애를 고려한 DR
```

사용자가 유럽에 있는데 DB가 서울에만 있다면 모든 읽기 요청이 서울까지 와야 한다.

Global Database를 사용하면 가까운 Secondary Region에서 read workload를 처리하는 구조를 만들 수 있다.

---

## 4. Cross-Region Read Replica와 비교

강의에는 Aurora Cross-Region Read Replica와 Global Database가 모두 등장한다.

```text
Cross-Region Read Replica
→ 다른 Region에 read replica
→ DR에도 활용 가능

Aurora Global Database
→ Aurora의 글로벌 전용 구조
→ Primary Region + Secondary Regions
→ 낮은 cross-region replication lag를 목표
→ 글로벌 read + DR에 적합
```

강의는 Global Database를 권장 옵션으로 제시한다.

---

## 5. 시험에서 숫자보다 구조를 먼저 기억

강의에는 Global Database의 secondary region 수, 각 region의 reader 수, replication lag, failover RTO 같은 수치도 나온다.

시험 준비에서는 먼저 다음 구조를 확실히 기억한다.

```text
1 Primary Region
→ read/write

Secondary Regions
→ read-only

Storage-level cross-region replication
→ low-latency global reads
→ DR
```

---

## SAA 판단

```text
예측하기 어려운 간헐적 Aurora workload
→ Aurora Serverless

세계 여러 지역에서 빠르게 읽고 싶다
→ Aurora Global Database

Region 장애에 대비한 Aurora DR
→ Aurora Global Database
```

## Recall Check

- Aurora Serverless는 어떤 workload에 적합한가?
- Global Database의 Primary / Secondary 역할은?
- Global Database가 read latency를 줄이는 이유는?
- Cross-Region Read Replica와 Global Database의 공통점과 차이는?
