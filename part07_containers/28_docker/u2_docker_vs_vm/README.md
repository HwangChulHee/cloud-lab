# u2. Docker vs Virtual Machine

Docker와 VM은 둘 다 workload를 격리하지만 구조가 다르다.

## Virtual Machine

```text
Physical / Cloud Infrastructure
          ↓
       Host OS
          ↓
      Hypervisor
      ├─ VM A
      │  ├─ Guest OS
      │  └─ App
      └─ VM B
         ├─ Guest OS
         └─ App
```

각 VM은 자체 Guest OS를 가진다.

## Container

```text
Infrastructure
    ↓
Host OS
    ↓
Container Runtime
├─ Container A
├─ Container B
└─ Container C
```

Container는 Host의 OS 자원을 공유하므로 VM보다 일반적으로 더 가볍게 여러 workload를 올릴 수 있다.

## 핵심 차이

```text
VM
→ Guest OS 포함
→ 더 무거움
→ 강한 VM 단위 격리

Container
→ Host OS kernel 공유
→ 더 가벼움
→ 한 host에 더 많은 workload 배치 가능
```

## SAA에서 중요한 연결

Container가 가볍다는 이유로 AWS에서 자동으로 관리되는 것은 아니다.

```text
Container packaging
→ Docker

Container scheduling / orchestration
→ ECS / EKS

Image storage
→ ECR

Underlying compute
→ EC2 또는 Fargate
```
