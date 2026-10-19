# u3. EKS Networking / Load Balancer 구조

강의의 EKS diagram에서는 VPC의 public/private subnet과 Load Balancer를 이용해 Kubernetes Service를 외부 또는 내부에 노출하는 구조를 보여준다.

## 전체 감각

```text
Internet
   ↓
Public Load Balancer
   ↓
EKS Service
   ↓
Pods on Worker Nodes
```

또는:

```text
VPC Internal Client
   ↓
Internal Load Balancer
   ↓
EKS Service
   ↓
Pods
```

## Worker Nodes

강의 diagram에서는 worker nodes가 여러 AZ의 private subnet에 분산될 수 있다.

```text
AZ-A Private Subnet
→ EKS Node / Pods

AZ-B Private Subnet
→ EKS Node / Pods

AZ-C Private Subnet
→ EKS Node / Pods
```

이 구조는 기존에 학습한 VPC / Subnet / Load Balancer 개념 위에 Kubernetes가 올라간 형태로 보면 된다.

## Public vs Private Service

```text
외부 사용자에게 공개
→ public Load Balancer

VPC 내부용 service
→ internal Load Balancer
```

## SAA에서 중요한 포인트

EKS라고 해서 기존 AWS networking 개념이 사라지는 것이 아니다.

```text
VPC
Subnet
Security Group
Load Balancer
NAT / outbound path
```

같은 기반 위에서 Kubernetes workload가 동작한다.

## 기억할 문장

> EKS는 Kubernetes를 쓰지만 실제 네트워크 기반은 AWS VPC/Subnet/Load Balancer 구조와 연결된다.
