# u4. Architecture Review Thinking

Architecture 문제를 볼 때 다음처럼 요구사항을 분해한다.

```text
Security
→ 누가 접근하는가? encryption은?

Reliability
→ instance/AZ/Region failure에 어떻게 대응하는가?

Performance
→ latency / throughput / scaling 요구는?

Cost
→ baseline과 burst workload는?

Operations
→ 관측/배포/복구를 자동화할 수 있는가?

Sustainability
→ 과도한 resource를 계속 유지하고 있지 않은가?
```

## 중요한 점

강의는 6 Pillar를 서로 하나씩 희생해서 맞추는 체크리스트로 설명하지 않는다.

예를 들어 Auto Scaling은:

```text
Performance Efficiency
+ Cost Optimization
+ Reliability
```

여러 관점에 동시에 기여할 수 있다.
