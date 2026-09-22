# 20. AWS Storage Gateway

AWS Storage Gateway는 **on-premises 환경과 AWS storage 사이를 연결하는 hybrid storage service**다.

강의에서는 hybrid cloud storage 문제를 해결하는 서비스로 설명한다.

## Units

- [ ] [u1. Hybrid Storage / 전체 구조](./u1_hybrid_storage_overview/README.md)
- [ ] [u2. S3 File Gateway](./u2_s3_file_gateway/README.md)
- [ ] [u3. Volume Gateway](./u3_volume_gateway/README.md)
- [ ] [u4. Tape Gateway](./u4_tape_gateway/README.md)
- [ ] [u5. SAA Selection](./u5_saa_selection/README.md)

## 전체 그림

```text
On-Premises
   │
   ├─ NFS/SMB
   ├─ iSCSI
   └─ iSCSI VTL
   │
Storage Gateway
   │
   ▼
AWS Storage
   ├─ S3
   ├─ EBS Snapshot
   └─ Glacier / Deep Archive
```

## 대표 use case

```text
disaster recovery
backup & restore
tiered storage
on-premises cache
low-latency file access
```

## 세 가지 유형

```text
S3 File Gateway
→ NFS/SMB → S3

Volume Gateway
→ iSCSI block volume → AWS

Tape Gateway
→ virtual tape library → S3/Glacier
```
