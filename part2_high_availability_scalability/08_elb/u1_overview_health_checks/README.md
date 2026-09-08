# u1. Elastic Load Balancing Overview & Health Checks

## 지도 확인

Load Balancer는 여러 서버 앞에서 요청을 받아 적절한 대상에게 트래픽을 분산한다.

```text
Users
  ↓
Load Balancer
  ↓
EC2 / Target
```

고가용성과 확장성의 핵심은 특정 인스턴스 한 대에 요청이 몰리거나, 장애 난 인스턴스로 트래픽이 계속 가는 상황을 줄이는 것이다.

---

## 1. Elastic Load Balancing이 해결하는 문제

Load Balancer가 없으면 사용자는 특정 인스턴스에 직접 접근한다.

```text
User → EC2 A
```

이 구조는 EC2 A가 장애 나면 서비스도 바로 영향을 받는다.

Load Balancer를 두면:

```text
          → EC2 A
User → ELB
          → EC2 B
```

여러 대상에 요청을 나눌 수 있고, 비정상 대상은 제외할 수 있다.

---

## 2. Health Check

Load Balancer는 Target의 상태를 주기적으로 확인한다.

```text
ELB
 ↓ health check
Target
```

정상 Target에는 요청을 보내고, 비정상 Target에는 요청을 보내지 않는다.

Health Check는 보통 다음을 기준으로 한다.

```text
Protocol
Port
Path (HTTP/HTTPS 계열)
```

예:

```text
GET /health
→ 200 OK
→ healthy
```

따라서 애플리케이션은 단순히 프로세스가 떠 있는지뿐 아니라, 실제 요청을 처리할 수 있는지 보여주는 health endpoint를 제공할 수 있다.

---

## 3. ELB 종류

강의에서는 다음 세 가지를 구분한다.

```text
ALB — Application Load Balancer
NLB — Network Load Balancer
GWLB — Gateway Load Balancer
```

핵심은 어떤 계층의 트래픽을 처리하고 어떤 요구사항에 맞는지 구분하는 것이다.

---

## SAA 판단

```text
HTTP/HTTPS 애플리케이션 트래픽
→ ALB

초고성능 TCP/UDP, 고정 IP 요구
→ NLB

방화벽/보안 어플라이언스 같은 네트워크 장비를 투명하게 통과
→ GWLB

비정상 인스턴스로 요청을 보내지 않아야 함
→ Health Check
```

이후 유닛에서 ALB, NLB, GWLB를 각각 구분한다.
