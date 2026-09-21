# Example 03 — ALB Health Check와 장애 격리 확인하기

Example 02에서 만든 ALB + EC2 두 대 구조를 그대로 사용한다.

```text
                ┌→ EC2-A
User → ALB → Target Group
                └→ EC2-B
```

이번에는 EC2 하나의 웹 서버를 일부러 중지하고 ALB가 어떻게 반응하는지 관찰한다.

> Example 02의 리소스를 재사용한다면 기존 `Example=02` 태그를 억지로 바꾸지 않는다. 이 예제에서 새 리소스를 만든다면 `Project=cloud-lab`, `Stage=examples`, `Example=03`을 적용한다.

## 목표

- ALB Health Check가 실제로 무엇을 하는지 확인한다.
- healthy / unhealthy 상태가 바뀌는 과정을 본다.
- 장애 난 서버로 신규 요청이 전달되지 않는 것을 확인한다.
- 복구 후 다시 Target으로 편입되는 것을 확인한다.

## 1. 시작 상태 확인

Target Group → Targets에서 두 EC2가 모두 `healthy`인지 확인한다.

```text
EC2-A: healthy
EC2-B: healthy
```

ALB DNS 이름으로 여러 번 요청해 두 서버가 모두 응답하는 것도 확인한다.

## 2. Health Check 설정 확인

Target Group → Health checks에서 다음 항목을 직접 확인한다.

```text
Protocol
Port
Health check path
Healthy threshold
Unhealthy threshold
Timeout
Interval
Success codes
```

예를 들어 Health check path가 `/`라면 ALB는 각 Target의 `/`에 주기적으로 요청을 보내 정상 여부를 판단한다.

## 3. EC2-A의 nginx 중지

```bash
sudo systemctl stop nginx
```

바로 Target Group 화면을 새로고침한다. 처음에는 아직 `healthy`로 보일 수 있다. 왜 즉시 unhealthy가 되지 않는지 threshold/interval 관점에서 생각한다.

## 4. 상태 변화 관찰

```text
healthy
  ↓
unhealthy
```

Health Check는 한 번 실패했다고 바로 서버를 제거하는 것이 아니라 설정된 임계값에 따라 상태를 판단한다.

## 5. ALB 요청 계속 보내기

EC2-A가 unhealthy가 된 뒤 ALB DNS로 여러 번 요청한다.

정상 Target이 하나 이상 남아 있다면 신규 요청이 정상 Target으로 전달되는지 확인한다.

```text
서버 장애
≠
서비스 전체 장애
```

## 6. EC2-A 복구

```bash
sudo systemctl start nginx
```

Target Group 상태가 `unhealthy → healthy`로 돌아오는지 확인한다. Healthy threshold를 만족해야 다시 정상 Target으로 판단된다.

## 7. Health Check endpoint 분리 실험

nginx에 간단한 health endpoint를 만든다.

```bash
sudo mkdir -p /usr/share/nginx/html/health
sudo bash -c 'echo OK > /usr/share/nginx/html/health/index.html'
```

`/health/`가 200으로 응답되는지 확인하고 Target Group Health Check path를 `/health/`로 변경한다.

## 8. 잘못된 Health Check 실험

Health Check path를 존재하지 않는 경로로 잠시 바꾼다.

```text
/does-not-exist
```

예상:

```text
EC2 정상
nginx 정상
하지만 ALB 기준 Target unhealthy
```

확인 후 정상 경로로 복구한다.

## 9. CLI 구축/장애 검증

[CLI Verification Guide](../CLI_VERIFICATION.md)의 Example 03 명령을 실행한다.

장애 전/중/복구 후 같은 명령을 반복해서 다음을 비교한다.

```text
HealthCheckPath
Healthy/Unhealthy threshold
TargetHealth.State
TargetHealth.Reason
```

## 10. 직접 설명하기

- ALB는 서버 프로세스가 죽었다는 사실을 어떻게 알까?
- 왜 한 번 실패했다고 바로 unhealthy로 만들지 않을까?
- Health Check endpoint가 너무 무거우면 어떤 문제가 생길까?
- 애플리케이션은 정상인데 잘못된 Health Check 때문에 서비스에서 제외될 수 있는 이유는?

## 11. 완료 체크

- [ ] 두 Target이 healthy인 상태에서 시작했다.
- [ ] nginx를 중지하고 unhealthy 전환을 관찰했다.
- [ ] 정상 Target으로만 요청이 가는 것을 확인했다.
- [ ] nginx 복구 후 healthy 전환을 확인했다.
- [ ] 별도 Health Check path를 구성했다.
- [ ] 잘못된 Health Check가 정상 서버를 제외할 수 있음을 확인했다.
- [ ] CLI로 장애 전/중/복구 상태를 비교했다.

## 12. 다음 단계 / 비용 정리

Example 04를 바로 진행한다면 Example 02의 리소스를 유지한다. 여기서 종료한다면 Example 02의 삭제 검증 절차로 ALB, Target Group, EC2, SG를 정리하고 잔존 리소스를 확인한다.

---

## 로컬 CLI 검증 가이드

### Example 03 CLI — Health Check 장애를 상태값으로 확인하기

Example 03은 새 리소스를 많이 만드는 예제가 아니라 **같은 CLI를 장애 전/중/복구 후 반복 실행하는 것**이 핵심이다.

\`\`\`bash
export TG_ARN=<target-group-arn>

aws elbv2 describe-target-groups --region $AWS_REGION \
  --target-group-arns $TG_ARN \
  --query 'TargetGroups[].{Path:HealthCheckPath,Interval:HealthCheckIntervalSeconds,Timeout:HealthCheckTimeoutSeconds,Healthy:HealthyThresholdCount,Unhealthy:UnhealthyThresholdCount,Matcher:Matcher.HttpCode}'
\`\`\`

이 명령은 ALB가 Target을 어떤 규칙으로 판단하는지 보여준다.

- \`HealthCheckPath\`: 어느 URL path를 검사하는가.
- \`HealthCheckIntervalSeconds\`: 몇 초 간격으로 검사하는가.
- \`HealthyThresholdCount\`: 몇 번 연속 성공해야 healthy가 되는가.
- \`UnhealthyThresholdCount\`: 몇 번 연속 실패해야 unhealthy가 되는가.
- \`Matcher.HttpCode\`: 어떤 HTTP 응답 코드를 성공으로 보는가.

실제 Target 상태:

\`\`\`bash
aws elbv2 describe-target-health --region $AWS_REGION \
  --target-group-arn $TG_ARN \
  --query 'TargetHealthDescriptions[].{Target:Target.Id,State:TargetHealth.State,Reason:TargetHealth.Reason,Description:TargetHealth.Description}' \
  --output table
\`\`\`

관찰 순서:

\`\`\`text
nginx 정상
→ State=healthy

nginx 중지 또는 잘못된 health path
→ 잠시 후 State=unhealthy
→ Reason/Description으로 원인 후보 확인

복구
→ threshold 충족 후 healthy
\`\`\`

Console의 색깔만 보는 대신 \`State / Reason / Description\`을 읽는 습관을 만든다.
