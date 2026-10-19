# u2. EKS Node Types

강의에서는 EKS workload가 실행되는 compute를 세 가지로 구분한다.

## 1. Managed Node Groups

```text
EKS
 ↓
Managed Node Group
 ↓
EC2 Nodes
 ↓
Pods
```

AWS/EKS가 node 생성과 관리 작업을 도와준다.

강의 핵심:

```text
EC2 instances 기반
ASG와 연결
On-Demand / Spot 사용 가능
```

## 2. Self-Managed Nodes

사용자가 EC2 nodes를 직접 만들고 EKS Cluster에 등록한다.

```text
User-managed EC2
→ EKS Optimized AMI 등 사용 가능
→ ASG 구성
→ Cluster에 등록
```

Managed Node Group보다 직접 제어와 운영 책임이 더 크다.

## 3. AWS Fargate

```text
EKS
 ↓
Fargate
 ↓
Pods
```

EC2 node를 직접 관리하지 않는다.

강의 핵심:

```text
No nodes to manage
No maintenance of EC2 worker nodes
```

## 선택 기준

```text
EC2 node 관리 일부 자동화
→ Managed Node Groups

node 세부 제어 직접 수행
→ Self-Managed Nodes

node 관리 자체를 피함
→ Fargate
```

## ECS와 연결

Fargate는 ECS 전용 서비스가 아니다.

```text
ECS + Fargate
EKS + Fargate
```

둘 다 가능하다.
