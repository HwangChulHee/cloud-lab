# u2. ECS EC2 Launch Type vs Fargate

## 1. EC2 Launch Type

```text
ECS Cluster
├─ EC2 Instance
│   ├─ ECS Agent
│   ├─ Task A
│   └─ Task B
└─ EC2 Instance
    ├─ ECS Agent
    └─ Task C
```

사용자가 EC2 instances를 provision하고 유지한다.

강의 핵심:

```text
EC2 생성/용량 관리
OS/instance 운영
ECS Agent 실행
Cluster 등록
→ 사용자 책임이 더 큼
```

ECS는 적절한 instance에 Task를 시작/중지한다.

## 2. Fargate Launch Type

```text
ECS Cluster
    ↓
Fargate
├─ Task A
├─ Task B
└─ Task C
```

EC2 instance를 직접 만들지 않는다.

사용자는 Task Definition에서 필요한 CPU/RAM을 지정하고 AWS가 해당 Task를 실행한다.

## 3. Scaling 차이

EC2 Launch Type에서는 두 종류의 scaling을 구분해야 한다.

```text
ECS Service Scaling
→ Task 개수 증가/감소

EC2 Auto Scaling
→ Task를 담을 EC2 capacity 증가/감소
```

반면 Fargate에서는 EC2 capacity를 직접 관리할 필요가 없기 때문에 Task 수 확장이 더 단순하다.

## SAA 판단

```text
underlying instances 직접 관리/제어
→ ECS EC2

serverless containers
→ ECS Fargate

Task scaling과 EC2 scaling을 구분하라
→ 시험 핵심
```
