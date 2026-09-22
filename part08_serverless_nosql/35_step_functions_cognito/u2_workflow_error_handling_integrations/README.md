# u2. Step Functions Workflow / Error Handling / Integrations

Step Functions는 Lambda만 연결하는 서비스가 아니다.

강의에서는 다음과의 integration을 언급한다.

```text
Lambda
EC2
ECS
On-Premises Servers
API Gateway
SQS
기타 AWS Services
```

## 1. Sequence

```text
Task A
  ↓
Task B
  ↓
Task C
```

앞 작업이 끝난 뒤 다음 작업으로 넘어간다.

## 2. Parallel

```text
        ┌→ Task B
Task A ─┤
        └→ Task C
```

독립 작업을 동시에 실행하는 workflow를 만들 수 있다.

## 3. Conditions

```text
PaymentResult
   ↓
 Choice
 ├─ SUCCESS → Shipping
 └─ FAIL    → Compensation
```

입력/결과에 따라 branch를 나눈다.

## 4. Timeout / Error Handling

긴 workflow에서 특정 step이 끝없이 대기하지 않도록 timeout을 두고, 실패 시 다른 처리 경로로 보낼 수 있다.

```text
Task Failure
   ↓
Error Handler
   ↓
Retry / Alternative Path
```

## 5. API Gateway와 연결

강의에서는 API Gateway AWS Service Integration으로 Step Functions workflow를 시작하는 예를 든다.

```text
Client
  ↓
API Gateway
  ↓
Step Functions
  ↓
Workflow
```

## SAA 판단

```text
여러 Lambda 호출 순서를 코드 밖에서 관리
→ Step Functions

조건/병렬/timeout/error path가 있는 serverless workflow
→ Step Functions
```
