# u4. EC2 Purchasing Options

## 지도 확인

EC2는 같은 인스턴스라도 어떤 구매 방식을 선택하느냐에 따라 비용과 유연성이 달라진다.

강의에서 핵심 구매 옵션은 다음과 같다.

```text
On-Demand
Reserved Instances
Savings Plans
Spot Instances
Dedicated Hosts
Dedicated Instances
Capacity Reservations
```

시험에서는 할인율 숫자 암기보다 **워크로드 특성과 구매 옵션을 연결하는 것**이 중요하다.

---

## 1. On-Demand

장기 약정 없이 사용한 만큼 지불한다.

적합한 경우:

```text
짧은 기간
사용량 예측 어려움
중단되면 안 되는 workload
초기 테스트 / 신규 서비스
```

비교적 유연하지만 장기적으로 계속 사용하는 경우 가장 저렴한 선택은 아닐 수 있다.

---

## 2. Reserved Instances

1년 또는 3년의 장기 사용을 전제로 할인받는 방식이다.

강의에서는 steady-state workload, 예를 들어 장기간 계속 실행되는 시스템을 대표적인 사용 사례로 든다.

```text
예측 가능한 장기 사용
→ Reserved Instance 고려
```

Convertible Reserved Instance는 일반 Reserved보다 변경 유연성이 더 크다.

---

## 3. Savings Plans

일정 기간 동안 일정 사용 금액을 약정하고 할인을 받는다.

강의 기준으로 인스턴스 크기, OS, tenancy 등에 어느 정도 유연성을 제공한다.

핵심은:

```text
특정 한 VM을 예약한다
```

보다는

```text
장기간 일정 Compute 사용량을 약정한다
```

는 관점으로 구분하는 것이다.

---

## 4. Spot Instances

남는 EC2 capacity를 매우 저렴하게 사용할 수 있지만 인스턴스를 잃을 수 있다.

따라서 interruption에 견딜 수 있는 workload에 적합하다.

```text
Batch Job
Data Analysis
Image Processing
Distributed Workload
Flexible Start/End Time
```

반대로 중요한 DB처럼 중단에 민감한 workload에는 적합하지 않다.

시험에서 Spot의 핵심은:

```text
가장 저렴함
+
중단 가능
```

이다.

---

## 5. Dedicated Host와 Dedicated Instance

### Dedicated Host

물리 서버 전체를 사용자에게 전용으로 제공한다.

주요 이유:

```text
Compliance
BYOL / 복잡한 라이선스
물리 서버 수준 제어
```

### Dedicated Instance

전용 하드웨어에서 실행되지만 Dedicated Host처럼 물리 서버 배치를 직접 제어하는 개념은 아니다.

---

## 6. Capacity Reservation

특정 Availability Zone의 EC2 capacity를 확보한다.

핵심 목적은 할인보다는:

```text
필요할 때 인스턴스를 실제로 띄울 capacity 보장
```

이다.

가격 할인과 capacity 확보를 같은 개념으로 혼동하지 않는다.

---

## SAA 판단표

| 요구사항 | 우선 떠올릴 옵션 |
|---|---|
| 짧고 예측 어려운 workload | On-Demand |
| 안정적인 장기 workload | Reserved / Savings Plans |
| 중단 가능, 비용 최소화 | Spot |
| 라이선스/규제/물리 서버 제어 | Dedicated Host |
| 전용 하드웨어 | Dedicated Instance |
| 특정 AZ capacity 확보 | Capacity Reservation |

이번 유닛은 SAA에서 선택 문제가 자주 나오므로 강의를 들은 뒤 위 표를 보지 않고 각 옵션을 설명할 수 있으면 충분하다.
