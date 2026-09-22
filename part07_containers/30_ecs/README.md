# 30. Amazon ECS

Amazon ECS(Elastic Container Service)는 AWS의 **container orchestration 서비스**다.

강의에서는 ECS를 이해할 때 다음 축을 가장 중요하게 본다.

```text
Task / Service
EC2 Launch Type vs Fargate Launch Type
IAM Roles
ALB Integration
EFS Volume
Service Auto Scaling
EventBridge / SQS integration
```

## Units

- [ ] [u1. Cluster / Task / Service](./u1_cluster_task_service/README.md)
- [ ] [u2. EC2 Launch Type vs Fargate](./u2_ec2_vs_fargate/README.md)
- [ ] [u3. ECS IAM Roles](./u3_iam_roles/README.md)
- [ ] [u4. Load Balancer / EFS](./u4_load_balancer_efs/README.md)
- [ ] [u5. ECS Service Auto Scaling](./u5_service_auto_scaling/README.md)
- [ ] [u6. EventBridge / SQS Integration Patterns](./u6_eventbridge_sqs_patterns/README.md)
- [ ] [u7. SAA 선택 기준](./u7_saa_selection/README.md)

## 전체 그림

```text
Docker Image
    ↓
   ECR
    ↓
Task Definition
    ↓
ECS Service
    ↓
ECS Tasks
    ↓
EC2 or Fargate
```

## 가장 중요한 구분

```text
ECS EC2 Launch Type
→ EC2 instances 직접 provision / maintain
→ ECS Agent가 Cluster에 등록
→ container scheduling은 ECS가 담당

ECS Fargate Launch Type
→ EC2 instances 직접 관리하지 않음
→ CPU / RAM을 지정한 Task를 AWS가 실행
→ serverless container compute
```

## SAA 핵심

```text
AWS-native container orchestration
→ ECS

Container host까지 직접 제어
→ ECS on EC2

Instance 관리 최소화
→ ECS on Fargate

HTTP/HTTPS service
→ ALB + ECS Service

공유 persistent filesystem
→ EFS

Task 수 자동 확장
→ ECS Service Auto Scaling
```
