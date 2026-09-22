# 21. AWS DataSync / Transfer Family

이 단원은 **데이터를 AWS storage로 어떻게 옮기거나 외부 사용자에게 전송 인터페이스를 제공할지** 구분한다.

## Units

- [ ] [u1. AWS DataSync 기본 구조](./u1_datasync_overview/README.md)
- [ ] [u2. DataSync 대상 / Agent / Scheduling](./u2_datasync_targets_agent_schedule/README.md)
- [ ] [u3. AWS Transfer Family](./u3_transfer_family/README.md)
- [ ] [u4. DataSync vs Transfer Family vs Storage Gateway](./u4_selection_comparison/README.md)

## 핵심 구분

```text
대량 데이터 복사 / 동기화
→ DataSync

FTP / FTPS / SFTP 인터페이스 제공
→ Transfer Family

on-premises application이 계속 NFS/SMB/iSCSI로 AWS storage 사용
→ Storage Gateway
```
