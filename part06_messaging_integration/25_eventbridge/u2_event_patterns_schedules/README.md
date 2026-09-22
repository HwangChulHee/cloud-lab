# u2. Event Pattern / Schedule

EventBridge Rule은 크게 **Event Pattern**과 **Schedule** 두 방식으로 생각한다.

## Event Pattern

AWS 서비스에서 어떤 일이 발생했을 때 반응한다.

강의 예시:

```text
EC2 Instance 시작/상태 변경
CodeBuild failed build
S3 object upload
Trusted Advisor finding
CloudTrail API call
```

JSON event의 field를 기준으로 filtering할 수 있다.

```text
Event
  ↓
Event Pattern
  ↓ match
Target
```

S3를 EventBridge와 연결하면 object metadata, size, name 같은 조건을 이용한 advanced filtering도 가능하다고 강의에서 설명한다.

## Schedule

정해진 시간에 rule을 실행한다.

강의 예시:

```text
every hour
cron schedule
every 4 hours
```

대표 구조:

```text
EventBridge Schedule
      ↓
Lambda / ECS Task
      ↓
Periodic Job
```

강의에서는 ECS Fargate task를 매 시간 실행하는 예도 보여준다.

## 기억할 문장

> Event Pattern은 "무슨 일이 발생했을 때", Schedule은 "언제 실행할지"를 정의한다.
