# Example 07 — ALB + Auto Scaling Group

수동으로 EC2 두 대를 만들던 구조를 Launch Template과 Auto Scaling Group으로 바꾼다.

## Recall Check
- ALB Listener → Target Group → EC2 흐름은?
- EC2-SG가 ALB-SG만 허용하도록 어떻게 설정했나?
- 서로 다른 AZ를 쓰는 이유는?

## 새로 배우는 것
- Launch Template
- Auto Scaling Group
- Min / Desired / Max
- ASG와 Target Group 자동 등록

## 반복하는 것
VPC, Public/Private Subnet, ALB, Target Group, EC2 Security Group, User Data를 다시 사용한다.

## 이번에는 도움 없이
ALB, Target Group, ALB-SG, EC2-SG는 이전 예제의 상세 절차를 보지 않고 만든다.

## 목표 구조
```text
Internet
  ↓
ALB
  ↓
Target Group
  ↓
ASG
├─ EC2-A
└─ EC2-B
```

## 구축
1. Launch Template을 만든다. AMI, instance type, EC2-SG, User Data를 지정한다.
2. ASG를 만들고 Private Subnet 2개를 선택한다.
3. `min=2`, `desired=2`, `max=4`로 시작한다.
4. 기존 Target Group에 ASG를 연결한다.
5. 두 인스턴스가 자동 생성되고 Target Group에서 healthy가 되는지 확인한다.
6. ALB DNS로 반복 요청해 두 인스턴스의 응답을 확인한다.

## 관찰
- 사람이 EC2를 직접 등록하지 않았는데 Target이 추가된 이유는?
- Launch Template과 ASG의 역할 차이는?
- Desired Capacity를 3으로 바꾸면 어떤 순서로 변화하는가?

## 장애 실험
EC2 한 대를 직접 terminate한다. 다음 흐름을 관찰한다.
```text
instance 종료
→ desired보다 실제 수 감소
→ ASG가 새 instance 생성
→ Target Group 등록
→ Health Check
→ healthy
```

## 기억만으로 설명하기
- ALB가 고가용성을 만들고 ASG가 확장성을 만든다는 표현은 어디까지 맞는가?
- EC2가 죽었을 때 누가 새 EC2를 만드는가?
- 새 EC2가 만들어졌다고 바로 트래픽을 받는가?

## 완료 체크
- [ ] Launch Template을 만들었다.
- [ ] 2AZ ASG를 만들었다.
- [ ] Target Group 자동 등록을 확인했다.
- [ ] Desired Capacity 변경을 관찰했다.
- [ ] EC2 강제 종료 후 자동 복구를 확인했다.
- [ ] ALB와 ASG의 역할을 구분해 설명할 수 있다.

## 비용 정리
ALB와 ASG를 삭제하면 ASG의 EC2도 함께 정리되는지 확인한다.
