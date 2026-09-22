# 07부 — Containers

SAA 강의의 Containers on AWS 영역을 정리한다.

이 파트는 **Docker → ECR → ECS/EKS → EC2/Fargate** 흐름을 먼저 잡는 것이 중요하다.

## 전체 지도

```text
Dockerfile
   ↓ build
Docker Image
   ↓ push
Amazon ECR
   ↓ pull
┌─────────────────────┬─────────────────────┐
│ Amazon ECS          │ Amazon EKS          │
│ AWS-native          │ Kubernetes          │
└─────────────────────┴─────────────────────┘
          │                     │
          └─────────┬───────────┘
                    ▼
              EC2 or Fargate
```

## Chapters

- [ ] [28. Docker](./28_docker/README.md)
- [ ] [29. ECR](./29_ecr/README.md)
- [ ] [30. ECS](./30_ecs/README.md)
- [ ] [31. EKS / App Runner 개념 비교](./31_eks_app_runner/README.md)

## 먼저 구분할 것

```text
Docker
→ application을 container image로 packaging

ECR
→ container image registry

ECS
→ AWS-native container orchestration

EKS
→ managed Kubernetes

Fargate
→ ECS/EKS에서 EC2 host를 직접 관리하지 않는 serverless compute
```

App Runner는 현재 저장소 커리큘럼을 위한 보강 개념이다. 첨부 SAA 강의 슬라이드의 Containers 섹션에서는 별도 App Runner 설명을 확인하지 못했기 때문에 31번에서 **서비스 선택 지도 수준**으로만 다룬다.

## 학습 순서

```text
28 Docker
Image / Container / Dockerfile
        ↓
29 ECR
Image Push / Pull / IAM
        ↓
30 ECS
Task / Service / EC2 vs Fargate / ALB / Scaling
        ↓
31 EKS
Kubernetes / Node / Fargate / CSI Storage
        ↓
ECS vs EKS vs App Runner 선택 기준
```

## SAA에서 특히 중요한 것

```text
ECS EC2 Launch Type
vs
ECS Fargate Launch Type

ECS Task Role
vs
EC2 Instance Profile

ECS Service Auto Scaling
vs
EC2 Auto Scaling

ECS
vs
EKS

ECR
= image registry

EFS
= ECS/EKS shared persistent file storage에 연결 가능
```

## 포트폴리오 연결

시험 이후 실제 프로젝트에서는 다음 흐름으로 확장한다.

```text
Spring App
   ↓
Docker Image
   ↓
ECR
   ↓
ECS Fargate
   ↓
ALB
   ↓
CloudWatch
```

이 단계에서 GitHub Actions, Terraform, rolling deployment/rollback 같은 운영 요소를 추가한다.

EKS는 이후 CKA/Kubernetes 학습과 직접 연결한다.
