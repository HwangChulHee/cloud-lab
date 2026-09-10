# 59. VPC

## 1. VPC란?

VPC는 AWS에서 사용자가 정의하는 논리적으로 격리된 네트워크다.

실습에서는 다음 구조의 바깥 경계가 VPC다.

```text
VPC 10.0.0.0/16
├─ Public Subnet A
├─ Public Subnet B
├─ Private Subnet A
└─ Private Subnet B
```

## 2. CIDR

VPC를 만들 때 IPv4 CIDR 범위를 지정한다.

예:

```text
10.0.0.0/16
```

이 범위를 더 작은 subnet CIDR로 나눈다.

예:

```text
10.0.1.0/24
10.0.2.0/24
10.0.11.0/24
10.0.12.0/24
```

핵심은 CIDR끼리 겹치지 않도록 설계하는 것이다. VPC Peering, VPN, Direct Connect처럼 다른 네트워크와 연결할 가능성이 있으면 주소 중복이 특히 문제가 된다.

## 3. Region과 AZ

VPC는 Region 범위의 리소스이고 Subnet은 하나의 Availability Zone에 속한다.

```text
Region
└─ VPC
   ├─ Subnet A → AZ-a
   └─ Subnet B → AZ-b
```

고가용성을 위해 보통 여러 AZ에 subnet을 나눈다.

## 4. VPC 내부 통신

VPC route table에는 VPC CIDR에 대한 `local` route가 존재한다.

```text
Destination   Target
10.0.0.0/16  local
```

이를 통해 VPC 내부 subnet 간 통신 경로가 형성된다. 실제 통신 허용 여부는 Security Group/NACL 등 다른 계층의 정책도 함께 영향을 준다.

## 5. 실습에서 볼 구조

```text
Internet
   ↓
Public ALB
   ↓
Private EC2
   ↓
Private RDS
```

모두 같은 VPC 안에 두되 인터넷 노출 수준을 다르게 설계한다.

## 6. Recall Check

- VPC와 Subnet의 범위 차이는?
- Subnet 하나가 여러 AZ에 걸칠 수 있는가?
- `/16` VPC 안에서 `/24` subnet 여러 개를 만드는 이유는?
- 다른 네트워크와 CIDR이 겹치면 왜 문제가 되는가?

## 7. 완료 기준

- [ ] VPC와 Subnet의 관계를 설명할 수 있다.
- [ ] VPC CIDR과 Subnet CIDR의 포함 관계를 이해한다.
- [ ] Multi-AZ 구조에서 subnet을 나누는 이유를 설명할 수 있다.
- [ ] `local` route의 의미를 설명할 수 있다.
