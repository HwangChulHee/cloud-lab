# u3. Security Groups와 SSH

## 지도 확인

EC2 강의에서는 인스턴스 기본 구성과 Instance Type을 본 뒤, **Security Group**을 EC2 접근 제어의 핵심으로 바로 연결한다.

Security Group은 AWS 네트워크 보안의 기본 요소이며 EC2로 들어오고 나가는 트래픽을 어떤 규칙으로 허용할지 결정한다.

```text
Internet
   ↓
Security Group
   ↓
EC2
```

이번 유닛에서는 VPC 보안 전체를 깊게 파기보다, EC2를 생성하고 SSH/HTTP로 접근하는 데 필요한 수준까지 익힌다. Security Group 자체의 심화 내용은 뒤에서 다시 다룬다.

---

## 1. Security Group의 기본 역할

Security Group에는 허용 규칙을 설정한다.

```text
Inbound Rules
→ EC2로 들어오는 트래픽

Outbound Rules
→ EC2에서 나가는 트래픽
```

강의에서 강조하는 기본값은 다음과 같다.

```text
Inbound
→ 기본적으로 차단

Outbound
→ 기본적으로 허용
```

Security Group은 방화벽처럼 생각할 수 있지만, OS 내부 방화벽과는 별개의 AWS 계층이다.

---

## 2. Rule은 무엇으로 구성되는가

EC2 웹 서버를 생각해보자.

```text
SSH   TCP 22
HTTP  TCP 80
HTTPS TCP 443
```

Inbound Rule에서는 보통 다음을 판단한다.

```text
Protocol
Port
Source
```

예를 들어 SSH를 내 IP에서만 허용한다면:

```text
TCP 22
Source: 내 Public IP/32
```

웹 서비스를 모두에게 공개한다면:

```text
TCP 80
Source: 0.0.0.0/0
```

`0.0.0.0/0`은 모든 IPv4 주소를 의미하므로 관리 포트를 무조건 이렇게 열어두는 습관은 피한다.

---

## 3. 다른 Security Group을 Source로 사용할 수 있다

Security Group Rule은 IP 주소뿐 아니라 다른 Security Group을 참조할 수 있다.

```text
ALB Security Group
        ↓ 허용
EC2 Security Group
```

이 방식은 나중에 다음 구조에서 중요해진다.

```text
Internet
  ↓
ALB
  ↓
EC2
```

EC2를 인터넷 전체에 직접 노출하기보다 **ALB에서 들어오는 요청만 EC2가 허용**하도록 만들 수 있다.

RDS에서도 같은 사고방식을 다시 사용한다.

---

## 4. Security Group은 EC2 바깥에서 필터링한다

강의에서 중요한 장애 분석 포인트다.

Security Group에서 트래픽이 차단되면 해당 트래픽은 애플리케이션까지 도달하지 않는다.

따라서:

```text
외부 요청 timeout
```

이면 Security Group 같은 네트워크 계층을 의심할 수 있다.

반면:

```text
connection refused
```

라면 요청이 서버까지 도달했지만 해당 포트에서 애플리케이션이 listen하지 않는 상황 등을 먼저 생각할 수 있다.

이 차이는 이후 장애 실험에서 직접 확인한다.

---

## 5. Classic Ports

강의에서 다음 포트들을 기본적으로 소개한다.

```text
22   SSH / SFTP
21   FTP
80   HTTP
443  HTTPS
3389 RDP
```

전부 암기 과목처럼 외우기보다 자주 쓰는 다음 세 개는 바로 알아보는 것이 좋다.

```text
22  SSH
80  HTTP
443 HTTPS
```

---

## 6. SSH로 EC2 접속

Linux EC2에 직접 접속할 때 보통 SSH를 사용한다.

```text
Local PC
   ↓ TCP 22
Security Group
   ↓
EC2 sshd
```

접속을 위해 여러 조건이 동시에 만족되어야 한다.

```text
EC2 running
Public network path 존재
Security Group에서 22 허용
올바른 username
올바른 Key Pair
SSH service 실행
```

따라서 SSH 실패를 단순히 "EC2 문제"로 보면 안 된다.

---

## 7. EC2 Instance Connect

강의에서는 브라우저를 통한 EC2 Instance Connect도 다룬다.

로컬에서 직접 key 파일을 지정하는 방법과 사용 경험은 다르지만, **네트워크 접근 제어가 사라지는 것은 아니다.**

즉 Security Group과 SSH의 관계를 먼저 이해하는 것이 중요하다.

---

## SAA / 운영 연결

```text
EC2에 HTTP 요청을 허용
→ inbound TCP 80

SSH를 관리자 IP에서만 허용
→ inbound TCP 22 + 제한된 Source

ALB만 EC2에 접근 허용
→ Source로 ALB Security Group 참조

요청 timeout
→ Security Group / 네트워크 계층 점검

connection refused
→ 애플리케이션 / listen 상태 점검
```

Security Group은 EC2뿐 아니라 ALB, RDS 등에서도 계속 등장한다. 이번에는 EC2 연결 흐름을 이해하고, 뒤의 Security Group 심화 파트에서 stateful 동작과 NACL 비교, 장애 실험을 다시 다룬다.

이번 유닛은 중요하지만 바로 이어지는 EC2 통합 실습에서 확인하므로 별도 3문장 요약은 생략한다.
