# u6. ECS EventBridge / SQS Integration Patterns

강의에서는 ECS를 항상 "24시간 떠 있는 Web Service"로만 사용하지 않고 Event-driven Task 실행에도 연결한다.

## 1. EventBridge → ECS Task

예:

```text
S3 Object Upload
      ↓ event
EventBridge
      ↓ rule
Run ECS Fargate Task
      ↓
S3 object 처리
      ↓
DynamoDB에 결과 저장
```

Task Role은 S3/DynamoDB 접근 권한을 가진다.

## 2. Schedule → ECS Task

```text
EventBridge Schedule
      ↓
매 1시간
      ↓
ECS Fargate Task
      ↓
Batch Processing
```

항상 떠 있는 Service가 필요 없는 batch workload에 적합한 패턴이다.

## 3. SQS → ECS Worker

```text
Producer
   ↓
SQS Queue
   ↓ poll
ECS Service
├─ Worker Task 1
├─ Worker Task 2
└─ Worker Task 3
```

Queue backlog가 늘면 ECS Worker 수를 늘리는 구조로 확장할 수 있다.

## 4. Stopped Task → EventBridge

강의에서는 ECS Task가 stopped 상태가 되었을 때 EventBridge Event를 받아 SNS 등으로 알림을 보내는 운영 패턴도 소개한다.

```text
ECS Task stopped
      ↓
EventBridge
      ↓
SNS
      ↓
Administrator
```

## SAA 판단

```text
이벤트가 있을 때만 container batch 실행
→ EventBridge + ECS Task

주기적 container batch
→ EventBridge Schedule + ECS Task

Queue worker
→ SQS + ECS Service

Task 종료 감지/알림
→ EventBridge
```
