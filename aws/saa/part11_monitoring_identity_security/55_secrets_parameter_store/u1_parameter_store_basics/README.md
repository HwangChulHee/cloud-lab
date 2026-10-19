# u1. SSM Parameter Store 기본 구조

SSM Parameter Store는 **configuration과 secrets를 안전하게 저장**하는 서비스다.

## 특징

강의에서 다음을 강조한다.

```text
secure storage
optional KMS encryption
serverless
scalable
durable
easy SDK
version tracking
IAM security
EventBridge notifications
CloudFormation integration
```

## Plaintext / Encrypted

```text
Application
   ↓ GetParameter
Parameter Store
   ├→ Plaintext configuration
   └→ Encrypted configuration
          ↓
         KMS
```

암호화된 parameter를 읽으려면 IAM뿐 아니라 필요한 KMS decrypt 권한도 함께 고려한다.

## 기억할 문장

> Parameter Store는 애플리케이션의 설정값과 비밀값을 IAM/KMS와 함께 중앙 관리하는 serverless configuration store다.
