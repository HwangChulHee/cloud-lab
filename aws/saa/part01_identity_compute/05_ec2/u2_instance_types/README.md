# u2. EC2 Instance Types

## 지도 확인

EC2 인스턴스는 모두 같은 성능을 가지지 않는다. 워크로드에 따라 CPU, Memory, Storage, Network 특성이 다른 인스턴스 타입을 선택한다.

강의에서는 인스턴스 이름을 다음처럼 읽는다.

```text
m5.2xlarge
│ │ └── size
│ └──── generation
└────── instance class
```

---

## 1. General Purpose

Compute, Memory, Network가 비교적 균형 잡혀 있다.

```text
웹 서버
코드 저장소
일반 애플리케이션 서버
```

처럼 한 자원만 극단적으로 많이 필요하지 않은 워크로드에 적합하다.

---

## 2. Compute Optimized

CPU 성능이 중요한 워크로드에 적합하다.

예:

```text
고성능 웹 서버
Batch Processing
Media Transcoding
High Performance Computing
Machine Learning
Gaming Server
```

핵심은 CPU-bound workload인지 판단하는 것이다.

---

## 3. Memory Optimized

큰 메모리 공간에서 많은 데이터를 처리해야 하는 워크로드에 적합하다.

예:

```text
In-memory Database
Distributed Cache
Real-time Big Data Processing
```

---

## 4. Storage Optimized

로컬 스토리지에 매우 높은 IOPS 또는 순차적 읽기/쓰기가 필요한 워크로드를 위한 계열이다.

예:

```text
OLTP
NoSQL Database
Data Warehouse
Distributed File System
```

---

## 선택 기준

인스턴스 이름 자체를 외우기보다 먼저 병목이 어디인지 판단한다.

```text
CPU 병목      → Compute Optimized
Memory 병목   → Memory Optimized
Storage I/O   → Storage Optimized
균형형        → General Purpose
```

실제 제품군과 세대는 계속 바뀔 수 있으므로 시험에서도 기본적으로 workload 특성과 category의 대응을 이해하는 것이 중요하다.

---

## SAA 연결

예를 들어 대규모 계산 작업인데 Memory Optimized를 고르는 식으로 서비스 이름만 보고 선택하지 않는다.

문제에서 다음 단어를 찾는다.

```text
CPU intensive
in-memory
high IOPS
balanced workload
```

이 키워드가 인스턴스 타입 선택의 단서가 된다.

이번 유닛은 분류 개념이라 별도 유제와 3문장 요약은 생략한다.
