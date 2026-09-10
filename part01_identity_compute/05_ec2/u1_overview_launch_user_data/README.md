# u1. EC2 Overview, Launch와 User Data

## 지도 확인

Amazon EC2(Elastic Compute Cloud)는 AWS에서 가상 머신을 빌려 사용하는 서비스다.

강의에서는 EC2를 단순한 VM 하나로 보지 않고 다음 요소와 함께 이해한다.

```text
EC2
├── Virtual Machine
├── EBS / EFS / Instance Store
├── Security Group
├── Public / Private IP
├── User Data
├── ELB
└── Auto Scaling
```

이번 유닛에서는 EC2의 전체 그림과 인스턴스 생성 시 선택하는 주요 설정, 그리고 User Data의 역할까지 잡는다.

---

## 1. EC2는 무엇인가

EC2는 Infrastructure as a Service(IaaS)에 해당한다.

즉 운영체제와 애플리케이션을 직접 관리하는 대신, 물리 서버를 직접 구매하지 않고 필요한 만큼 가상 서버를 생성한다.

EC2를 생성할 때 주로 선택하는 것은 다음과 같다.

```text
Operating System
CPU / Memory
Storage
Network
Public IP
Security Group
User Data
```

EC2 자체는 컴퓨팅 자원이고, 저장소는 EBS/EFS/Instance Store와 연결된다. 부하 분산은 ELB, 자동 확장은 Auto Scaling Group에서 이어서 다룬다.

---

## 2. 인스턴스 생성 흐름

강의의 첫 실습에서는 AWS Console에서 Linux EC2 인스턴스를 생성하고 웹 서버를 User Data로 실행한다.

큰 흐름은 다음처럼 보면 된다.

```text
AMI 선택
  ↓
Instance Type 선택
  ↓
Key Pair
  ↓
Network / Security Group
  ↓
Storage
  ↓
User Data
  ↓
Launch
```

처음에는 옵션을 모두 외우려 하지 말고, 각각이 어떤 종류의 결정인지 구분하는 게 중요하다.

---

## 3. EC2 User Data

User Data는 인스턴스의 최초 시작 시 자동으로 명령을 실행하기 위한 bootstrap script다.

주로 다음 작업에 사용한다.

```text
패키지 업데이트
소프트웨어 설치
설정 파일 생성
웹 서버 실행
필요한 파일 다운로드
```

예를 들어 웹 서버 설치를 자동화하면:

```text
EC2 Launch
  ↓
User Data 실행
  ↓
웹 서버 설치
  ↓
서비스 시작
```

강의에서는 User Data가 첫 시작 시 실행되고 root 권한으로 실행된다는 점을 강조한다.

운영 관점에서는 User Data를 사람이 SSH로 접속해서 반복 작업하는 대신 초기 설정을 자동화하는 첫 단계로 보면 된다.

---

## 4. Start / Stop / Terminate

EC2 인스턴스는 상태를 가진다.

```text
running
stopped
terminated
```

`stop`은 인스턴스 실행을 멈추지만 EBS 데이터는 유지될 수 있다.

`terminate`는 인스턴스를 제거하는 동작이며 root EBS가 Delete on Termination으로 설정되어 있다면 해당 볼륨도 삭제된다.

이 차이는 이후 EBS 파트에서 더 자세히 다룬다.

---

## SAA 연결

EC2 문제에서는 단순히 "서버"라고 읽기보다 다음 질문으로 분해한다.

```text
얼마나 많은 CPU/Memory가 필요한가?
저장소는 무엇을 사용할까?
외부에서 접근해야 하는가?
부팅 시 자동 설정이 필요한가?
트래픽이 증가하면 어떻게 확장할까?
```

EC2는 이후 EBS, Security Group, ELB, Auto Scaling, IAM Role, CloudWatch와 계속 연결된다.

---

## 앞으로의 연결

```text
EC2 Instance Type
→ 성능 특성

User Data
→ 초기 설정 자동화

Security Group
→ 인스턴스 방화벽

EBS
→ 영구 블록 스토리지

ELB / ASG
→ 고가용성과 확장
```

이번 유닛은 전체 그림이므로 별도 유제와 3문장 요약은 생략한다.
