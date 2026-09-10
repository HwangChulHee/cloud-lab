# 08. Monitoring / Observability

## 핵심 질문

1. Metrics, Logs, Traces의 차이는 무엇인가요?
2. CPU 100% alert가 발생했습니다. 어떻게 대응하나요?
3. 어떤 metric을 기준으로 Auto Scaling을 구성할 수 있나요?
4. 단순 CPU metric만 보면 놓칠 수 있는 문제는 무엇인가요?
5. 애플리케이션 latency가 증가했을 때 어떤 지표를 같이 보겠습니까?
6. Alert threshold를 너무 민감하게 잡으면 어떤 문제가 생기나요?
7. SLI, SLO, SLA의 차이를 설명해보세요.
8. 로그를 중앙화해야 하는 이유는 무엇인가요?
9. Distributed tracing이 필요한 이유는 무엇인가요?
10. 운영 대시보드에 어떤 지표를 우선 배치하겠습니까?

## 사고 흐름

```text
Alert
 ↓
사용자 영향 확인
 ↓
최근 변경 확인
 ↓
Metrics로 범위 축소
 ↓
Logs로 원인 후보 확인
 ↓
필요하면 Trace로 요청 경로 추적
 ↓
복구 / 완화
 ↓
재발 방지
```

## CPU 100% 예시

```text
CPU metric 확인
 ↓
지속적인지 spike인지 구분
 ↓
traffic / request 증가 확인
 ↓
서버 내부 process 확인
 ↓
애플리케이션 문제인지 용량 부족인지 판단
 ↓
scale-out / scale-up / 코드 개선 / 제한 적용
```

면접에서는 "CloudWatch를 보겠습니다"에서 끝내지 말고 어떤 metric을 보고 그 결과에 따라 다음 확인 지점이 어떻게 달라지는지 설명하는 것이 중요합니다.
