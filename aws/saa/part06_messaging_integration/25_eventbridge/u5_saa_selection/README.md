# u5. EventBridge SAA Selection

## EventBridge를 선택하는 경우

```text
AWS service event에 반응
→ EventBridge

JSON event field로 advanced filtering
→ EventBridge Rule

정기 실행
→ EventBridge Schedule

여러 Account의 event 중앙 수집
→ EventBridge + Resource-based Policy

과거 event 재처리
→ Archive + Replay

CloudTrail API call 발생 시 자동 대응
→ CloudTrail + EventBridge
```

## SQS / SNS / EventBridge / Kinesis 비교

```text
SQS
→ queue / buffering / worker decoupling
→ consumer가 message를 가져가 처리

SNS
→ pub-sub / fan-out
→ 하나의 message를 여러 subscriber에 push

EventBridge
→ event bus / content-based routing
→ source event를 rule로 분류해 target으로 전달

Kinesis Data Streams
→ continuous streaming data
→ retention / replay / multiple stream consumers
```

## 대표 문제

```text
주문 처리 worker가 밀림
→ SQS

주문 이벤트를 결제/배송/분석에 모두 전달
→ SNS + 각 SQS

EC2 state change가 발생하면 Lambda 실행
→ EventBridge

매 시간 ECS Fargate batch task 실행
→ EventBridge Schedule

CloudTrail DeleteTable API 감지 후 관리자 알림
→ EventBridge + SNS

초당 수많은 click event를 계속 저장하고 다시 읽음
→ Kinesis Data Streams
```

## 기억할 문장

> EventBridge의 핵심 키워드는 event routing, rule, filtering, schedule, archive/replay다.
