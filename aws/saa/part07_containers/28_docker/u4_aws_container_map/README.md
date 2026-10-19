# u4. AWS Container 서비스 전체 지도

강의의 핵심 서비스는 네 가지로 정리할 수 있다.

```text
Docker Image
   ↓
Amazon ECR
   ↓
┌───────────────┬───────────────┐
│ Amazon ECS    │ Amazon EKS    │
│ AWS-native    │ Kubernetes    │
└───────────────┴───────────────┘
        │               │
        └──────┬────────┘
               ▼
        EC2 or Fargate
```

## ECS

AWS 자체 container orchestration 서비스.

## EKS

AWS가 관리하는 Kubernetes 서비스.

## Fargate

ECS/EKS에서 사용할 수 있는 serverless compute option.

```text
EC2
→ node/instance를 직접 관리

Fargate
→ instance를 직접 provision/patch/manage하지 않음
```

## ECR

Container Image 저장소.

## SAA 선택

```text
AWS-native orchestration
→ ECS

Kubernetes API/생태계 필요
→ EKS

Container host 관리 최소화
→ Fargate

Image 저장
→ ECR
```
