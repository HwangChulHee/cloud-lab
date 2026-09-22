# 25. Amazon EventBridge

Amazon EventBridge는 **AWS 서비스, SaaS, custom application에서 발생한 이벤트를 rule로 필터링하고 target으로 routing하는 event bus 서비스**다.

첨부 SAA 강의에서는 EventBridge를 기존 CloudWatch Events의 확장 개념으로 설명하고, Schedule / Event Pattern / Event Bus / Archive & Replay / Schema Registry / Resource-based Policy를 핵심으로 다룬다.

## Units

- [x] [u1. Event Bus / Rules / Targets](./u1_event_bus_rules_targets/README.md)
- [x] [u2. Event Pattern / Schedule](./u2_event_patterns_schedules/README.md)
- [x] [u3. CloudTrail / Cross-Account Integration](./u3_cloudtrail_cross_account/README.md)
- [x] [u4. Archive / Replay / Schema Registry](./u4_archive_replay_schema/README.md)
- [x] [u5. SAA Selection / SQS·SNS·Kinesis 비교](./u5_saa_selection/README.md)

## 기본 구조

```text
Event Source
   ↓
EventBridge Event Bus
   ↓ Rule / Filter
Target
├─ Lambda
├─ SQS
├─ SNS
├─ Kinesis Data Streams
├─ Step Functions
├─ ECS Task
├─ CodeBuild / CodePipeline
└─ SSM / EC2 Actions
```

## Event Bus 종류

```text
Default Event Bus
→ AWS 서비스 이벤트

Partner Event Bus
→ AWS SaaS Partner 이벤트

Custom Event Bus
→ 직접 만든 application 이벤트
```

## 핵심 감각

```text
SQS
→ Queue에 작업을 쌓음

SNS
→ 하나의 메시지를 여러 subscriber에 push

EventBridge
→ 이벤트 내용을 rule로 보고 적절한 target으로 routing

Kinesis
→ 지속적으로 들어오는 stream data 저장/처리
```

## 기억할 문장

> EventBridge는 이벤트를 저장하는 queue가 아니라, event source와 target 사이에서 JSON event를 rule로 분류하고 routing하는 event bus다.
