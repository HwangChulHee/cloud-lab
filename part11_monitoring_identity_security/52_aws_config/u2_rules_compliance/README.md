# u2. Config Rules / Compliance

Config Rule은 AWS resource가 원하는 기준을 만족하는지 평가한다.

## Managed Rules

AWS가 미리 제공하는 rule을 사용할 수 있다.

강의 예시:

```text
EBS disk type이 gp2인가?
EC2 instance가 t2.micro인가?
Security Group이 원하는 기준을 만족하는가?
```

## Custom Rules

강의에서는 custom Config Rule을 **AWS Lambda**로 정의할 수 있다고 설명한다.

## Evaluation Trigger

```text
Configuration Change 발생 시
또는
정기적인 시간 간격
```

으로 평가할 수 있다.

## 상태

```text
COMPLIANT
→ rule 만족

NON_COMPLIANT
→ rule 위반
```

## 매우 중요한 점

```text
AWS Config Rule
≠ preventive control
```

잘못된 resource creation을 미리 차단하는 서비스가 아니다.

```text
작업 발생
→ Config가 기록
→ Rule 평가
→ NON_COMPLIANT 탐지
```

## SAA 판단

```text
resource configuration이 정책을 준수하는지 지속 평가
→ AWS Config Rules
```
