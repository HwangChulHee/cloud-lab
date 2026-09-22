# u1. Amazon EKS / Kubernetes Overview

Amazon EKS는 **Amazon Elastic Kubernetes Service**다.

AWS에서 managed Kubernetes cluster를 실행할 수 있게 해준다.

## Kubernetes란?

Kubernetes는 containerized application의 배포, scaling, management를 자동화하는 open-source orchestration system이다.

```text
Container Images
      ↓
Kubernetes
      ↓
Pods / Services / Nodes
```

## EKS 역할

```text
직접 Kubernetes control plane 운영
→ 관리 부담 큼

Amazon EKS
→ AWS가 managed Kubernetes control plane 제공
```

## ECS와 차이

강의 핵심:

```text
ECS
→ AWS 자체 container platform

EKS
→ managed Kubernetes
→ 목적은 비슷하지만 API/생태계가 다름
```

## 언제 EKS인가?

강의에서 대표 use case로 다음을 제시한다.

```text
이미 on-premises에서 Kubernetes 사용
다른 cloud에서 Kubernetes 사용
Kubernetes 기반 workload를 AWS로 migration
```

Kubernetes는 cloud-agnostic 성격이 있기 때문에 기존 운영 지식과 manifest를 재사용하기 쉽다는 점이 선택 이유가 된다.

## Multi-Region

강의에서는 여러 Region에서 EKS를 운영하려면 Region별로 EKS Cluster를 두는 구조로 설명한다.

```text
Region A
→ EKS Cluster A

Region B
→ EKS Cluster B
```

## Observability

CloudWatch Container Insights를 통해 EKS container의 metrics/logs를 수집할 수 있다.

## 기억할 문장

> EKS는 AWS에서 Kubernetes API와 생태계를 유지하면서 managed Kubernetes cluster를 운영하기 위한 서비스다.
