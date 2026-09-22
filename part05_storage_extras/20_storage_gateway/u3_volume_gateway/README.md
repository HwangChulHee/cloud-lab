# u3. Volume Gateway

Volume Gateway는 on-premises application에 **iSCSI block storage interface**를 제공한다.

## 구조

```text
On-Premises Application
        ↓ iSCSI
    Volume Gateway
        ↓
      AWS Cloud
        ↓
    EBS Snapshots
```

강의의 전체 Storage Gateway diagram에서는 Volume Gateway가 local cache를 사용하고 AWS EBS와 연결되는 구조로 설명된다.

## 언제 쓰나?

```text
기존 application이 block storage/iSCSI를 기대
→ Volume Gateway
```

## File Gateway와 구분

```text
File Gateway
→ NFS/SMB
→ file interface

Volume Gateway
→ iSCSI
→ block interface
```

## 기억할 문장

> Volume Gateway는 on-premises에 iSCSI block volume을 제공하고 AWS 기반 snapshot/backup 흐름으로 연결하는 hybrid block storage 방식이다.
