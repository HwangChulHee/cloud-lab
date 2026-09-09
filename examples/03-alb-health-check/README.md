# Example 03 — ALB Health Check와 장애 격리 확인하기

Example 02에서 만든 ALB + EC2 두 대 구조를 그대로 사용한다.

```text
                ┌→ EC2-A
User → ALB → Target Group
                └→ EC2-B
```

이번에는 EC2 하나의 웹 서버를 일부러 중지하고 ALB가 어떻게 반응하는지 관찰한다.

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

각 항목을 읽고 예상한다.

예를 들어:

```text
Health check path: /
```

이라면 ALB는 각 Target의 `/`에 주기적으로 요청을 보내 정상 여부를 판단한다.

## 3. EC2-A의 nginx 중지

EC2-A에 접속해 nginx를 중지한다.

```bash
sudo systemctl stop nginx
```

바로 Target Group 화면을 새로고침한다.

처음에는 아직 `healthy`로 보일 수 있다.

왜 즉시 unhealthy가 되지 않는지 생각해본다.

```text
예상 이유:
→
```

## 4. 상태 변화 관찰

Target Group의 상태가 다음처럼 변하는지 관찰한다.

```text
healthy
  ↓
unhealthy
```

Health Check는 한 번 실패했다고 바로 서버를 제거하는 것이 아니라 설정된 임계값에 따라 상태를 판단한다.

## 5. ALB 요청 계속 보내기

EC2-A가 unhealthy가 된 뒤 ALB DNS로 여러 번 요청한다.

예상:

```text
EC2-B
EC2-B
EC2-B
...
```

ALB는 unhealthy Target으로 신규 요청을 보내지 않는다.

여기서 중요한 점:

```text
서버 장애
≠
서비스 전체 장애
```

로드밸런서 뒤에 정상 Target이 남아 있다면 서비스 진입점은 계속 응답할 수 있다.

## 6. EC2-A 복구

다시 nginx를 시작한다.

```bash
sudo systemctl start nginx
```

Target Group 상태를 관찰한다.

```text
unhealthy
   ↓
healthy
```

복구 직후 바로 healthy가 되지 않을 수 있다.

Healthy threshold를 만족해야 다시 정상 Target으로 판단된다.

## 7. 복구 후 요청 확인

ALB DNS로 여러 번 요청한다.

다시 EC2-A와 EC2-B의 응답이 모두 나타나는지 확인한다.

## 8. Health Check endpoint 분리 실험

애플리케이션에서는 보통 `/health` 같은 별도 endpoint를 둔다.

예:

```text
GET /health
200 OK
```

nginx에 간단한 health 파일을 만든다.

```bash
sudo mkdir -p /usr/share/nginx/html/health
sudo bash -c 'echo OK > /usr/share/nginx/html/health/index.html'
```

브라우저에서 다음이 200으로 응답되는지 확인한다.

```text
http://<EC2_IP>/health/
```

이후 Target Group Health Check path를 `/health/`로 변경해본다.

## 9. 잘못된 Health Check 실험

Health Check path를 존재하지 않는 경로로 잠시 바꾼다.

```text
/does-not-exist
```

예상:

```text
EC2는 정상 실행 중
nginx도 정상 실행 중
하지만 ALB 기준 Target은 unhealthy
```

이 실험이 중요한 이유는 **Health Check 설계 자체가 잘못되어도 정상 서버가 트래픽에서 제외될 수 있기 때문**이다.

확인 후 Health Check path를 정상 경로로 되돌린다.

## 10. 직접 설명하기

다음 질문에 답해본다.

```text
Q1. ALB는 서버 프로세스가 죽었다는 사실을 어떻게 알까?
→

Q2. Health Check가 없다면 어떤 문제가 생길까?
→

Q3. 왜 한 번 실패했다고 바로 unhealthy로 만들지 않을까?
→

Q4. Health Check endpoint가 너무 무거우면 어떤 문제가 생길까?
→
```

## 11. 완료 체크

- [ ] 두 Target이 healthy인 상태에서 시작했다.
- [ ] EC2-A의 nginx를 중지했다.
- [ ] Target이 unhealthy로 바뀌는 것을 관찰했다.
- [ ] unhealthy Target으로 요청이 가지 않는 것을 확인했다.
- [ ] nginx를 다시 시작했다.
- [ ] Target이 다시 healthy가 되는 것을 확인했다.
- [ ] Health Check path를 바꿔봤다.
- [ ] 잘못된 Health Check가 정상 서버를 제외할 수 있음을 확인했다.

## 12. 다음 단계

현재 구조에는 아직 문제가 있다.

EC2의 HTTP 80 포트가 인터넷 전체에 열려 있다면 사용자가 ALB를 거치지 않고 EC2에 직접 접근할 수 있다.

다음 예제에서는 Security Group Reference를 사용해서 다음 구조로 바꾼다.

```text
Internet
   ↓ :80
ALB Security Group
   ↓ :80, source = ALB SG
EC2 Security Group
```
