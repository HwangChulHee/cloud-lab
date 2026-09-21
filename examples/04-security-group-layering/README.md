# Example 04 — Security Group을 계층별로 나누기

Example 02~03의 구조를 그대로 사용한다. 이제 EC2의 HTTP 포트를 인터넷 전체에 열지 않고, **ALB를 통해 들어온 요청만 EC2가 받도록** 변경한다.

```text
Internet
   ↓ TCP 80
ALB-SG
   ↓ TCP 80, source = ALB-SG
EC2-SG
```

Example 02의 리소스를 재사용한다면 기존 태그는 유지한다. 이 예제에서 새 SG나 리소스를 별도로 만들 경우 다음 규칙을 적용한다.

```text
Project=cloud-lab
Stage=examples
Example=04
Name=example-04-*
```

## 목표

- Security Group Reference를 실제로 사용한다.
- IP/CIDR 허용과 Security Group 참조의 차이를 이해한다.
- 사용자는 ALB에는 접근할 수 있지만 EC2에는 직접 접근할 수 없는 구조를 만든다.
- 계층별 접근 제어가 왜 필요한지 체감한다.

## 1. 현재 구조 확인

Example 02에서 EC2 Security Group이 인터넷 전체의 HTTP 요청을 허용하는 상태라면, EC2 Public IP를 알고 있는 사용자는 ALB를 우회할 수 있다. EC2 직접 접근과 ALB 접근을 각각 확인한다.

## 2. ALB Security Group

ALB-SG는 인터넷 사용자의 HTTP 요청을 받을 수 있게 유지한다.

## 3. EC2 Security Group 수정

EC2-SG의 기존 HTTP rule을 삭제하고 source에 IP/CIDR이 아니라 ALB-SG를 지정한다.

```text
HTTP TCP 80 Source: ALB-SG
```

## 4. ALB를 통한 요청 확인

```text
Client
  ↓
ALB-SG가 Client 요청 허용
  ↓
ALB
  ↓
EC2-SG가 ALB-SG에서 온 트래픽 허용
  ↓
EC2
```

ALB DNS로는 정상 응답해야 한다.

## 5. EC2 직접 접근 확인

EC2 Public IP로 직접 접속한다. 접속 실패 또는 timeout이 예상된다. EC2에 Public IP가 있어도 HTTP source가 ALB-SG로 제한되어 있기 때문이다.

## 6. 구조 비교

```text
나쁜 구조
User ─────────→ EC2
  └→ ALB ─────→ EC2

개선 구조
User → ALB → EC2
User ──X──→ EC2
```

## 7. 왜 IP 대신 Security Group Reference인가?

특정 IP를 허용하는 것보다 "ALB 계층에서 온 트래픽만 허용"한다는 의도를 정책에 직접 표현할 수 있다. ALB 내부 IP가 바뀌거나 EC2가 추가·교체되어도 동일한 SG 관계를 유지할 수 있다.

## 8. SSH도 분리하기

SSH가 필요하더라도 인터넷 전체에 열지 않는다. 실습에서는 자신의 공인 IP로 제한하고, 이후에는 Systems Manager Session Manager 같은 운영 접근 방식을 다룬다.

## 9. 장애 실험 — ALB → EC2 허용 제거

EC2-SG의 `HTTP 80 Source: ALB-SG` rule을 잠시 삭제한다.

```text
Client → ALB   도달 가능
ALB → EC2      차단
```

Target Group Health Check가 실패하고 Target이 unhealthy가 되는지 확인한 뒤 rule을 복구한다.

## 10. CLI 구축/장애 검증

[CLI Verification Guide](../CLI_VERIFICATION.md)의 Example 04 명령을 실행한다.

다음을 출력만 보고 설명할 수 있어야 한다.

```text
ALB-SG: client HTTP 허용
EC2-SG: app port source = ALB-SG
EC2-SG에 인터넷 전체를 source로 둔 app rule 없음
```

장애 실험 전/중/복구 후 SG rule과 Target Health를 비교한다.

## 11. 완료 체크

- [ ] ALB-SG와 EC2-SG를 구분했다.
- [ ] ALB는 인터넷에서 접근 가능하다.
- [ ] EC2 HTTP source를 ALB-SG로 제한했다.
- [ ] ALB DNS를 통한 요청은 성공한다.
- [ ] EC2 Public IP 직접 요청은 실패한다.
- [ ] EC2-SG rule 제거로 Health Check 실패를 관찰했다.
- [ ] Security Group Reference의 의미를 설명할 수 있다.
- [ ] CLI로 SG 관계를 검증했다.

## 12. 비용 정리와 삭제 검증

Example 05에서는 새 VPC를 만들 예정이므로 02~04 리소스를 더 이상 쓰지 않는다면 정리한다. Example 02 삭제 검증을 다시 실행해 ALB, Target Group, EC2가 남지 않았는지 확인한다. 이 예제에서 별도로 생성한 SG도 다른 리소스에 연결되어 있지 않다면 삭제한다.

---

## 로컬 CLI 검증 가이드

### Example 04 CLI — Security Group Reference가 실제로 어떻게 보이는가

Example 02 리소스를 재사용했다면 태그보다 **실제 SG ID를 직접 지정**하는 편이 명확하다.

\`\`\`bash
export ALB_SG_ID=<alb-security-group-id>
export EC2_SG_ID=<ec2-security-group-id>

aws ec2 describe-security-groups --region $AWS_REGION \
  --group-ids $ALB_SG_ID $EC2_SG_ID \
  --query 'SecurityGroups[].{Name:GroupName,Id:GroupId,Ingress:IpPermissions}'
\`\`\`

여기서 중요한 것은 EC2-SG의 \`IpPermissions\` 안에 source CIDR 대신 **ALB Security Group ID**가 보이는지 확인하는 것이다.

\`\`\`text
나쁜 상태
EC2-SG :80 source = 0.0.0.0/0

의도한 상태
EC2-SG :80 source = sg-... (ALB-SG)
\`\`\`

SG rule을 제거한 뒤 Target 상태도 같이 본다.

\`\`\`bash
export TG_ARN=<target-group-arn>

aws elbv2 describe-target-health --region $AWS_REGION \
  --target-group-arn $TG_ARN \
  --query 'TargetHealthDescriptions[].{Target:Target.Id,State:TargetHealth.State,Reason:TargetHealth.Reason}' \
  --output table
\`\`\`

이 두 명령을 함께 보면 **설정 변화(SG) → 결과 변화(Target Health)**를 연결해서 볼 수 있다.
