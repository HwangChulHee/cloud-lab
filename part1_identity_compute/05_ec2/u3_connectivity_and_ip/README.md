# u3. EC2 Connectivity와 IP

## 지도 확인

EC2를 만들었다고 바로 접속 가능한 것은 아니다.

접속을 이해하려면 다음을 함께 본다.

```text
Public IP / Private IP
SSH
Port 22
Key Pair
Security Group
EC2 Instance Connect
Elastic IP
```

---

## 1. Private IP와 Public IP

강의에서는 기본적으로 EC2가 내부 AWS 네트워크에서 사용하는 Private IP와, 인터넷에서 접근할 때 사용할 수 있는 Public IP를 구분한다.

```text
Private IP
→ AWS 내부 네트워크에서 사용

Public IP
→ 인터넷에서 접근할 때 사용 가능
```

내 PC가 같은 사설 네트워크 안에 있지 않다면 일반적으로 EC2의 Private IP로 바로 SSH 접속할 수 없다.

---

## 2. SSH

SSH는 원격 Linux 서버를 명령줄로 제어하는 기본 방식이다.

```text
내 PC
  ↓ SSH :22
Internet
  ↓
EC2 Public IP
```

접속이 되려면 최소한 다음이 맞아야 한다.

```text
인스턴스 running
Public IP 존재
Security Group에서 22 허용
올바른 사용자 이름
올바른 Key Pair
```

SSH 문제를 볼 때는 "EC2가 안 된다"라고 뭉뚱그리지 말고 어느 조건에서 막혔는지 분리해서 본다.

---

## 3. EC2 Instance Connect

강의에서는 브라우저에서 EC2에 연결하는 EC2 Instance Connect도 소개한다.

임시 키를 인스턴스에 전달해 접속하는 방식이며, 로컬에 내려받은 private key를 직접 지정하지 않고 접속할 수 있다.

단, 네트워크 요구사항이 사라지는 것은 아니다. SSH 포트 접근 가능 여부 등은 여전히 확인해야 한다.

---

## 4. Public IP는 바뀔 수 있다

강의에서 중요한 포인트:

```text
EC2 stop
  ↓
start
  ↓
Public IP가 변경될 수 있음
```

Private IP는 인스턴스의 내부 주소로 사용되고, 자동 할당된 Public IPv4는 stop/start 이후 달라질 수 있다.

---

## 5. Elastic IP

고정된 Public IPv4가 필요하면 Elastic IP를 사용할 수 있다.

```text
Elastic IP
→ 고정 Public IPv4
→ EC2에 연결 가능
```

하지만 강의에서는 Elastic IP를 남용하기보다 DNS나 Load Balancer를 사용하는 아키텍처를 선호하는 방향을 설명한다.

즉 고정 IP가 정말 요구사항인지부터 판단한다.

---

## 장애 분석

```text
SSH timeout
```

이라면 다음 순서로 생각한다.

```text
1. EC2 running인가?
2. Public IP가 맞는가?
3. Security Group 22가 열려 있는가?
4. 네트워크 경로가 있는가?
5. SSH username / key가 맞는가?
```

Security Group 자체는 07 파트에서 자세히 다룬다.

이번 유닛은 0부 Linux/Network 내용과 겹치므로 별도 유제와 3문장 요약은 생략한다.
