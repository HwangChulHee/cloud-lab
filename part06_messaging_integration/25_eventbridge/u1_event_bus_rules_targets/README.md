# u1. Event Bus / Rules / Targets

## Event Bus

EventBridge Event Bus는 source에서 들어온 event를 받아 rule 평가 대상으로 전달한다.

강의에서는 세 종류를 구분한다.

```text
Default Event Bus
→ AWS Services

Partner Event Bus
→ AWS SaaS Partners

Custom Event Bus
→ Custom Apps
```

## Rule

Rule은 event가 어떤 조건일 때 어떤 target으로 보낼지 정의한다.

```text
Event
  ↓
Rule
  ↓ match
Target
```

## Target

강의에서 예시로 다음 target들을 보여준다.

```text
Lambda
AWS Batch
ECS Task
SQS
SNS
Kinesis Data Streams
Step Functions
CodePipeline
CodeBuild
SSM
EC2 Actions
```

즉 EventBridge는 compute, integration, orchestration, maintenance 계층으로 event를 routing할 수 있다.

## 예시

```text
EC2 State Change
      ↓
EventBridge
      ↓ rule
SNS
      ↓
Administrator Notification
```

## 기억할 문장

> Event Bus가 이벤트를 받고, Rule이 이벤트를 고르고, Target이 실제 후속 작업을 수행한다.
