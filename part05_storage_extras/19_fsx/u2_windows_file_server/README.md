# u2. FSx for Windows File Server

완전 관리형 Windows file share다.

## 핵심 기능

```text
SMB protocol
Windows NTFS
Microsoft Active Directory integration
ACLs
User quotas
DFS Namespaces
```

강의에서는 Linux EC2에서도 mount할 수 있다고 설명한다.

## Storage Options

```text
SSD
→ latency-sensitive
→ database / media processing / analytics

HDD
→ home directory / CMS 등
```

## Hybrid Access

On-premises에서 VPN 또는 Direct Connect를 통해 접근할 수 있다.

## High Availability

Multi-AZ 구성 가능.

강의에서는 data가 daily backup되어 S3에 저장된다고 설명한다.

## SAA 판단

```text
Windows shared drive
SMB
NTFS
Active Directory
→ FSx for Windows File Server
```
