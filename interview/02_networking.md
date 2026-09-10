# 02. Networking

## 핵심 질문

1. TCP와 UDP의 차이는 무엇인가요?
2. TCP 3-way handshake를 설명해보세요.
3. DNS가 어떻게 동작하는지 설명해보세요.
4. 사용자가 `example.com`을 입력한 뒤 서버까지 어떤 일이 일어나나요?
5. HTTP와 HTTPS의 차이는 무엇인가요?
6. TLS 인증서가 어떤 역할을 하나요?
7. HTTP 502, 503, 504의 차이는 무엇인가요?
8. CIDR의 `/24`는 무엇을 의미하나요?
9. `10.0.0.0/16`을 `/24` subnet으로 나누면 몇 개가 나오나요?
10. NAT는 왜 필요한가요?
11. Public subnet과 Private subnet의 차이는 무엇인가요?
12. inbound와 outbound traffic의 차이는 무엇인가요?
13. ping은 되는데 HTTP가 안 됩니다. 어떻게 조사하겠습니까?
14. DNS resolution은 되는데 웹사이트 접속이 안 됩니다. 어디부터 확인하나요?
15. `connection refused`와 `timeout`은 어떻게 다른가요?

## 면접에서 자주 연결되는 흐름

```text
Browser
 ↓
DNS Resolver
 ↓
Authoritative DNS
 ↓
Load Balancer / Public IP
 ↓
Network rules
 ↓
Server
 ↓
Application
```

## 실전형 질문

### Private subnet의 EC2가 인터넷에서 패키지를 다운로드하려면?

```text
Private EC2
  ↓
Private subnet Route Table
  ↓ 0.0.0.0/0
NAT Gateway (Public subnet)
  ↓
Internet Gateway
  ↓
Internet
```

핵심은 Private EC2 자체에 public IPv4를 주는 것이 아니라 NAT를 통해 outbound 통신을 가능하게 하는 것입니다.
