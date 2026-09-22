# 18. Amazon EFS

Amazon EFS(Elastic File System)는 **Linux 기반 EC2 등에서 공유해서 사용할 수 있는 managed NFS file system**이다.

강의에서는 여러 인스턴스가 동시에 같은 파일 시스템을 마운트할 수 있고, 자동으로 크기가 확장되며 사용량 기반으로 비용을 내는 점을 강조한다.

## Units

- [ ] [u1. EFS 기본 구조 / NFS](./u1_basics_nfs/README.md)
- [ ] [u2. Performance / Throughput Modes](./u2_performance_throughput/README.md)
- [ ] [u3. Storage Classes / Lifecycle](./u3_storage_classes_lifecycle/README.md)
- [ ] [u4. Security / Availability / SAA Selection](./u4_security_availability_selection/README.md)

## 기본 구조

```text
EC2 A ─┐
EC2 B ─┼→ Amazon EFS
EC2 C ─┘
```

## 강의 핵심

```text
NFSv4.1
Linux compatible
Security Group
KMS encryption at rest
POSIX file system
자동 확장
pay-per-use
capacity planning 불필요
```

## 대표 use case

```text
content management
web serving
data sharing
WordPress
```

## SAA 선택 기준

```text
여러 Linux EC2가 같은 파일 공유
→ EFS

Windows SMB file share
→ FSx for Windows File Server

단일 EC2 block storage
→ EBS
```
