# 19. Amazon FSx

Amazon FSx는 **AWS에서 third-party/high-performance file system을 managed service로 제공**한다.

강의에서 다루는 주요 종류:

```text
FSx for Windows File Server
FSx for Lustre
FSx for NetApp ONTAP
FSx for OpenZFS
```

## Units

- [ ] [u1. FSx 전체 지도](./u1_overview_map/README.md)
- [ ] [u2. FSx for Windows File Server](./u2_windows_file_server/README.md)
- [ ] [u3. FSx for Lustre](./u3_lustre/README.md)
- [ ] [u4. FSx for NetApp ONTAP](./u4_netapp_ontap/README.md)
- [ ] [u5. FSx for OpenZFS / SAA Selection](./u5_openzfs_selection/README.md)

## 전체 지도

```text
Windows SMB / NTFS
→ FSx for Windows File Server

HPC / ML / Parallel File System
→ FSx for Lustre

NetApp ONTAP / NFS + SMB + iSCSI
→ FSx for NetApp ONTAP

ZFS workload / NFS
→ FSx for OpenZFS
```
