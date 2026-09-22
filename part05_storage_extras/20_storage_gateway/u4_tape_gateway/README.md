# u4. Tape Gateway

Tape Gateway는 기존 backup software가 사용하는 **Virtual Tape Library(VTL)**를 AWS storage로 연결한다.

## 구조

```text
Backup Application
       ↓ iSCSI VTL
    Tape Gateway
       ↓
      Amazon S3
       ↓ eject/archive
Glacier / Glacier Deep Archive
```

강의 diagram에서는 backup application이 virtual tape를 사용하고, archive 시 Glacier 계층으로 이동하는 흐름을 보여준다.

## 왜 필요한가?

기존 조직이 이미 tape backup workflow를 가지고 있다면 application/process를 크게 바꾸지 않고 cloud archive를 사용할 수 있다.

## SAA 판단

```text
physical tape workflow 대체
virtual tape library
backup archive
→ Tape Gateway
```
