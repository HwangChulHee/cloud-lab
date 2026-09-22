# u4. ECS Load Balancer / EFS

## 1. Load Balancer Integration

강의에서는 ECS Service 앞에 Application Load Balancer를 두는 구성을 대부분의 HTTP/HTTPS use case에 권장한다.

```text
Users
  ↓
ALB
  ↓
ECS Service
├─ Task 1
├─ Task 2
└─ Task 3
```

### ALB

```text
HTTP/HTTPS
path/host routing
대부분의 web workload
```

### NLB

강의에서는 높은 throughput / high performance 요구 또는 PrivateLink 연동 같은 경우 NLB를 고려한다고 설명한다.

### CLB

지원은 되지만 advanced feature가 부족하고 Fargate와 맞지 않아 권장하지 않는 흐름으로 설명한다.

---

## 2. ECS Data Volume — EFS

ECS Task에 EFS를 mount할 수 있다.

```text
ECS Task A ─┐
ECS Task B ─┼→ Amazon EFS
ECS Task C ─┘
```

강의 핵심:

```text
EC2 Launch Type + EFS 가능
Fargate + EFS 가능
여러 AZ의 Task가 같은 EFS 데이터 공유 가능
persistent multi-AZ shared storage
```

Fargate + EFS 조합은 compute와 shared file storage 모두 server 관리 부담을 낮춘 구조로 볼 수 있다.

## 주의

강의에서는 S3를 ECS container에 일반 file system처럼 mount하는 대상으로 설명하지 않는다.

## SAA 판단

```text
Web ECS Service
→ ALB

초고성능 TCP/PrivateLink
→ NLB 고려

여러 ECS Task가 같은 persistent files 공유
→ EFS
```
