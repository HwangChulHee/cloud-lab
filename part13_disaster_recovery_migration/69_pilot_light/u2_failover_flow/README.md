# u2. Pilot Light Failover Flow

재해 시 흐름을 개념적으로 보면 다음과 같다.

```text
1. Primary 장애
2. AWS의 replicated critical data 확인
3. 중지된 compute/application resource 시작
4. 필요한 production capacity 확보
5. Route 53 등으로 traffic 전환
6. 서비스 복구
```

## 중요한 포인트

Pilot Light는 "AWS에 아무것도 없는 상태"가 아니다.

```text
항상 살아 있음
→ critical core / replicated database

재해 때 준비
→ compute / application tier / traffic cutover
```

따라서 Backup & Restore보다 RTO를 줄일 수 있다.
