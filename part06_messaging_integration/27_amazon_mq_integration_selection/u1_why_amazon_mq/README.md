# u1. 왜 Amazon MQ가 필요한가

## 1. SQS/SNS는 AWS-native

SQS와 SNS는 AWS에서 제공하는 cloud-native messaging 서비스다.

신규 시스템이라면 관리 부담이 적고 AWS 서비스와 잘 통합되기 때문에 매우 좋은 선택이 될 수 있다.

하지만 기존 시스템이 이미 다른 메시지 브로커 프로토콜에 강하게 의존하고 있다면 이야기가 달라진다.

## 2. 기존 애플리케이션의 문제

강의에서 예로 드는 프로토콜:

```text
MQTT
AMQP
STOMP
OpenWire
WSS
```

기존 on-premises 애플리케이션:

```text
Application
   │ AMQP / STOMP / ...
   ▼
Traditional Message Broker
```

이 애플리케이션을 SQS/SNS로 옮기려면 messaging API와 동작 방식을 다시 설계해야 할 수 있다.

## 3. Amazon MQ의 역할

```text
기존 Application
   │ 기존 protocol 유지
   ▼
Amazon MQ
```

핵심은 **re-platform/re-host 성격의 migration에서 application re-engineering을 줄이는 것**이다.

## 4. 언제 SQS/SNS가 더 자연스러운가?

신규 cloud-native 시스템이라면 보통 기존 protocol compatibility보다 다음이 더 중요할 수 있다.

```text
높은 확장성
server 관리 최소화
AWS 서비스와 간단한 통합
Queue / Pub-Sub 목적 분리
```

이 경우 SQS/SNS가 더 자연스러운 선택이 될 수 있다.

## SAA 판단

```text
"existing application"
"on-premises message broker"
"AMQP / MQTT / STOMP"
"minimal application changes"
→ Amazon MQ
```

반대로:

```text
"new cloud-native application"
"massive scale"
"fully managed queue"
→ SQS / SNS 쪽부터 검토
```
