# u4. FSx for NetApp ONTAP

AWS에서 **managed NetApp ONTAP**을 제공한다.

## Protocol

```text
NFS
SMB
iSCSI
```

## Migration

```text
기존 ONTAP / NAS workload
→ AWS로 이동
→ FSx for NetApp ONTAP
```

## 호환 환경

강의에서는 다음을 언급한다.

```text
Linux
Windows
macOS
VMware Cloud on AWS
Amazon WorkSpaces
AppStream 2.0
EC2
ECS
EKS
```

## Storage 기능

```text
storage auto grow/shrink
snapshots
replication
compression
data deduplication
point-in-time instantaneous cloning
```

## SAA 판단

```text
기존 NetApp workload
NFS + SMB + iSCSI
NAS migration
→ FSx for NetApp ONTAP
```
