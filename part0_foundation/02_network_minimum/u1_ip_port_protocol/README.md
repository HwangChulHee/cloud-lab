# u1. IP, Port와 Protocol

## 지도 확인

클라우드 아키텍처의 대부분은 결국 **누가 누구에게 어떤 프로토콜과 포트로 통신할 수 있는가**라는 질문으로 내려온다.

```text
Client -- HTTPS:443 --> ALB -- HTTP:8000 --> Application -- TCP:5432 --> PostgreSQL
```

이번 유닛에서는 이 그림을 읽는 데 필요한 최소 개념을 잡는다.

---

## 1. IP Address

IP 주소는 네트워크에서 통신 대상을 식별하기 위한 주소다.

IPv4 예시:

```text
203.0.113.10
10.0.1.20
```

### Public IP

인터넷에서 접근 가능한 주소 공간에서 사용된다.

### Private IP

사설 네트워크 내부에서 사용한다. 서로 다른 사설 네트워크에서는 같은 private IP가 존재할 수 있다.

대표적인 private IPv4 범위:

```text
10.0.0.0/8
172.16.0.0/12
192.168.0.0/16
```

AWS에서 EC2는 VPC 내부 통신용 private IP를 기본적으로 가진다. 인터넷 통신 여부는 public IP 하나만으로 결정되지 않고 subnet, route, gateway, firewall 설정까지 함께 봐야 한다.

---

## 2. Port

IP가 어느 서버인지를 가리킨다면 port는 그 서버의 어느 네트워크 서비스를 찾을지 구분한다.

```text
22    SSH
80    HTTP
443   HTTPS
5432  PostgreSQL
3306  MySQL
```

따라서 다음은 서로 다른 대상이다.

```text
10.0.1.20:80
10.0.1.20:5432
```

AWS Security Group에서도 흔히 `protocol + port + source/destination` 조합으로 규칙을 생각하게 된다.

---

## 3. Protocol

네트워크 통신에는 약속이 필요하다.

### TCP

연결을 맺고 데이터 전달의 신뢰성과 순서를 관리한다. HTTP/HTTPS, SSH, 일반적인 DB 연결 등이 TCP 위에서 많이 동작한다.

### UDP

연결 설정과 전달 보장을 단순화하여 오버헤드가 작다. DNS는 상황에 따라 UDP와 TCP를 사용한다.

### ICMP

오류 전달이나 네트워크 상태 확인에 쓰이며 `ping`이 대표적이다.

중요한 것은 `port`만 보지 않는 것이다.

```text
TCP 443
UDP 443
```

은 같은 포트 번호여도 다른 통신이다.

---

## 4. Connection을 읽는 습관

앞으로 아키텍처의 화살표를 볼 때 다음 네 가지를 묻는다.

```text
1. Source는 누구인가?
2. Destination은 누구인가?
3. Protocol은 무엇인가?
4. Port는 무엇인가?
```

예:

```text
Internet
  ↓ TCP 443
ALB
  ↓ TCP 8000
EC2
  ↓ TCP 5432
RDS PostgreSQL
```

이 네 가지를 명확히 하면 Security Group 설계도 훨씬 쉬워진다.

## 앞으로의 연결

```text
Security Group → 허용할 protocol/port/source
ALB → listener와 target port
RDS → DB port와 접근 주체
VPC → private IP 공간
NACL → subnet 수준 트래픽 제어
```

기초 개념이라 별도 유제와 3문장 요약은 생략한다.
