# u3. ECS IAM Roles

강의에서는 ECS 권한을 **EC2 Instance Profile**과 **ECS Task Role**로 구분한다.

## 1. EC2 Instance Profile

EC2 Launch Type에서 ECS Agent가 사용하는 권한이다.

강의 예시:

```text
ECS Agent
→ ECS service API 호출
→ ECR에서 image pull
→ CloudWatch Logs 전송
→ Secrets Manager / SSM Parameter Store 참조
```

구조:

```text
EC2 Instance
├─ ECS Agent
│   └─ EC2 Instance Profile
├─ Task A
└─ Task B
```

## 2. ECS Task Role

각 Task 안의 애플리케이션이 AWS API를 호출할 때 사용하는 Role이다.

```text
Task A
→ S3 access
→ Task A Role

Task B
→ DynamoDB access
→ Task B Role
```

각 Service/Task마다 다른 권한을 줄 수 있다.

## 3. 왜 분리하는가?

```text
EC2 host/ECS Agent가 필요한 권한
≠
application container가 필요한 권한
```

예를 들어 주문 API Task가 S3만 사용한다면 그 Task Role에는 S3 권한만 주는 식으로 최소 권한을 적용할 수 있다.

## SAA 판단

```text
"container needs access to S3"
→ ECS Task Role

"EC2 ECS agent pulls image / talks to ECS"
→ EC2 Instance Profile
```

## 기억할 문장

> ECS Task Role은 애플리케이션 권한이고, EC2 Instance Profile은 EC2 Launch Type에서 ECS Agent/host 측 권한이다.
