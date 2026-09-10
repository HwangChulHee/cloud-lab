# Example 08 — Auto Scaling과 장애 복구 관찰하기

이전 Example의 ALB + ASG 구조를 그대로 사용하거나 다시 만든다. 이번에는 새 서비스를 추가하기보다 **자동 복구와 scale-out이 실제로 어떻게 일어나는지** 본다.

## Recall Check
- `min / desired / max`는 각각 무엇인가?
- Target Group에서 `healthy`가 되기 전까지 새 인스턴스는 어떻게 취급되는가?
- EC2 하나가 죽으면 누가 대체 인스턴스를 만드는가?
- Target Tracking의 CPU 지표는 한 인스턴스의 CPU인가 ASG 평균인가?

## 새로 배우는 것
- Target Tracking / Step Scaling 개념
- CloudWatch Metric과 Scaling Policy 연결
- Cooldown / instance warm-up
- ASG 평균 CPU와 scale-out 조건

## 반복하는 것
- ALB / Target Group
- Launch Template / ASG
- Health Check
- EC2 장애 복구

모든 태그 가능 리소스에는 `Project=cloud-lab`, `Stage=examples`, `Example=08`을 붙인다.

## 이번에는 도움 없이
기존 리소스를 삭제했다면 VPC, ALB, Target Group, Launch Template, ASG를 요구사항만 보고 다시 구성한다.

Private EC2의 bootstrap이 외부 다운로드에 의존한다면 Example 06~07에서 사용한 NAT 또는 사전 준비 AMI 전략을 그대로 적용한다.

## 실험 A — Instance Failure Recovery
1. ASG desired=2 상태를 확인한다.
2. EC2 한 대를 terminate한다.
3. ASG Activity에서 replacement가 시작되는지 본다.
4. Target Group에서 old target 제거 → new target 등록 → healthy 흐름을 관찰한다.
5. 장애 중 ALB로 계속 요청해 서비스가 유지되는지 본다.

기록:
```text
종료 시각:
새 인스턴스 생성 시각:
healthy 전환 시각:
서비스 전체 중단 여부:
```

## 실험 B — CPU 기반 Scale-out

Target Tracking으로 평균 CPU 목표값을 실습용으로 낮게 잡는다. 예를 들어 20~30% 수준에서 시작하고 테스트 후 원래 값으로 되돌린다.

중요: Target Tracking의 `ASGAverageCPUUtilization`은 **ASG 전체 인스턴스의 평균 CPU**를 본다. 한 대만 100%여도 다른 인스턴스가 낮으면 평균이 목표값을 넘지 않을 수 있다.

따라서 가능하면 **ASG의 모든 인스턴스에 비슷한 CPU 부하를 준다.** 패키지 설치 없이 사용할 수 있는 예:

```bash
yes > /dev/null &
```

필요하면 CPU 수에 맞춰 여러 개 실행한다. 종료:

```bash
pkill yes
```

다음 흐름을 관찰한다.

```text
ASG 평균 CPU 상승
→ CloudWatch Metric 상승
→ Target Tracking Policy 판단
→ ASG Desired Capacity 증가
→ EC2 생성
→ bootstrap
→ Target Group 등록
→ healthy
```

실습 비용과 시간을 줄이기 위해 max는 3~4 정도로 제한한다.

## 실험 C — Scale-in
부하를 제거한 후 시간이 지나면서 desired가 줄어드는지 본다. 즉시 줄지 않는 이유를 cooldown/warm-up/metric 안정화 관점에서 생각한다.

## 장애 분석 질문
- 한 EC2 CPU는 100%인데 ASG가 scale-out하지 않았다. 평균 CPU는 얼마였는가?
- 평균 CPU가 목표보다 높은데 scale-out이 안 됐다. Policy와 Activity에서 무엇을 볼까?
- 새 EC2는 생성됐는데 계속 unhealthy다. bootstrap/NAT/SG/health check 중 무엇을 어떻게 확인할까?
- ASG가 계속 늘었다 줄었다 반복하면 어떤 설정을 의심할까?

## CLI 구축/장애 검증
[CLI Verification Guide](../CLI_VERIFICATION.md)의 Example 08 명령을 실행한다. Scaling Activity의 `Cause`와 `Description`을 함께 확인한다.

## 기억만으로 설명하기
`Metric → Target Tracking Policy → ASG → EC2 → bootstrap → Target Group → ALB` 흐름을 그림 없이 설명한다.

## 완료 체크
- [ ] EC2 강제 종료 후 replacement를 관찰했다.
- [ ] Scaling Policy를 설정했다.
- [ ] ASG 평균 CPU라는 의미를 확인했다.
- [ ] 전체 인스턴스에 부하를 만들어 scale-out을 확인했다.
- [ ] scale-in까지 관찰했다.
- [ ] ASG Activity와 CloudWatch Metric을 함께 볼 수 있다.

## 비용 정리
테스트용 인스턴스 수를 원복하거나 ASG/ALB를 삭제한다. NAT를 사용했다면 NAT Gateway와 EIP도 함께 정리한다.

삭제 후 CLI 삭제 검증을 실행한다.
