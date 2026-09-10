# 64. VPC Endpoint / PrivateLink

`examples/06`, `11`, `12`에서 private EC2가 AWS 서비스에 접근하는 구조를 이해하기 위한 챕터다.

## 1. 왜 필요한가?

Private subnet의 EC2가 S3 같은 AWS 서비스에 접근한다고 해서 반드시 인터넷이나 NAT Gateway를 경유해야 하는 것은 아니다.

VPC Endpoint를 사용하면 VPC 내부에서 AWS 서비스로 사설 경로를 만들 수 있다.

```text
Private EC2
   ↓
VPC Endpoint
   ↓
AWS Service
```

## 2. Gateway Endpoint

Gateway Endpoint는 대표적으로 S3, DynamoDB 접근에 사용한다.

route table에 endpoint 경로가 추가된다.

개념적으로:

```text
Private Subnet Route Table

VPC CIDR       → local
S3 prefix list → Gateway Endpoint
```

S3 접근 때문에 NAT Gateway를 사용하던 경우라면 Gateway Endpoint를 통해 NAT 경유 비용과 인터넷 경로 의존을 줄일 수 있다.

## 3. Interface Endpoint

Interface Endpoint는 AWS PrivateLink를 기반으로 하며 VPC 안에 ENI를 생성해 AWS 서비스 또는 PrivateLink 서비스에 접근한다.

```text
Private EC2
   ↓ private IP
Interface Endpoint ENI
   ↓
AWS Service
```

Interface Endpoint에는 Security Group을 연결할 수 있다.

Session Manager처럼 private EC2가 특정 AWS API endpoint에 접근해야 하는 경우 NAT 대신 필요한 Interface Endpoint들을 구성하는 방식을 고려할 수 있다.

## 4. Gateway vs Interface

```text
Gateway Endpoint
- Route Table 기반
- S3 / DynamoDB
- NAT 없이 해당 서비스 접근

Interface Endpoint
- ENI / private IP 기반
- PrivateLink 사용
- 많은 AWS 서비스에서 사용
- Security Group 적용 가능
```

## 5. Endpoint Policy

Endpoint를 만들었다고 모든 API 동작을 자동으로 허용해야 하는 것은 아니다.

접근 제어는 다음 요소들이 함께 결정할 수 있다.

```text
IAM Policy
Resource Policy (예: S3 Bucket Policy)
Endpoint Policy
Security Group (Interface Endpoint인 경우)
```

`AccessDenied`가 발생하면 네트워크 연결과 IAM 권한 문제를 구분해야 한다.

## 6. NAT와 비교하기

S3 접근만 필요한 private EC2라면:

```text
방법 A
EC2 → NAT Gateway → AWS public endpoint → S3

방법 B
EC2 → Gateway Endpoint → S3
```

실습에서 중요한 것은 무조건 endpoint를 쓰는 것이 아니라 **왜 경로를 선택했는지 설명하는 것**이다.

## 7. Recall Check

- VPC Endpoint를 사용하면 어떤 네트워크 경로를 줄일 수 있는가?
- S3에는 어떤 종류의 endpoint를 우선 떠올릴 수 있는가?
- Interface Endpoint와 Gateway Endpoint의 차이는?
- Endpoint가 정상인데 `AccessDenied`가 날 수 있는 이유는?

## 8. 완료 기준

- [ ] VPC Endpoint의 목적을 설명할 수 있다.
- [ ] Gateway / Interface Endpoint 차이를 설명할 수 있다.
- [ ] S3 접근에서 NAT와 Gateway Endpoint를 비교할 수 있다.
- [ ] Endpoint Policy와 IAM/Resource Policy가 별개의 접근 제어 계층임을 이해한다.
