# 29. Amazon ECR

Amazon ECR(Elastic Container Registry)은 AWS의 Container Image 저장소다.

강의에서는 ECR을 ECS와 강하게 통합된 registry로 설명하며, private/public repository, IAM 접근 제어, image scanning, tag/lifecycle 기능을 강조한다.

## Units

- [ ] [u1. Repository / Push / Pull](./u1_repository_push_pull/README.md)
- [ ] [u2. IAM / Authentication](./u2_iam_authentication/README.md)
- [ ] [u3. Scanning / Tags / Lifecycle](./u3_scanning_tags_lifecycle/README.md)
- [ ] [u4. ECS 연동과 SAA 선택](./u4_ecs_integration/README.md)

## 전체 흐름

```text
Developer / CI
   │ docker build
   ▼
Docker Image
   │ push
   ▼
Amazon ECR
   │ pull
   ▼
ECS Task / EKS Pod
```

## 기억할 것

```text
ECR
→ Container Image storage

IAM
→ push/pull 권한 제어

ECS/EKS
→ ECR image를 pull해서 실행
```
