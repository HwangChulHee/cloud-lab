# u4. Cognito Identity Pools / Temporary AWS Credentials

Cognito Identity Pools는 사용자에게 **temporary AWS credentials**를 제공하는 역할을 한다.

강의 핵심:

```text
Users
→ identity 획득
→ temporary AWS credentials
→ AWS Services 직접 접근
```

## Identity Source

강의에서는 Identity Pool의 user source로 다음을 언급한다.

```text
Cognito User Pools
3rd-party logins
기타 identity source
```

## 구조

```text
Web / Mobile App
      ↓ login
Identity Provider / Cognito User Pool
      ↓ token
Cognito Identity Pool
      ↓ exchange
Temporary AWS Credentials
      ↓
S3 / DynamoDB / API Gateway
```

## IAM Role

Identity Pool에서 받은 temporary credentials에는 IAM policy가 적용된다.

강의에서는 다음을 구분한다.

```text
Authenticated Users Role
Guest Users Role
```

사용자 identity에 따라 fine-grained control도 가능하다.

## 대표 예시 — 사용자별 S3 접근

```text
User A
→ Cognito
→ temporary credentials
→ S3의 User A 전용 영역

User B
→ Cognito
→ temporary credentials
→ S3의 User B 전용 영역
```

Application backend를 거치지 않고 사용자가 AWS resource에 직접 접근하도록 만들 수 있다.

## DynamoDB Fine-Grained Access

강의에서는 Identity Pool credentials와 IAM policy를 이용한 DynamoDB row-level/fine-grained access 개념도 보여준다.

## SAA 판단

```text
external user에게 AWS temporary credentials 제공
→ Cognito Identity Pools

user가 private S3에 직접 접근
→ Cognito Identity Pools + IAM Policy

guest/authenticated 권한 분리
→ Cognito Identity Pool Roles
```
