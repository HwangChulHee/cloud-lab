# u3. Amazon MQ High Availability / Failover

강의에서는 Amazon MQ가 server/broker 기반이며 **Multi-AZ failover 구성**을 할 수 있다고 설명한다.

## 구조

```text
Region
├─ AZ-A
│   └─ Amazon MQ Broker
│      ACTIVE
│
└─ AZ-B
    └─ Amazon MQ Broker
       STANDBY

        shared storage
             │
             ▼
            EFS
```

장애가 발생하면 Client가 standby broker로 failover할 수 있는 형태다.

## 왜 중요한가?

Amazon MQ는 SQS/SNS처럼 "서버가 보이지 않는 무한 확장 메시징" 관점보다 **broker instance의 availability**를 고려해야 한다.

따라서 다음을 분리한다.

```text
확장성
→ SQS/SNS가 강함

기존 protocol 호환
→ Amazon MQ

Broker 장애 대응
→ Multi-AZ / failover 구성
```

## SAA 판단

```text
Amazon MQ + HA
→ Active / Standby Multi-AZ

기존 메시지 브로커 migration
+ 장애 대응 필요
→ Amazon MQ HA 구성 고려
```

## 주의

Multi-AZ는 "무한 확장"을 의미하지 않는다.

```text
High Availability
≠
Unlimited Scalability
```

시험에서 이 두 개념을 섞지 않는다.
