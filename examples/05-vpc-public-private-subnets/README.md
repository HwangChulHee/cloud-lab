# Example 05 — VPC와 Public/Private Subnet 직접 만들기

기본 VPC를 쓰지 않고 직접 네트워크를 구성한다. 이번 단계부터 이전에 배운 EC2와 Security Group은 반복 작업으로 취급한다.

## Recall Check

- EC2의 Public IP와 Private IP 차이는?
- Security Group inbound를 닫으면 어떤 증상이 났는가?
- ALB와 EC2는 왜 SG를 분리했는가?

## 새로 배우는 것

- VPC CIDR
- Public / Private Subnet
- Route Table
- Internet Gateway
- Subnet과 AZ의 관계

## 반복하는 것

- EC2 생성
- Security Group
- User Data
- HTTP 요청 확인

## 이번에는 도움 없이

EC2 생성, User Data 작성, HTTP 80 SG 생성은 이전 Example을 보지 않고 먼저 해본다. 막히면 01~04를 참고한다.

모든 태그 가능 리소스에는 다음 태그를 붙인다.

```text
Project=cloud-lab
Stage=examples
Example=05
```

Name은 `example-05-*` 형식을 사용한다.

## 리소스 이름표

| 리소스 | 이름 |
| --- | --- |
| VPC | `example-05-vpc` |
| Public Subnet A | `example-05-public-a` |
| Public Subnet B | `example-05-public-b` |
| Private Subnet A | `example-05-private-a` |
| Private Subnet B | `example-05-private-b` |
| Internet Gateway | `example-05-igw` |
| Public Route Table | `example-05-public-rt` |
| Main/Private Route Table Name tag | `example-05-private-rt` |
| EC2 | `example-05-web` |
| EC2 Security Group | `example-05-web-sg` |

Main Route Table은 VPC 생성 시 자동으로 생긴다. 새로 만들 필요는 없고, Name tag만 `example-05-private-rt`로 붙여 식별하기 쉽게 한다.

## 목표 구조

```text
VPC 10.0.0.0/16
├─ AZ-A
│  ├─ Public  10.0.1.0/24
│  └─ Private 10.0.11.0/24
└─ AZ-B
   ├─ Public  10.0.2.0/24
   └─ Private 10.0.12.0/24

Internet → IGW → Public Route Table
```

## 1. VPC 생성

- Name: `example-05-vpc`
- IPv4 CIDR: `10.0.0.0/16`

생성 후 Main Route Table을 확인한다. `10.0.0.0/16 -> local` 경로가 왜 자동으로 존재하는지 생각한다.

## 2. Subnet 4개 생성

서로 다른 두 AZ를 선택해 위 구조대로 Public 2개, Private 2개를 만든다.

- Subnet은 하나의 AZ에 속한다.
- 같은 VPC 내부 CIDR이 겹치면 안 된다.

## 3. Internet Gateway 연결

`example-05-igw`를 만들고 VPC에 Attach한다.

## 4. Public Route Table 생성

Public 전용 Route Table을 만들고 VPC 내부 local route 외에 인터넷으로 향하는 default route를 추가한다. Public Subnet 2개를 이 Route Table에 association 한다.

Private Subnet은 VPC 내부 local route만 유지한다.

## 5. Public Subnet에 EC2 생성

Public Subnet 하나에 EC2를 만든다.

- Public IPv4 활성화
- HTTP 80 허용
- User Data로 nginx 실행

Public IP로 접속되는지 확인한다.

## 6. 관찰

```text
Q. Public Subnet을 Public하게 만드는 핵심은 무엇인가?
Q. IGW만 VPC에 붙이고 Route가 없으면 인터넷 통신이 가능한가?
Q. Public route만 있고 EC2에 Public IPv4/EIP가 없다면 인터넷에서 직접 접근 가능한가?
```

## 7. 장애 실험 — IGW Route 삭제

Public Route Table의 인터넷 default route를 잠시 삭제한다. 브라우저 요청이 어떻게 변하는지 확인하고, EC2 상태와 SG는 정상이라는 것도 확인한다. 원인을 찾은 뒤 route를 복구한다.

## 8. 장애 실험 — 잘못된 Route Table Association

Public Subnet 하나를 Private 쪽 Route Table에 association 해본다. 같은 EC2가 어떤 영향을 받는지 관찰하고 원래 association으로 복구한다.

## 9. CLI 구축/장애 검증

### 1. 실습 VPC ID 얻기

```bash
export VPC_ID=$(aws ec2 describe-vpcs --region $AWS_REGION \
  --filters 'Name=tag:Name,Values=example-05-vpc' \
  --query 'Vpcs[0].VpcId' --output text)

echo $VPC_ID
```

먼저 사람이 VPC ID를 복사하는 대신 CLI로 찾아 변수에 저장한다. 이후 모든 조회를 같은 VPC로 제한할 수 있다.

### 2. Subnet과 AZ

```bash
aws ec2 describe-subnets --region $AWS_REGION \
  --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'Subnets[].{Name:Tags[?Key==`Name`]|[0].Value,Id:SubnetId,CIDR:CidrBlock,AZ:AvailabilityZone,PublicIP:MapPublicIpOnLaunch}' \
  --output table
```

- `CIDR`: subnet 주소 범위.
- `AZ`: subnet이 속한 단일 AZ.
- `MapPublicIpOnLaunch`: 새 EC2에 public IPv4를 자동 부여하도록 설정했는지 보여준다. 이것만으로 public subnet이 되는 것은 아니다.

### 3. Route Table

```bash
aws ec2 describe-route-tables --region $AWS_REGION \
  --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'RouteTables[].{Name:Tags[?Key==`Name`]|[0].Value,Id:RouteTableId,Routes:Routes,Associations:Associations[].SubnetId}'
```

핵심은 `Routes`와 `Associations`를 같이 보는 것이다.

```text
Routes
→ 어디로 보내는가?

Associations
→ 이 Route Table을 어느 Subnet이 사용하는가?
```

Public Subnet의 Route Table에는 인터넷 default route가 IGW를 가리켜야 한다.

### 4. Internet Gateway

```bash
aws ec2 describe-internet-gateways --region $AWS_REGION \
  --filters "Name=attachment.vpc-id,Values=$VPC_ID" \
  --query 'InternetGateways[].{Id:InternetGatewayId,Attachments:Attachments}'
```

`Attachments`를 통해 IGW가 **실제로 이 VPC에 attach되어 있는지** 확인한다.

장애 실험에서는 route 삭제 전/후에 2번과 3번 명령을 반복하면 "EC2와 SG는 그대로인데 Route만 사라졌다"는 것을 증명할 수 있다.

## 10. 기억만으로 설명하기

- Public Subnet과 Private Subnet의 차이를 Route Table 기준으로 설명한다.
- Public EC2가 인터넷과 직접 통신하려면 route뿐 아니라 Public IPv4/EIP도 필요하다는 것을 설명한다.
- SG와 Route Table의 역할 차이를 설명한다.
- `10.0.0.0/16 local`이 필요한 이유를 설명한다.

## 완료 체크

- [ ] 공통 태그와 이름 규칙을 적용했다.
- [ ] VPC를 직접 만들었다.
- [ ] 2AZ에 Public/Private Subnet을 만들었다.
- [ ] IGW와 Public Route Table을 연결했다.
- [ ] EC2를 Public Subnet에 배치했다.
- [ ] IGW route 삭제 장애를 재현했다.
- [ ] 잘못된 Route Table association을 재현/복구했다.
- [ ] SG 문제와 Route 문제를 구분해 설명할 수 있다.
- [ ] CLI로 네트워크 연결 관계를 검증했다.

## 비용 정리와 삭제 검증

다음 Example을 바로 할 예정이면 VPC/Subnet을 유지해도 된다. 종료한다면 EC2와 VPC 관련 리소스를 정리하고 [CLI Verification Guide](../CLI_VERIFICATION.md)의 Example 05 삭제 검증을 실행한다.

---
