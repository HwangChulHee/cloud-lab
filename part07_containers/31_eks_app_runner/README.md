# 31. Amazon EKS / App Runner 개념 비교

이 단원은 Containers 파트의 마지막 선택 기준을 정리한다.

강의 자료의 핵심 범위는 **Amazon EKS**다. App Runner는 현재 저장소 커리큘럼에 포함된 보강 항목으로, 강의 슬라이드에서는 별도 설명이 확인되지 않아 **보강 개념**으로만 다룬다.

## Units

- [ ] [u1. EKS / Kubernetes Overview](./u1_eks_kubernetes_overview/README.md)
- [ ] [u2. EKS Node Types](./u2_node_types/README.md)
- [ ] [u3. EKS Networking / Load Balancer 구조](./u3_networking_load_balancer/README.md)
- [ ] [u4. EKS Storage / CSI](./u4_storage_csi/README.md)
- [ ] [u5. ECS vs EKS vs App Runner 선택 기준](./u5_ecs_eks_app_runner_selection/README.md)

## EKS 전체 그림

```text
Kubernetes API
      ↓
Amazon EKS Cluster
      ↓
Worker Nodes
├─ Managed Node Group (EC2)
├─ Self-Managed Nodes (EC2)
└─ Fargate
      ↓
Pods
```

## EKS를 떠올리는 상황

```text
기존 Kubernetes 운영 경험 재사용
→ EKS

on-premises / 다른 cloud Kubernetes workload를 AWS로 이전
→ EKS

Kubernetes API / ecosystem 필요
→ EKS
```

## ECS와 먼저 구분

```text
ECS
→ AWS-native container orchestration

EKS
→ managed Kubernetes
→ cloud-agnostic Kubernetes API 활용
```

## App Runner 보강

App Runner는 저장소 커리큘럼 보강용으로 다음 수준만 구분한다.

```text
App Runner
→ web application/container를 빠르게 managed service 형태로 배포
→ orchestration 세부 제어를 크게 줄임

ECS/EKS
→ networking / task / pod / scaling / IAM 등 더 세밀한 제어
```

SAA 강의 범위에서는 EKS를 우선 학습하고, App Runner는 서비스 선택 지도 수준으로만 본다.
