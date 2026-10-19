# u4. EFS Security / Availability / SAA Selection

## Security Group

강의에서는 EFS access를 Security Group으로 제어한다고 설명한다.

```text
EC2
 ↓ NFS
EFS Mount Target
 ↓
Security Group
```

## Encryption

```text
Encryption at rest
→ KMS
```

## Availability

```text
Standard
→ Multi-AZ

One Zone
→ Single AZ
```

## 최종 선택

```text
shared Linux file system
→ EFS

NFSv4.1
→ EFS

auto-growing shared file system
→ EFS

Windows SMB / NTFS
→ FSx for Windows File Server

HPC / ML high-performance parallel file system
→ FSx for Lustre
```

## 면접용 설명

> EFS는 Linux workload가 NFSv4.1로 공유하는 managed file system이고, 자동 확장·Multi-AZ·Security Group·KMS 암호화를 지원합니다. 접근 빈도에 따라 Standard/IA/Archive와 Lifecycle을 사용할 수 있습니다.
