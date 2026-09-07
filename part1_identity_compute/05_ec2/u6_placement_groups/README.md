# u6. EC2 Placement Groups

## 지도 확인

Placement Group은 EC2 인스턴스의 물리적 배치 전략을 제어하는 기능이다.

강의에서는 세 가지 전략을 구분한다.

```text
Cluster
Spread
Partition
```

핵심은 성능, 장애 격리, 대규모 분산 배치 중 무엇을 우선하는지 판단하는 것이다.

---

## 1. Cluster Placement Group

인스턴스를 하나의 Availability Zone 안에서 서로 가까이 배치한다.

장점:

```text
낮은 지연시간
높은 네트워크 처리량
```

단점:

```text
같은 AZ에 집중
→ AZ 장애 시 함께 영향
```

사용 사례:

```text
Big Data
HPC
초저지연 네트워크가 중요한 workload
```

---

## 2. Spread Placement Group

인스턴스를 서로 다른 물리 하드웨어에 분산한다.

목표는 개별 하드웨어 장애가 여러 인스턴스에 동시에 영향을 주는 위험을 줄이는 것이다.

강의에서는 AZ별 그룹당 인스턴스 수 제한이 있다는 점도 설명한다.

사용 사례는 소수의 매우 중요한 인스턴스를 강하게 분리하고 싶을 때다.

---

## 3. Partition Placement Group

인스턴스를 여러 Partition으로 나누고, 각 Partition은 서로 다른 rack 집합을 사용하도록 분산한다.

```text
Partition A
├── EC2
├── EC2

Partition B
├── EC2
├── EC2
```

대규모 분산 시스템에서 특정 rack 장애가 전체 클러스터로 번지는 위험을 줄이는 데 사용한다.

강의에서 예로 드는 workload:

```text
Hadoop
Cassandra
Kafka
```

---

## SAA 판단

```text
최고 네트워크 성능 / 낮은 latency
→ Cluster

소수 중요 인스턴스의 하드웨어 장애 격리
→ Spread

대규모 분산 시스템의 rack 단위 장애 격리
→ Partition
```

이번 유닛은 선택 패턴만 명확히 구분하면 되므로 별도 유제와 3문장 요약은 생략한다.
