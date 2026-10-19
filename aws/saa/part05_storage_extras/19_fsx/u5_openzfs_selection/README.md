# u5. FSx for OpenZFS / SAA Selection

FSx for OpenZFS는 **AWS에서 managed OpenZFS file system**을 제공한다.

## Protocol

강의에서는 다음 NFS 버전을 언급한다.

```text
NFS v3
NFS v4
NFS v4.1
NFS v4.2
```

## Migration

```text
기존 ZFS workload
→ AWS로 이동
→ FSx for OpenZFS
```

## 호환 환경

```text
Linux
Windows
macOS
VMware Cloud on AWS
WorkSpaces
AppStream 2.0
EC2
ECS
EKS
```

강의에서는 높은 IOPS와 낮은 latency, snapshot/compression/instant cloning을 강조한다.

## 최종 선택 지도

```text
Windows SMB/NTFS/AD
→ FSx for Windows

HPC / ML / S3 연동 parallel filesystem
→ FSx for Lustre

NetApp ONTAP / NFS+SMB+iSCSI
→ FSx for NetApp ONTAP

ZFS / NFS workload
→ FSx for OpenZFS
```
