# 61. Internet Gateway와 NAT Gateway

## 1. Internet Gateway

Internet Gateway(IGW)는 VPC와 인터넷 사이의 게이트웨이다.

Public subnet의 전형적인 route:

```text
0.0.0.0/0 → Internet Gateway
```

하지만 이 route만 있다고 EC2가 자동으로 인터넷에 노출되는 것은 아니다. EC2가 public IPv4/EIP를 가지고 있어야 하고 Security Group/NACL도 허용해야 한다.

## 2. NAT Gateway

Private subnet의 EC2가 인터넷으로 outbound 통신은 해야 하지만 인터넷에서 직접 inbound를 받을 필요가 없을 때 NAT Gateway를 사용할 수 있다.

```text
Private EC2
   ↓
Private Route Table
0.0.0.0/0 → NAT Gateway
   ↓
Public Subnet
   ↓
Internet Gateway
   ↓
Internet
```

NAT Gateway는 public subnet에 배치하고 Elastic IP를 사용한다.

## 3. IGW와 NAT의 차이

```text
IGW
VPC와 인터넷을 연결
Public subnet의 인터넷 경로에 사용

NAT Gateway
Private subnet 인스턴스의 outbound 인터넷 접근 지원
인터넷에서 private EC2로 직접 연결하는 용도가 아님
```

## 4. 실습에서 왜 필요한가?

`examples/06`에서 EC2를 private subnet에 두면 public IP 없이도 ALB를 통해 사용자 요청을 받을 수 있다.

하지만 EC2가 다음 작업을 해야 한다면 별도 outbound 경로가 필요할 수 있다.

```text
패키지 다운로드
외부 API 호출
AWS public endpoint 접근
```

이때 NAT Gateway 또는 특정 AWS 서비스에 대한 VPC Endpoint를 고려한다.

## 5. 고가용성과 비용

운영 환경에서 여러 AZ를 사용할 때 NAT Gateway도 AZ 단위 장애를 고려해 AZ별 배치를 검토한다.

NAT Gateway는 시간당 비용과 처리 데이터 비용이 있으므로 단순 실습에서는 오래 유지하지 않는다. S3/DynamoDB와 같이 Gateway Endpoint를 제공하는 서비스는 endpoint를 이용해 NAT 경유를 줄일 수 있다.

## 6. 장애 진단

Private EC2에서 인터넷이 안 될 때:

```text
1. Private Route Table에 0.0.0.0/0 → NAT가 있는가?
2. NAT Gateway가 Available인가?
3. NAT가 public subnet에 있는가?
4. NAT subnet의 route가 IGW를 향하는가?
5. SG/NACL outbound가 막혀 있지 않은가?
```

## 7. Recall Check

- IGW와 NAT Gateway 역할 차이는?
- NAT Gateway는 왜 public subnet에 두는가?
- private EC2에 public IP가 없어도 인터넷 outbound가 가능한 이유는?
- S3 접근만 필요한 private EC2라면 NAT 외에 무엇을 고려할 수 있는가?

## 8. 완료 기준

- [ ] IGW를 public subnet route와 연결해서 설명할 수 있다.
- [ ] NAT Gateway의 요청 흐름을 그릴 수 있다.
- [ ] private EC2 outbound 장애의 확인 순서를 말할 수 있다.
- [ ] NAT와 VPC Endpoint의 비용/경로 관점 차이를 이해한다.
