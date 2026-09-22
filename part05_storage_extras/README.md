# 05부 — Storage Extras

SAA 강의의 **Storage Extras** 영역을 정리한다.

이 파트는 저장소 자체보다 먼저 **어떤 access protocol / workload / migration 방식이 필요한가**를 구분하는 것이 핵심이다.

## Chapters

- [ ] [18. EFS](./18_efs/README.md)
- [ ] [19. FSx](./19_fsx/README.md)
- [ ] [20. Storage Gateway](./20_storage_gateway/README.md)
- [ ] [21. DataSync / Transfer Family](./21_datasync_transfer_family/README.md)
- [ ] [22. Snow Family](./22_snow_family/README.md)

## 전체 지도

```text
Linux shared file system / NFS
→ EFS

Windows / Lustre / NetApp / OpenZFS
→ Amazon FSx

On-Premises에서 AWS Storage를 hybrid하게 사용
→ Storage Gateway

대량 데이터 copy / synchronization
→ DataSync

FTP / FTPS / SFTP endpoint
→ AWS Transfer Family

대량 offline migration / edge compute
→ Snowball Edge
```

## 먼저 구분할 것

```text
EBS
→ EC2 block storage

EFS
→ Linux shared NFS file system

FSx
→ specialized managed file systems

S3
→ object storage

Storage Gateway
→ hybrid bridge

DataSync
→ data movement

Transfer Family
→ managed FTP interface

Snowball
→ physical/offline transfer + edge compute
```

## 대표 Architecture

### Shared Linux File

```text
EC2 A ─┐
EC2 B ─┼→ EFS
EC2 C ─┘
```

### Hybrid Storage

```text
On-Premises
   ↓ NFS / SMB / iSCSI
Storage Gateway
   ↓
AWS Storage
```

### Data Migration

```text
On-Premises
   ↓ DataSync Agent
AWS DataSync
   ↓
S3 / EFS / FSx
```

Network transfer가 너무 오래 걸리면:

```text
On-Premises
   ↓
Snowball Edge
   ↓ physical shipping
AWS
   ↓
S3
```

## 시험에서 특히 중요한 비교

```text
EFS
vs
FSx for Windows
→ Linux NFS vs Windows SMB/NTFS

EFS
vs
FSx for Lustre
→ general shared file vs HPC parallel file system

Storage Gateway
vs
DataSync
→ 지속적인 hybrid access vs data copy/sync

DataSync
vs
Transfer Family
→ managed data migration vs FTP/SFTP endpoint

DataSync
vs
Snowball
→ network transfer vs physical offline transfer

Snowball
vs
Glacier
→ Snowball은 Glacier로 직접 import하지 않고 S3를 거쳐 Lifecycle 사용
```

## 학습 순서

```text
18 EFS
shared file system
   ↓
19 FSx
specialized file systems
   ↓
20 Storage Gateway
hybrid storage
   ↓
21 DataSync / Transfer Family
online data transfer
   ↓
22 Snow Family
offline migration / edge
```

## 학습 깊이

이 파트는 기본적으로 **Coverage ~ Hands-on 수준**이다.

특히 다음 질문에 답할 수 있으면 좋다.

```text
NFS인가 SMB인가?
Linux인가 Windows인가?
HPC인가?
on-premises가 계속 AWS storage를 사용해야 하나?
데이터를 옮기는 것인가, storage를 제공하는 것인가?
network로 옮길 수 있는가?
```

현재 `examples/01~16`의 필수 선행조건은 아니지만, EFS/FSx/Storage Gateway/DataSync/Snowball의 선택 기준은 SAA 문제에서 구분할 수 있어야 한다.
