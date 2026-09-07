# u6. Elastic Network Interface (ENI)

## 지도 확인

ENI(Elastic Network Interface)는 VPC 안에서 EC2에 붙는 **가상 네트워크 카드**라고 보면 된다.

```text
EC2
├── eth0 → primary ENI
└── eth1 → secondary ENI
```

강의에서는 ENI를 EC2 네트워킹의 구성 요소로 설명한다.

---

## 1. ENI가 가지는 것

ENI에는 다음과 같은 속성이 연결될 수 있다.

```text
Primary Private IPv4
Secondary Private IPv4
Public IPv4
Elastic IP
Security Groups
MAC Address
```

즉 IP 주소와 Security Group 같은 네트워크 정보가 단순히 EC2 본체에만 붙어 있다고 생각하기보다, ENI라는 네트워크 인터페이스 단위로 연결된다고 이해하면 된다.

---

## 2. ENI는 독립적으로 만들 수 있다

강의에서는 ENI를 EC2와 별도로 생성한 뒤 다른 EC2에 붙일 수 있다는 점을 설명한다.

```text
EC2 A
  │
 ENI

장애 발생

EC2 B
  │
 ENI 이동
```

이런 특성을 이용하면 네트워크 인터페이스를 이동시켜 failover 구조를 생각할 수 있다.

---

## 3. Availability Zone 제약

ENI는 특정 Availability Zone에 종속된다.

```text
ENI in AZ-A
→ AZ-A의 EC2에 연결
```

따라서 ENI를 아무 Region/AZ의 EC2에 자유롭게 붙이는 개념은 아니다.

---

## SAA 연결

ENI 문제에서는 다음 키워드를 본다.

```text
virtual network card
multiple private IPs
multiple security groups
move network interface for failover
bound to an AZ
```

ENI의 세부 활용은 이후 VPC와 Load Balancer를 공부할 때 다시 연결한다.

이번 유닛은 개념 분류가 중심이므로 유제와 3문장 요약은 생략한다.
