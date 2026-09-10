# Example 06 — EC2를 Private Subnet에 배치하기

이제 웹 서버를 인터넷에 직접 노출하지 않고 ALB를 통해서만 접근하도록 바꾼다.

## Recall Check

- Public Subnet의 조건은 무엇이었나?
- ALB-SG → EC2-SG Reference는 어떻게 구성했나?
- ALB Listener와 Target Group의 관계는?

## 새로 배우는 것

- Private Subnet의 실제 의미
- Public ALB + Private EC2 구조
- Private EC2의 outbound 경로
- NAT Gateway와 Session Manager의 역할

## 반복하는 것

- VPC / Subnet / Route Table
- ALB / Target Group
- EC2 / Security Group

## 이번에는 도움 없이

다음은 이전 README를 보지 않고 먼저 구성한다.

- ALB-SG: 80 from `0.0.0.0/0`
- EC2-SG: 80 from ALB-SG
- Target Group과 Listener 연결

## 목표 구조

```text
Internet
   ↓
Public Subnet
   ALB
   ↓
Private Subnet
   EC2
```

## 1. 네트워크 준비

Example 05의 VPC를 재사용하거나 동일 구조를 다시 만든다.

- Public Subnet 2개
- Private Subnet 2개
- Public RT: `0.0.0.0/0 -> IGW`
- Private RT: 인터넷 경로 없음

## 2. ALB 생성

Internet-facing ALB를 두 Public Subnet에 배치한다. Target Group은 HTTP 80을 사용한다.

## 3. Private EC2 생성

EC2를 Private Subnet에 만들고 Public IPv4를 비활성화한다. nginx가 실행되도록 User Data를 설정한다.

EC2-SG는 ALB-SG에서 오는 80만 허용한다.

## 4. 요청 확인

ALB DNS 이름으로 접속한다.

```text
Client → ALB(public) → EC2(private)
```

EC2에 Public IP가 없어도 서비스가 가능한 이유를 설명한다.

## 5. 직접 접근 불가 확인

EC2 상세 화면에서 Public IPv4가 없는지 확인한다. 인터넷에서 EC2로 직접 들어갈 주소 자체가 없다는 점을 이전 Example 04의 SG 차단 방식과 비교한다.

## 6. Private EC2의 outbound 생각하기

Private EC2가 OS 패키지 다운로드 등 인터넷 outbound가 필요하다면 NAT Gateway 같은 경로가 필요하다.

선택 실습:

- Public Subnet에 NAT Gateway 생성
- Private RT에 `0.0.0.0/0 -> NAT Gateway` 추가
- Private EC2에서 outbound 동작 확인

비용이 발생하므로 개념 확인 후 즉시 삭제한다.

## 7. 관리 접근

SSH 22를 인터넷에 열지 않는 방향을 생각한다. Session Manager를 사용할 수 있다면 IAM Role과 SSM을 이용해 접속해본다.

## 8. 장애 실험 — Private Route 변경

Private EC2의 서비스 요청은 ALB에서 VPC 내부로 들어오므로 인터넷 route와 별개다. NAT route를 제거했을 때 **사용자의 ALB 요청**과 **EC2의 인터넷 outbound**가 각각 어떻게 되는지 비교한다.

## 9. 기억만으로 설명하기

- Public ALB가 Private EC2에 요청을 전달할 수 있는 이유는?
- Private EC2가 인터넷 outbound를 하려면 무엇이 필요한가?
- SG와 NAT의 역할은 어떻게 다른가?
- EC2에 Public IP를 주지 않는 보안상 이점은?

## 완료 체크

- [ ] ALB를 Public Subnet에 배치했다.
- [ ] EC2를 Private Subnet에 배치했다.
- [ ] EC2에 Public IP가 없음을 확인했다.
- [ ] ALB를 통해 서비스가 정상 동작했다.
- [ ] NAT/SSM이 왜 필요한지 설명할 수 있다.
- [ ] 인터넷 inbound와 outbound 경로를 구분할 수 있다.

## 비용 정리

ALB, EC2, NAT Gateway를 사용했다면 실습 후 삭제한다.
