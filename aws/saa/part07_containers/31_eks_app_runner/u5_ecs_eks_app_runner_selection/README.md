# u5. ECS vs EKS vs App Runner 선택 기준

이 문서는 Containers 파트 전체의 서비스 선택 지도를 정리한다.

> EKS/ECS 비교는 강의 범위다. App Runner 부분은 현재 저장소 커리큘럼을 위한 보강 개념이며, 첨부 강의 슬라이드에서는 별도 App Runner 설명을 확인하지 못했다.

## 1. ECS

```text
AWS-native container orchestration
Task / Service
EC2 or Fargate
ALB / Auto Scaling / IAM 세밀한 제어
```

대표:

```text
AWS에 최적화된 container service
→ ECS
```

## 2. EKS

```text
Managed Kubernetes
Kubernetes API / ecosystem
EC2 nodes or Fargate
기존 Kubernetes 운영 경험 재사용
```

대표:

```text
on-prem Kubernetes를 AWS로 migration
→ EKS
```

## 3. App Runner — 보강 개념

App Runner는 source code 또는 container image 기반 web application을 비교적 적은 infrastructure 설정으로 배포하는 managed application service로 이해한다.

```text
Source / Container Image
       ↓
   App Runner
       ↓
Managed Web Service
```

ECS/EKS보다 orchestration 상세 제어를 줄이고 빠른 web service 배포에 초점을 둔다.

## 제어 수준 감각

```text
더 단순한 Web App 운영
→ App Runner

AWS-native container orchestration 제어
→ ECS

Kubernetes 표준/생태계 필요
→ EKS
```

## Fargate는 어디에 들어가나?

Fargate는 ECS/EKS와 경쟁하는 orchestration 서비스가 아니라 **container compute option**이다.

```text
ECS
├─ EC2
└─ Fargate

EKS
├─ EC2 Nodes
└─ Fargate
```

## 최종 선택표

| 요구사항 | 선택 |
|---|---|
| AWS-native container orchestration | ECS |
| Kubernetes API / migration | EKS |
| EC2 host 관리 없이 ECS/EKS 실행 | Fargate |
| Container Image Registry | ECR |
| 빠른 managed web app 배포, orchestration 세부 제어 최소화 | App Runner (보강) |

## 기억할 문장

> ECS는 AWS-native orchestration, EKS는 Kubernetes, Fargate는 serverless container compute, ECR은 image registry다. App Runner는 더 높은 수준으로 web application 배포를 단순화하는 managed service다.
