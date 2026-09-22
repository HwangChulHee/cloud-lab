# u2. DataSync 대상 / Agent / Scheduling

## Agent 필요 여부

강의에서 중요한 구분:

```text
On-Premises / Other Cloud → AWS
→ DataSync Agent 필요

AWS Storage → AWS Storage
→ Agent 불필요
```

## Destination

강의에서 지원 대상으로 다음을 언급한다.

```text
Amazon S3
Amazon EFS
Amazon FSx
  - Windows
  - Lustre
  - NetApp
  - OpenZFS
```

## Scheduling

Replication task는 다음 주기로 schedule할 수 있다.

```text
hourly
daily
weekly
```

## Metadata / Permission

강의에서는 다음을 보존할 수 있다고 설명한다.

```text
NFS POSIX permissions
SMB metadata
file metadata
```

## Performance

강의에서는 하나의 agent task가 최대 10 Gbps를 사용할 수 있고 bandwidth limit도 설정할 수 있다고 설명한다.

## SAA 판단

```text
on-prem NFS/SMB 대량 migration
→ DataSync Agent

S3 ↔ EFS / FSx 같은 AWS storage 복사
→ DataSync, Agent 없음
```
