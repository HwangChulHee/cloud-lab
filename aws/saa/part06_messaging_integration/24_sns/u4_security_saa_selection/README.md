# u4. SNS Security & SAA Selection

## 1. 접근 제어

SNS 접근은 IAM Policy와 Topic Policy 같은 권한 계층을 함께 고려한다.

개념적으로:

```text
Publisher Role
→ sns:Publish

Subscriber 관련 권한
→ Topic/Subscription 정책에 따라 제어
```

다른 AWS 서비스나 Account와 연동할 때 Resource Policy가 중요해질 수 있다.

## 2. Encryption

SNS도 전송/저장 데이터 보호 관점에서 HTTPS와 KMS 기반 암호화를 함께 고려한다.

SAA에서는 세부 암호화 API보다 **메시징 서비스도 IAM/KMS와 통합된다**는 선택 기준을 기억한다.

## 3. SAA 선택 지도

```text
한 이벤트 → 여러 Consumer
→ SNS

Email/SMS/Lambda/SQS 등 여러 destination으로 push
→ SNS

각 Consumer에 durable buffer 필요
→ SNS + SQS

특정 구독자에게 필요한 이벤트만
→ SNS Filter Policy

한 Worker pool이 작업을 경쟁 소비
→ SNS보다 SQS

실시간 event stream 보관/replay
→ SNS보다 Kinesis Data Streams
```

## 면접용 설명

> SNS는 Topic 기반 Pub/Sub 서비스로 Publisher가 한 번 publish한 이벤트를 여러 Subscriber에게 push할 때 사용합니다. Consumer별로 버퍼와 독립 재처리가 필요하면 SNS 뒤에 SQS를 붙여 fan-out 구조를 만드는 것이 일반적입니다.
