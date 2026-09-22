# 27. Amazon MQ / Integration 선택 기준

SAA 강의의 Messaging / Integration 마지막 정리 단원이다.

Amazon MQ는 SQS/SNS처럼 AWS 전용 API를 중심으로 설계된 cloud-native messaging과 달리, **기존 애플리케이션이 사용하던 메시지 브로커 프로토콜을 유지하면서 AWS로 옮겨야 할 때** 선택하는 관리형 메시지 브로커다.

> 강의 핵심: 기존 on-premises 애플리케이션이 MQTT, AMQP, STOMP, OpenWire, WSS 같은 프로토콜을 사용하고 있다면, SQS/SNS로 재설계하지 않고 Amazon MQ를 고려한다.

## Units

- [ ] [u1. 왜 Amazon MQ가 필요한가](./u1_why_amazon_mq/README.md)
- [ ] [u2. Queue / Topic / Broker 구조](./u2_broker_queue_topic/README.md)
- [ ] [u3. High Availability / Failover](./u3_high_availability/README.md)
- [ ] [u4. Messaging 서비스 최종 선택 지도](./u4_integration_selection/README.md)

## 핵심 구조

```text
기존 Application
MQTT / AMQP / STOMP / OpenWire / WSS
          │
          ▼
    Amazon MQ Broker
      ├─ Queue
      └─ Topic
```

## Amazon MQ를 먼저 떠올리는 상황

```text
기존 애플리케이션이 표준/open messaging protocol 사용
→ Amazon MQ

기존 브로커 기반 애플리케이션을 최소 변경으로 AWS 이전
→ Amazon MQ

AWS-native 신규 시스템
→ 우선 SQS / SNS / EventBridge / Kinesis 검토
```

## 중요한 trade-off

강의에서는 Amazon MQ가 SQS/SNS만큼 크게 자동 확장되는 서비스는 아니라는 점을 강조한다.

```text
Amazon MQ
→ broker/server 기반
→ 기존 protocol 호환성이 장점
→ Multi-AZ failover 가능

SQS / SNS
→ AWS cloud-native
→ 대규모 확장과 관리 부담 최소화에 강점
```

## 최종 목표

이 단원을 끝내면 문제를 보고 다음을 구분할 수 있어야 한다.

```text
작업 Queue
→ SQS

Pub/Sub Fan-Out
→ SNS

Event routing / schedule / AWS events
→ EventBridge

실시간 stream + replay
→ Kinesis Data Streams

관리형 streaming destination delivery
→ Amazon Data Firehose

기존 message broker protocol 호환
→ Amazon MQ
```
