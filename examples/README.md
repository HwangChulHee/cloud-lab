# AWS Guided Examples

`labs/`에 들어가기 전에, AWS 콘솔에서 직접 따라 만들면서 서비스의 역할과 연결 방식을 익히는 단계다.

Lab이 **상황을 보고 스스로 설계하는 문제**라면, Example은 **정해진 구조를 그대로 구축하고 관찰하는 실습**이다.

> 따라 만들기 → 요청 보내기 → AWS 콘솔에서 관찰하기 → 일부러 망가뜨리기 → 다시 복구하기

## 목적

- AWS 콘솔에 익숙해진다.
- 서비스 이름만 외우지 않고 실제 연결 관계를 본다.
- Security Group, Target Group, Health Check, DNS 등 추상적인 개념을 실제 리소스로 확인한다.
- 나중에 `labs/`에서 설계 문제를 풀기 위한 재료를 만든다.

## 진행 원칙

1. 처음에는 Console 중심으로 진행한다.
2. 각 단계에서 "왜 이 설정을 하는지"를 확인한다.
3. 구축만 하고 끝내지 않고 반드시 요청을 보내 결과를 본다.
4. 가능하면 일부 리소스를 정지/변경해 장애를 재현한다.
5. 실습 후 리소스를 삭제해 비용을 정리한다.
6. Terraform은 SAA 이후 같은 예제를 다시 구현하는 용도로 사용한다.

## 현재 예제

- [ ] [01. EC2 한 대에 웹 서버 띄우기](./01-single-ec2-web/README.md)
- [ ] [02. EC2 두 대를 ALB 뒤에 연결하기](./02-alb-two-ec2/README.md)
- [ ] [03. ALB Health Check와 장애 격리 확인하기](./03-alb-health-check/README.md)
- [ ] [04. Security Group을 계층별로 나누기](./04-security-group-layering/README.md)

## 이후 추가할 예제

학습 진도에 맞춰 아래 예제를 순차적으로 추가한다.

- Auto Scaling Group + ALB
- RDS를 Private Subnet에 배치하고 EC2에서만 접속
- Route 53 + ACM + HTTPS
- S3 파일 업로드
- CloudFront + S3
- SQS + Worker
- CloudWatch Alarm
- ECS/Fargate 배포

## Examples와 Labs의 차이

| 구분 | Examples | Labs |
| --- | --- | --- |
| 목적 | 사용법/원리 익히기 | 설계 판단 연습 |
| 구조 | 정답 구조를 보고 따라 함 | 정답을 먼저 보지 않음 |
| 진행 | 단계별 가이드 | 요구사항만 제공 |
| 실패 실험 | 지정된 장애를 재현 | 스스로 장애 시나리오를 판단 |
| 난이도 | 낮음 → 중간 | 중간 → 높음 |

권장 순서는 다음과 같다.

```text
SAA 개념 학습
   ↓
Guided Example
   ↓
개념 복습
   ↓
Scenario Lab
   ↓
SAA 이후 Terraform으로 재구축
```
