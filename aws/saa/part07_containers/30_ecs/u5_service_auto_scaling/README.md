# u5. ECS Service Auto Scaling

ECS Service Auto Scaling은 **원하는 ECS Task 수를 자동으로 증가/감소**시킨다.

```text
CloudWatch Metric
      ↓
Scaling Policy
      ↓
ECS Service
Desired Count 2 → 4
      ↓
새 Task 시작
```

## 강의에서 다루는 대표 Metric

```text
ECS Service Average CPU Utilization
ECS Service Average Memory Utilization
ALB Request Count Per Target
```

## Scaling 방식

### Target Tracking

특정 metric을 목표값 근처로 유지한다.

```text
CPU Target = 50%
→ 높아지면 scale out
→ 낮아지면 scale in
```

### Step Scaling

CloudWatch Alarm 임계값 구간에 따라 정해진 크기로 확장/축소한다.

### Scheduled Scaling

예측 가능한 시간대에 Task 수를 미리 조정한다.

## 가장 중요한 구분

```text
ECS Service Auto Scaling
→ Task 개수

EC2 Auto Scaling
→ ECS Cluster의 EC2 instance 개수
```

둘은 같은 것이 아니다.

Fargate에서는 EC2 instance capacity를 직접 관리하지 않으므로 Service Auto Scaling 구성이 더 단순해진다.

## SAA 판단

```text
ECS application CPU가 증가
→ ECS Service Auto Scaling

EC2 Launch Type에서 Task를 놓을 host capacity 부족
→ EC2/Capacity Provider 측 scaling도 고려
```
