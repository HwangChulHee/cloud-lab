# u4. DataSync vs Transfer Family vs Storage Gateway

## DataSync

```text
목적
→ 대량 copy / migration / synchronization

특징
→ scheduled transfer
→ agent 가능
→ metadata/permission 보존
```

## Transfer Family

```text
목적
→ FTP / FTPS / SFTP endpoint 제공

대상
→ S3 / EFS
```

## Storage Gateway

```text
목적
→ hybrid storage access를 지속적으로 제공

protocol
→ NFS / SMB / iSCSI / VTL
```

## 최종 선택

```text
데이터를 옮긴다
→ DataSync

FTP client가 계속 접속해야 한다
→ Transfer Family

on-prem application이 AWS storage를 local storage처럼 계속 사용한다
→ Storage Gateway
```
