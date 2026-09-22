# u1. EC2 Purchasing Options

강의에서는 workload 성격에 따라 EC2 구매 옵션을 구분한다.

```text
On-Demand
→ short / unpredictable / no commitment

Reserved Instances
→ steady-state long-running workload

Savings Plans
→ 1년/3년 사용 commitment 기반 할인

Spot
→ interruption을 허용하는 flexible workload

Dedicated Host
→ compliance / BYOL / physical host control

Capacity Reservation
→ 특정 AZ capacity 확보
→ 할인 자체가 목적은 아님
```

## Spot 대표 use case

```text
Batch
Data Analysis
Image Processing
Distributed Workload
Flexible Start/End
```

critical database처럼 interruption을 허용하기 어려운 workload와는 맞지 않는다.

## 기억할 문장

> 비용 최적화는 On-Demand를 무조건 피하는 것이 아니라 workload의 예측 가능성과 interruption 허용 여부에 맞춰 구매 옵션을 선택하는 것이다.
