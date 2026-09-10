# Example 07 — ALB + Auto Scaling Group

수동으로 EC2 두 대를 만들던 구조를 Launch Template과 Auto Scaling Group으로 바꾼다. 이번 예제부터는 **ASG가 새 인스턴스를 언제든 다시 만들 수 있으므로 bootstrap이 반복 가능해야 한다.**

## Recall Check
- ALB Listener → Target Group → EC2 흐름은?
- EC2-SG가 ALB-SG만 허용하도록 어떻게 설정했나?
- 서로 다른 AZ를 쓰는 이유는?
- Private EC2에서 `dnf install`이 필요하면 어떤 outbound 경로가 필요한가?

## 새로 배우는 것
- Launch Template
- Auto Scaling Group
- Min / Desired / Max
- ASG와 Target Group 자동 등록
- 반복 가능한 bootstrap

## 반복하는 것
VPC, Public/Private Subnet, ALB, Target Group, EC2 Security Group, User Data를 다시 사용한다.

모든 태그 가능 리소스에는 `Project=cloud-lab`, `Stage=examples`, `Example=07`을 붙인다.

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
├─ EC2-A (private)
└─ EC2-B (private)
```

## Bootstrap 사전 조건

Launch Template의 User Data가 외부 저장소에서 패키지를 설치한다면 Private Subnet에 NAT Gateway가 필요하다.

이번 예제에서는 다음 중 하나를 선택한다.

```text
A. NAT Gateway 유지 + User Data에서 nginx 설치
B. Example 06에서 만든 nginx 포함 AMI 사용
C. 외부 다운로드가 필요 없는 사전 준비 AMI 사용
```

ASG replacement가 발생할 때마다 같은 bootstrap이 재현되어야 한다.

## 구축
1. Launch Template을 만든다. AMI, instance type, EC2-SG, User Data 또는 사전 준비 AMI를 지정한다.
2. ASG를 만들고 서로 다른 AZ의 Private Subnet 2개를 선택한다.
3. `min=2`, `desired=2`, `max=4`로 시작한다.
4. 기존 Target Group에 ASG를 연결한다.
5. 두 인스턴스가 자동 생성되고 Target Group에서 healthy가 되는지 확인한다.
6. ALB DNS로 반복 요청해 두 인스턴스의 응답을 확인한다.

## 관찰
- 사람이 EC2를 직접 등록하지 않았는데 Target이 추가된 이유는?
- Launch Template과 ASG의 역할 차이는?
- Desired Capacity를 3으로 바꾸면 어떤 순서로 변화하는가?
- replacement 인스턴스도 동일한 User Data/AMI로 정상 기동되는가?

## 장애 실험 A — EC2 한 대 강제 종료
EC2 한 대를 직접 terminate한다.

```text
instance 종료
→ desired보다 실제 수 감소
→ ASG가 새 instance 생성
→ bootstrap
→ Target Group 등록
→ Health Check
→ healthy
```

새 인스턴스가 계속 unhealthy라면 다음 순서로 본다.

```text
Launch Template
→ AMI/User Data
→ outbound/NAT
→ Security Group
→ app process
→ Health Check path/port
```

## 장애 실험 B — Bootstrap 실패
가능하면 테스트용 Launch Template version에서 User Data 패키지 설치 명령이나 시작 명령을 일부러 잘못 설정하고 replacement를 유도한다.

ASG는 EC2를 생성했지만 애플리케이션이 준비되지 않으면 Target이 healthy가 되지 않는다는 것을 확인한다. 실험 후 정상 Launch Template version으로 복구한다.

## 기억만으로 설명하기
- ALB가 고가용성을 만들고 ASG가 확장성을 만든다는 표현은 어디까지 맞는가?
- EC2가 죽었을 때 누가 새 EC2를 만드는가?
- 새 EC2가 만들어졌다고 바로 트래픽을 받는가?
- Private Subnet에서 replacement가 bootstrap에 실패하면 어디를 볼 것인가?

## CLI 구축 검증
[CLI Verification Guide](../CLI_VERIFICATION.md)의 Example 07 명령을 실행한다.

## 완료 체크
- [ ] Launch Template을 만들었다.
- [ ] 2AZ ASG를 만들었다.
- [ ] Target Group 자동 등록을 확인했다.
- [ ] Desired Capacity 변경을 관찰했다.
- [ ] EC2 강제 종료 후 자동 복구를 확인했다.
- [ ] replacement 인스턴스의 bootstrap까지 확인했다.
- [ ] ALB와 ASG의 역할을 구분해 설명할 수 있다.

## 비용 정리
ASG를 먼저 삭제해 관리 대상 EC2가 정리되는지 확인한 뒤 ALB, Target Group, Launch Template, NAT Gateway/EIP 등을 정리한다.

삭제 후 CLI 삭제 검증을 실행한다.
