# 60. Subnet과 Route Table

## 1. Subnet

Subnet은 VPC의 IP 범위를 AZ 단위로 나눈 네트워크다.

예:

```text
VPC 10.0.0.0/16

AZ-a
├─ Public  10.0.1.0/24
└─ Private 10.0.11.0/24

AZ-b
├─ Public  10.0.2.0/24
└─ Private 10.0.12.0/24
```

## 2. Public / Private의 본질

`Public Subnet`과 `Private Subnet`은 이름 자체가 기능을 만드는 것이 아니다. 핵심은 해당 subnet에 연결된 Route Table의 경로다.

대표적인 public subnet:

```text
Destination   Target
10.0.0.0/16  local
0.0.0.0/0    Internet Gateway
```

대표적인 private subnet:

```text
Destination   Target
10.0.0.0/16  local
0.0.0.0/0    NAT Gateway   # 필요할 때
```

private subnet은 인터넷으로 직접 들어오는 경로를 만들지 않는다.

## 3. Route Table

Route Table은 목적지 CIDR에 따라 다음 hop을 결정한다.

```text
packet destination
       ↓
Route Table
       ↓
local / IGW / NAT / VPC Endpoint / Peering ...
```

라우팅이 된다는 것과 접근이 허용된다는 것은 다르다. Route Table은 경로를 정하고 Security Group/NACL은 허용 여부에 관여한다.

## 4. 가장 구체적인 Route

여러 route가 일치하면 더 구체적인 CIDR prefix가 우선한다.

예:

```text
10.0.0.0/16 → local
0.0.0.0/0   → IGW
```

10.0.1.10 목적지는 `/16 local`이 더 구체적이므로 VPC 내부로 간다.

## 5. 실습 연결

`examples/05`에서 직접:

- 2개 AZ
- Public subnet 2개
- Private subnet 2개
- Public route table
- Private route table
- subnet association

을 만든다.

장애 실험에서는 public route table의 `0.0.0.0/0 → IGW`를 제거해 인터넷 연결 변화를 관찰한다.

## 6. Recall Check

- Public subnet을 결정하는 핵심 요소는 무엇인가?
- Route Table과 Security Group의 역할 차이는?
- subnet별로 서로 다른 route table을 두는 이유는?
- private subnet에 `0.0.0.0/0 → NAT`가 있어도 인터넷에서 직접 들어올 수 없는 이유는?

## 7. 완료 기준

- [ ] Public/Private subnet을 route 관점에서 설명할 수 있다.
- [ ] Route Table의 목적을 설명할 수 있다.
- [ ] subnet association을 이해한다.
- [ ] 요청 목적지를 보고 어떤 route가 선택되는지 추론할 수 있다.
