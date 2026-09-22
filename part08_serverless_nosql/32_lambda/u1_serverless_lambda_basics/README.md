# u1. Serverless / Lambda 기본 구조

## 1. Serverless란?

강의 정의:

> Serverless는 서버가 없다는 뜻이 아니라, 개발자가 서버를 직접 관리 / 프로비저닝 / 보지 않는다는 뜻이다.

개발자는 코드를 배포하고 AWS가 runtime, scaling, infrastructure를 관리한다.

```text
Developer
   ↓ deploy code
Lambda
   ↓
AWS가 infrastructure 관리
```

## 2. Lambda 실행 모델

Lambda는 function을 on-demand로 실행한다.

```text
Event
  ↓
Lambda Function
  ↓
Result / Side Effect
```

대표:

```text
API Gateway request
S3 event
SQS message
DynamoDB Stream
EventBridge schedule
```

## 3. EC2와 차이

```text
EC2
→ 항상 떠 있는 server
→ OS/instance lifecycle 관리
→ long-running workload 가능

Lambda
→ event가 있을 때 function 실행
→ server 관리 없음
→ short execution 중심
```

## 4. 지원 언어

강의에서 다음 runtime을 언급한다.

```text
Node.js
Python
Java
C# / .NET
PowerShell
Ruby
Custom Runtime API
Lambda Container Image
```

Container Image를 쓸 수 있지만 Lambda Runtime API를 구현해야 하며, **arbitrary Docker image 실행은 ECS/Fargate가 더 적합**하다고 설명한다.

## 기억할 문장

> Lambda는 서버를 직접 관리하지 않고 event에 반응해 짧은 코드를 자동 확장 실행하는 serverless compute 서비스다.
