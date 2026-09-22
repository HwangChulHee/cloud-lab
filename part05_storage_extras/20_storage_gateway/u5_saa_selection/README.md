# u5. Storage Gateway SAA Selection

```text
on-prem NFS/SMB → S3
→ S3 File Gateway

on-prem iSCSI block volume
→ Volume Gateway

backup software / virtual tape
→ Tape Gateway
```

## 대표 keyword

```text
hybrid storage
on-premises cache
backup & restore
disaster recovery
tiered storage
existing storage protocol
```

## 다른 서비스와 구분

```text
Storage Gateway
→ hybrid access를 지속적으로 제공

DataSync
→ 대량 data copy / synchronization

Transfer Family
→ FTP / FTPS / SFTP로 S3/EFS 접근

Snowball
→ network 대신 physical device로 대량 offline migration
```

## 면접용 설명

> Storage Gateway는 on-premises와 AWS storage를 연결하는 hybrid storage bridge입니다. File Gateway는 NFS/SMB에서 S3로, Volume Gateway는 iSCSI block storage로, Tape Gateway는 기존 VTL backup workflow를 AWS archive로 연결합니다.
