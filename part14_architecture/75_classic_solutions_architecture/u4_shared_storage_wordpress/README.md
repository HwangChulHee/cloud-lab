# u4. Shared Storage / WordPress

강의의 WordPress 예시는 scale-out된 여러 EC2가 **같은 user upload/file을 어떻게 공유할지**를 보여준다.

## 문제

```text
EC2 A local disk에 image upload
→ EC2 B에서는 그 image가 없음
```

Auto Scaling 환경에서 local file dependency가 생긴다.

## 해결 방향

```text
EC2 A ─┐
EC2 B ─┼→ Shared File System
EC2 C ─┘
```

Linux shared file use case라면 EFS를 연결할 수 있다.

Database content는 RDS Multi-AZ와 결합한다.

## 전체 감각

```text
Route 53
 ↓
ELB
 ↓
ASG EC2
 ├→ EFS : shared files
 └→ RDS : relational data
```

## 기억할 문장

> Scale-out web application에서 local disk에 공유 데이터를 두지 말고 shared storage 또는 object storage로 state를 분리한다.
