# u5. Lambda VPC / IAM / Logging

## 1. IAM

Lambda function이 AWS 서비스에 접근할 때 Execution Role을 사용한다.

예:

```text
Lambda
→ S3 PutObject
→ DynamoDB PutItem
→ SES SendEmail
```

필요한 API 권한을 Lambda Execution Role에 부여한다.

## 2. CloudWatch Logs

강의에서 Lambda monitoring은 CloudWatch와 연결된다.

```text
Lambda invocation
→ logs
→ CloudWatch Logs
```

장애 시 function code error, timeout, retry 등의 단서를 확인한다.

## 3. Lambda와 VPC

Lambda가 VPC 안의 private resource에 접근해야 할 때 VPC networking을 구성할 수 있다.

예:

```text
Lambda
   ↓
Private RDS
```

이때 Lambda를 VPC에 연결했다고 해서 자동으로 인터넷이나 AWS public endpoint 접근이 생기는 것은 아니다.

기존 VPC 학습과 연결해서:

```text
internet outbound 필요
→ NAT path 고려

DynamoDB private access
→ Gateway Endpoint 고려
```

강의의 VPC 섹션에서도 Lambda가 DynamoDB에 접근할 때 NAT 대신 DynamoDB Gateway Endpoint를 사용할 수 있는 구조를 보여준다.

## 4. RDS 연결

짧은 시간에 Lambda가 많이 늘어나면 DB connection 수도 급격히 늘 수 있다.

강의의 RDS 영역과 연결해서 RDS Proxy를 함께 떠올린다.

## 기억할 문장

> Lambda의 AWS API 권한은 Execution Role, 실행 로그는 CloudWatch Logs, VPC 내부 자원 접근은 VPC networking 조건을 따로 본다.
