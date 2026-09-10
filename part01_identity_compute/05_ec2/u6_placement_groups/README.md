# u6. EC2 Placement Groups

## 지도 확인

Placement Group은 EC2 인스턴스를 AWS의 물리 인프라에 **어떤 방식으로 배치할지 제어하는 전략**이다.

강의에서는 세 가지 전략을 구분한다.

```text
Cluster
Spread
Partition
```

이번 단원은 별도 구축보다 **세 전략의 목적과 선택 기준을 구분하는 것**이 핵심이다.

---

## 1. Cluster Placement Group

인스턴스를 **하나의 Availability Zone 안에서 서로 가깝게** 배치한다.

```text
Same AZ

EC2  EC2  EC2
 \    |    /
  Cluster
```

강의에서 강조하는 장점은 낮은 latency와 높은 network throughput이다.
Enhanced Networking과 함께 사용할 때 높은 네트워크 성능이 필요한 워크로드에 적합하다고 설명한다.

반대로 같은 AZ에 밀집하므로 AZ 장애가 발생하면 그룹 전체가 동시에 영향을 받을 수 있다.

### 대표 사용 사례

- Big Data 작업
- 매우 낮은 latency가 필요한 애플리케이션
- 인스턴스 간 높은 network throughput이 필요한 워크로드

### SAA 키워드

```text
low latency
high network throughput
same AZ
```

→ **Cluster**

---

## 2. Spread Placement Group

인스턴스를 **서로 다른 물리 하드웨어에 분산**한다.

목적은 한 하드웨어 장애가 여러 중요 인스턴스에 동시에 영향을 주는 위험을 낮추는 것이다.

Spread Placement Group은 여러 Availability Zone에 걸쳐 사용할 수 있다.
강의 기준으로 **placement group 하나당 AZ별 최대 7개 인스턴스** 제한이 있다는 점을 함께 기억한다.

```text
AZ-A
EC2 → Hardware 1
EC2 → Hardware 2

AZ-B
EC2 → Hardware 3
EC2 → Hardware 4
```

### 대표 사용 사례

- 높은 가용성이 중요한 애플리케이션
- 각 인스턴스를 서로 장애로부터 강하게 격리하고 싶은 경우
- 소수의 중요 인스턴스

### SAA 키워드

```text
critical instances
different hardware
reduce simultaneous failure
small number of instances
```

→ **Spread**

---

## 3. Partition Placement Group

인스턴스를 여러 **Partition**으로 나누고, 각 Partition이 서로 다른 rack 집합을 사용하도록 배치한다.

```text
Partition A
├── EC2
├── EC2

Partition B
├── EC2
├── EC2

Partition C
├── EC2
└── EC2
```

한 rack 집합에 문제가 생기더라도 다른 Partition으로 장애가 번지는 위험을 줄이는 것이 목적이다.

강의에서는 하나의 placement group에 **수백 개 규모의 EC2 인스턴스**까지 확장할 수 있는 전략으로 설명한다.

### 대표 사용 사례

- Hadoop
- Cassandra
- Kafka
- 대규모 분산 시스템

### SAA 키워드

```text
large distributed system
rack isolation
hundreds of instances
Hadoop / Cassandra / Kafka
```

→ **Partition**

---

## 한 번에 비교하기

| 전략 | 우선하는 것 | 배치 특징 | 대표 상황 |
|---|---|---|---|
| Cluster | 성능 | 같은 AZ에 가깝게 배치 | 낮은 latency, 높은 throughput |
| Spread | 개별 인스턴스 장애 격리 | 서로 다른 물리 하드웨어 | 소수의 중요 서버 |
| Partition | 대규모 장애 격리 | rack 집합 단위로 분리 | Hadoop, Cassandra, Kafka |

---

## SAA 판단

```text
최고 수준의 인스턴스 간 네트워크 성능
→ Cluster

소수의 중요한 EC2를 서로 다른 물리 서버에 배치
→ Spread

수백 개 EC2로 구성된 분산 시스템에서 rack 장애 격리
→ Partition
```

특히 다음 두 개를 헷갈리지 않는다.

```text
Spread
→ 인스턴스 하나하나를 서로 다른 하드웨어에 분산
→ 소수의 중요한 인스턴스

Partition
→ 여러 인스턴스를 Partition 단위로 묶어 rack 집합을 분리
→ 대규모 분산 시스템
```

이번 단원은 Coverage 성격이 강하므로 별도 Hands-on, 유제, 3문장 요약은 생략한다.
