# Example 05 — VPC와 Public/Private Subnet 직접 만들기

기본 VPC를 쓰지 않고 직접 네트워크를 구성한다. 이번 단계부터 이전에 배운 EC2와 Security Group은 반복 작업으로 취급한다.

## Recall Check

시작 전에 기억만으로 답한다.

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

확인할 것:

- Subnet은 하나의 AZ에 속한다.
- 같은 VPC 내부 CIDR이 겹치면 안 된다.

## 3. Internet Gateway 연결

`example-05-igw`를 만들고 VPC에 Attach한다.

## 4. Public Route Table 생성

Public 전용 Route Table을 만들고 다음 경로를 추가한다.

```text
10.0.0.0/16  local
0.0.0.0/0    Internet Gateway
```

Public Subnet 2개를 이 Route Table에 association 한다.

Private Subnet은 기본 local route만 유지한다.

## 5. Public Subnet에 EC2 생성

Public Subnet 하나에 EC2를 만든다.

조건:

- Public IPv4 활성화
- HTTP 80 허용
- User Data로 nginx 실행

Public IP로 접속되는지 확인한다.

## 6. 관찰

다음 질문에 직접 답한다.

```text
Q. Public Subnet을 Public하게 만드는 핵심은 무엇인가?
Q. IGW만 VPC에 붙이고 Route가 없으면 인터넷 통신이 가능한가?
Q. Public IP만 있고 IGW route가 없으면 가능한가?
```

## 7. 장애 실험 — IGW Route 삭제

Public Route Table의 `0.0.0.0/0 -> IGW`를 잠시 삭제한다.

브라우저 요청이 어떻게 변하는지 확인하고, EC2 상태와 SG는 정상이라는 것도 확인한다.

원인을 찾은 뒤 route를 복구한다.

## 8. 장애 실험 — 잘못된 Route Table Association

Public Subnet 하나를 Private 쪽 Route Table에 association 해본다. 같은 EC2가 어떤 영향을 받는지 관찰한다.

## 9. 기억만으로 설명하기

- Public Subnet과 Private Subnet의 차이를 Route Table 기준으로 설명한다.
- SG와 Route Table의 역할 차이를 설명한다.
- `10.0.0.0/16 local`이 필요한 이유를 설명한다.

## 완료 체크

- [ ] VPC를 직접 만들었다.
- [ ] 2AZ에 Public/Private Subnet을 만들었다.
- [ ] IGW와 Public Route Table을 연결했다.
- [ ] EC2를 Public Subnet에 배치했다.
- [ ] IGW route 삭제 장애를 재현했다.
- [ ] SG 문제와 Route 문제를 구분해 설명할 수 있다.

## 비용 정리

EC2를 종료하고 필요 없는 VPC 관련 리소스를 정리한다. 다음 Example을 바로 할 예정이면 VPC/Subnet은 유지해도 된다.
