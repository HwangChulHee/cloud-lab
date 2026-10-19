# u3. AWS Secrets Manager / Rotation

AWS Secrets Manager는 **secret 저장과 rotation에 초점을 둔 managed service**다.

## 강의 핵심

```text
secret 저장
KMS encryption
rotation every X days
rotation 시 secret 자동 생성 가능
Lambda 사용
RDS integration
```

## Rotation

```text
Application
   ↓
Secrets Manager
   ↓ scheduled rotation
Lambda
   ↓
새 secret 생성 / DB credential 갱신
```

## RDS Integration

강의에서는 다음 DB와의 integration을 강조한다.

```text
MySQL
PostgreSQL
Aurora
```

## Parameter Store와 비교

```text
Parameter Store
→ config + secret
→ rotation 자체가 핵심 기능은 아님

Secrets Manager
→ secret 전용
→ automatic rotation이 핵심
```

## 기억할 문장

> DB credential처럼 주기적으로 바꿔야 하는 secret은 Secrets Manager의 대표 use case다.
