# u1. FSx 전체 지도

강의에서는 FSx를 "AWS에서 3rd-party high-performance file system을 실행하는 fully managed service"로 소개한다.

```text
Amazon FSx
├─ Windows File Server
├─ Lustre
├─ NetApp ONTAP
└─ OpenZFS
```

## 구분 기준

```text
어떤 protocol?
어떤 운영체제/기존 workload?
HPC인가?
기존 NetApp/ZFS migration인가?
```

## EFS와 차이 감각

```text
EFS
→ AWS managed NFS shared file system
→ Linux 중심

FSx
→ 특정 file system/호환성 요구
→ Windows / Lustre / ONTAP / OpenZFS
```
