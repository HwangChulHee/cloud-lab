# u2. Subnet, CIDR, Gateway와 NAT

## 지도 확인

AWS VPC를 이해하려면 IP 주소 하나보다 **주소 범위를 어떻게 나누고, 외부 네트워크와 어떻게 연결하는가**를 볼 수 있어야 한다.

```text
VPC 10.0.0.0/16
├── Subnet A 10.0.1.0/24
└── Subnet B 10.0.2.0/24
```

---

## 1. CIDR

CIDR은 IP 주소 범위를 표현하는 방식이다.

```text
10.0.1.0/24
```

`/24`는 앞 24비트가 네트워크 부분이라는 뜻이다. 지금 단계에서는 비트 계산을 깊게 하기보다 크기 감각만 익힌다.

```text
/16 → 큰 범위
/24 → /16보다 작은 범위
/32 → 단일 IPv4 주소
```

예를 들어 Security Group에서:

```text
203.0.113.10/32
```

이라면 특정 한 IP만 가리키는 식으로 자주 사용한다.

---

## 2. Subnet

Subnet은 더 큰 네트워크 주소 공간을 나눈 작은 네트워크다.

AWS에서는 VPC의 CIDR 범위 일부를 사용해 subnet을 만든다.

```text
VPC 10.0.0.0/16

AZ A
└── 10.0.1.0/24

AZ B
└── 10.0.2.0/24
```

AWS subnet은 하나의 Availability Zone에 속한다. 이후 Multi-AZ 아키텍처에서 서로 다른 AZ에 subnet을 배치하게 된다.

---

## 3. Public / Private이라는 말

AWS에서 subnet의 public/private 성격은 이름 자체가 아니라 **라우팅 구조**로 결정된다.

단순화하면:

```text
Public Subnet
→ Internet Gateway로 향하는 route가 있음

Private Subnet
→ 인터넷으로 직접 향하는 route가 없음
```

실제 인터넷 연결에는 리소스의 IP 설정 등 다른 조건도 함께 필요하지만, 핵심 판단은 route다.

---

## 4. Gateway

서로 다른 네트워크로 나가기 위한 출구를 gateway라고 생각할 수 있다.

AWS에서 자주 만나는 Internet Gateway(IGW)는 VPC와 인터넷 사이의 연결 지점이다.

```text
Internet
   ↕
Internet Gateway
   ↕
VPC
```

Public subnet의 EC2가 인터넷과 통신하려면 route table이 IGW 방향을 가리키는 구조를 사용한다.

---

## 5. NAT

Private subnet의 서버는 외부에서 직접 접근받지 않게 두면서도 업데이트 다운로드나 외부 API 호출을 위해 인터넷으로 **나가는 통신**이 필요할 수 있다.

그때 NAT를 사용할 수 있다.

```text
Private EC2
   ↓
NAT
   ↓
Internet Gateway
   ↓
Internet
```

핵심 차이:

```text
Internet Gateway
→ VPC와 인터넷 연결

NAT
→ private 주소를 사용하는 리소스가 다른 네트워크로 나갈 때 주소 변환
```

AWS의 NAT Gateway는 뒤에서 VPC를 배울 때 비용, AZ 배치, routing까지 다시 자세히 다룬다.

---

## 6. 처음 보는 아키텍처 읽기

```text
Internet
   ↓
IGW
   ↓
Public Subnet: ALB
   ↓
Private Subnet: Application
   ↓
Private Subnet: RDS
```

이런 구조에서 중요한 질문은:

```text
인터넷에 직접 노출되어야 하는 것은 무엇인가?
애플리케이션은 어디에서 요청을 받아야 하는가?
DB가 인터넷에 직접 공개될 이유가 있는가?
private 서버의 outbound 인터넷은 필요한가?
```

이다.

## 앞으로의 연결

VPC 파트에서 CIDR 계산, route table, IGW, NAT Gateway를 실제 AWS 리소스와 함께 다시 다룬다. 지금은 아키텍처 그림을 읽을 정도면 충분하다.

기초 유닛이므로 별도 유제와 3문장 요약은 생략한다.
