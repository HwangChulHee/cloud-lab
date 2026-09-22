# u3. CloudTrail / Cross-Account Integration

## CloudTrail API Call 감지

EventBridge는 CloudTrail에 기록되는 AWS API call을 event source로 사용할 수 있다.

강의 예시:

```text
User
  ↓ DeleteTable API Call
DynamoDB
  ↓ API 기록
CloudTrail
  ↓
EventBridge
  ↓
SNS
  ↓
Alert
```

즉 특정 관리 API가 호출되었을 때 후속 알림이나 자동화 작업을 실행할 수 있다.

## Resource-based Policy

Event Bus에는 resource-based policy를 설정할 수 있다.

강의 핵심:

```text
다른 AWS Account에서 PutEvents 허용/거부
다른 Region의 event 허용/거부
```

대표 use case:

```text
Account A ─┐
Account B ─┼→ Central Event Bus
Account C ─┘
```

AWS Organization의 여러 계정 이벤트를 하나의 중앙 계정/Region으로 모으는 구조를 만들 수 있다.

## 기억할 문장

> CloudTrail은 API 행위를 기록하고, EventBridge는 그 API event를 받아 후속 자동화로 routing할 수 있다.
