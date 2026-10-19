# u1. ECS Cluster / Task / Service

## 1. Cluster

ECS Cluster는 ECS workload가 실행되는 논리적 묶음이다.

```text
ECS Cluster
├─ Task A
├─ Task B
└─ Task C
```

EC2 Launch Type에서는 Cluster 안에 ECS Agent가 실행되는 EC2 instances가 등록된다.

Fargate에서는 EC2 host를 직접 관리하지 않는다.

## 2. Task Definition

Task Definition은 Container를 어떻게 실행할지 정의하는 설계도다.

개념적으로 다음 정보를 포함한다.

```text
어떤 container image?
CPU / Memory는?
어떤 port?
환경 변수는?
어떤 IAM Role?
어떤 volume?
```

## 3. Task

Task Definition을 실제로 실행한 단위가 ECS Task다.

```text
Task Definition
     ↓ run
ECS Task
     ↓
Container(s)
```

## 4. Service

Service는 원하는 개수의 Task를 계속 유지하는 역할을 한다.

```text
Desired Count = 3

ECS Service
├─ Task 1
├─ Task 2
└─ Task 3
```

Task 하나가 종료되면 Service는 desired count를 맞추기 위해 replacement Task를 시작할 수 있다.

## 5. Service와 one-off Task 구분

```text
지속적으로 떠 있어야 하는 Web/API
→ ECS Service

한 번 실행하고 끝나는 batch job
→ ECS Task 직접 실행 가능
```

## 기억할 문장

> Task Definition은 설계도, Task는 실행 인스턴스, Service는 원하는 Task 수를 유지하는 컨트롤러다.
