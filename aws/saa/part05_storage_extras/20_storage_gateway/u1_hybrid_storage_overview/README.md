# u1. Hybrid Storage / 전체 구조

강의에서는 Storage Gateway를 **on-premises data와 cloud data 사이의 bridge**로 설명한다.

## 왜 필요한가?

Hybrid Cloud 상황:

```text
일부 infrastructure
→ On-Premises

일부 infrastructure
→ AWS Cloud
```

이런 구조가 생기는 이유로 강의는 다음을 언급한다.

```text
긴 cloud migration
security requirement
compliance requirement
IT strategy
```

S3는 proprietary object storage이고 on-premises application은 NFS/SMB/iSCSI 같은 기존 protocol을 기대할 수 있다.

Storage Gateway가 그 차이를 연결한다.

## Deployment

강의 diagram에서는 Gateway를 다음 virtualization 환경에 배포할 수 있다고 설명한다.

```text
VMware
Hyper-V
KVM
```

## 연결

```text
On-Premises
   ↓
Storage Gateway
   ↓
Internet 또는 Direct Connect
   ↓
AWS
```

## 기억할 문장

> Storage Gateway는 on-premises 애플리케이션의 기존 storage protocol을 유지하면서 AWS storage를 hybrid하게 사용하는 bridge다.
