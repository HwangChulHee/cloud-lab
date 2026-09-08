# u4. Gateway Load Balancer (GWLB)

## 지도 확인

Gateway Load Balancer는 일반 웹 애플리케이션 트래픽 분산보다 **네트워크 가상 어플라이언스**를 확장하고 통과시키는 데 초점이 있다.

```text
Traffic
  ↓
GWLB
  ↓
Firewall / IDS / IPS / Inspection Appliance
  ↓
Destination
```

---

## 1. 왜 필요한가

보안 장비를 직접 여러 대 운영하면 트래픽 분산과 장애 대응을 별도로 구성해야 한다.

GWLB를 사용하면 네트워크 트래픽을 여러 가상 어플라이언스로 분산하고, 장애 난 장비를 제외하는 구조를 만들 수 있다.

---

## 2. Layer 3 Gateway + Layer 4 Load Balancing

강의에서는 GWLB를 다음 두 역할을 결합한 서비스로 본다.

```text
Gateway
+
Load Balancer
```

즉 트래픽의 통과 지점 역할과 여러 appliance로 분산하는 역할을 함께 수행한다.

GWLB는 GENEVE 프로토콜을 사용하며 포트 6081을 사용한다.

---

## 3. 사용 사례

대표적으로 다음과 같은 네트워크 장비를 확장할 때 사용한다.

```text
Firewall
Intrusion Detection / Prevention System
Deep Packet Inspection
보안 가상 어플라이언스
```

일반 HTTP 웹 서비스의 Path Routing을 위해 선택하는 서비스가 아니다.

---

## SAA 판단

```text
HTTP path/host 기반 분기
→ ALB

TCP/UDP 고성능 / 고정 IP
→ NLB

트래픽을 방화벽·보안 appliance에 통과시키고 확장
→ GWLB
```

시험에서는 ALB/NLB와 이름이 비슷해도 용도가 완전히 다르다는 점을 구분하는 것이 핵심이다.
