# u2. S3 File Gateway

S3 File Gateway는 on-premises에서 **NFS/SMB file share처럼 접근하면서 실제 data는 S3에 저장**하는 구조다.

## 구조

```text
On-Premises Application
        ↓ NFS / SMB
    File Gateway
        ↓
      Amazon S3
```

## Local Cache

강의에서는 최근 사용한 data를 File Gateway의 local cache에 둔다고 설명한다.

```text
frequently/recently used data
→ local cache
→ low-latency access
```

## 핵심 감각

```text
사용자/애플리케이션
→ 일반 file share처럼 접근

실제 cloud backend
→ Amazon S3
```

## SAA 판단

```text
on-premises에서 NFS/SMB 사용
+
backend는 S3
→ S3 File Gateway
```
