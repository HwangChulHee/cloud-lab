# u4. Secrets Manager Multi-Region / SAA Selection

Secrets Manager는 secret을 여러 AWS Region에 replicate할 수 있다.

## 구조

```text
Region A
Secrets Manager
MySecret (Primary)
      ↓ replicate
Region B
Secrets Manager
MySecret (Replica)
```

강의에서는 replica secret이 primary와 동기화되며, 필요하면 replica를 standalone secret으로 promote할 수 있다고 설명한다.

## Use Cases

```text
multi-region application
DR strategy
multi-region database
```

## 최종 선택

```text
일반 config / hierarchy / versioning
→ Parameter Store

sensitive secret + automatic rotation
→ Secrets Manager

RDS credential rotation
→ Secrets Manager

multi-region secret replication
→ Secrets Manager
```

## 기억할 문장

> Parameter Store는 configuration 중심, Secrets Manager는 rotation이 필요한 secret 중심으로 구분한다.
