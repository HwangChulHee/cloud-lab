# 56. Systems Manager — Session Manager 중심

`examples/06-private-ec2-access`를 하기 전에 필요한 Systems Manager 핵심만 정리한다.

## 1. 왜 필요한가?

Private Subnet의 EC2는 public IP가 없을 수 있다. 그렇다고 운영자가 반드시 Bastion Host를 두고 SSH 22번 포트를 열어야 하는 것은 아니다.

Session Manager를 사용하면 AWS Systems Manager를 통해 EC2에 관리 세션을 열 수 있다.

```text
Operator
  ↓ AWS Console / CLI
Systems Manager Session Manager
  ↓
Private EC2
```

## 2. 필요한 구성 요소

핵심 조건은 다음 세 가지다.

```text
EC2
├─ SSM Agent
├─ IAM Role
└─ Systems Manager endpoint에 도달 가능한 네트워크 경로
```

IAM Role에는 Systems Manager가 인스턴스를 관리하는 데 필요한 권한이 있어야 한다.

네트워크 측에서는 EC2가 Systems Manager 관련 AWS endpoint와 통신할 수 있어야 한다. 실습 환경에서는 NAT Gateway를 통한 outbound 경로를 사용하거나, 더 사설적인 구성에서는 VPC Interface Endpoint를 사용할 수 있다.

## 3. SSH와 비교

```text
SSH
Client → EC2 :22
키 관리 필요
네트워크 inbound 경로 필요

Session Manager
Client → AWS 관리 평면 → EC2
EC2의 22 inbound를 열 필요가 없음
IAM 기반 접근 통제 가능
```

핵심은 `private EC2 = 접근 불가능`이 아니라는 것이다.

## 4. 실습에서 확인할 것

`examples/06`에서 다음을 직접 확인한다.

- EC2에 public IP가 없어도 Session Manager 세션을 열 수 있는가?
- EC2-SG에 SSH 22 inbound가 없어도 되는가?
- EC2의 IAM Role을 제거하면 어떤 증상이 생기는가?
- outbound 경로가 끊기면 Session Manager 연결은 어떻게 되는가?

## 5. 장애 진단 순서

Session Manager 연결 실패 시 무작정 SG의 22번을 열지 않는다.

```text
1. 인스턴스가 Systems Manager Managed Node로 보이는가?
2. SSM Agent가 동작하는가?
3. EC2 IAM Role이 올바른가?
4. AWS endpoint로 나갈 네트워크 경로가 있는가?
5. NAT 또는 필요한 VPC Endpoint가 정상인가?
```

## 6. Recall Check

- Session Manager를 쓰면 왜 SSH inbound 22가 필요하지 않은가?
- EC2 IAM Role은 왜 필요한가?
- private subnet EC2가 AWS API endpoint에 접근하려면 어떤 방법들이 있는가?
- NAT가 없더라도 VPC Endpoint로 해결할 수 있는 경우는 무엇인가?

## 7. 완료 기준

- [ ] Private EC2 운영 접근 문제를 설명할 수 있다.
- [ ] Session Manager와 SSH의 차이를 설명할 수 있다.
- [ ] SSM Agent / IAM Role / 네트워크 경로의 역할을 구분할 수 있다.
- [ ] 연결 실패 시 확인 순서를 말할 수 있다.
