# u2. Warm Standby Failover / Scale-Up

재해가 발생하면 핵심 작업은 **새 환경을 만드는 것보다 이미 실행 중인 환경을 production size로 확장하는 것**이다.

```text
1. Primary failure 감지
2. DR database/replication 상태 확인
3. EC2 Auto Scaling desired capacity 증가
4. production traffic을 감당할 capacity 확보
5. Route 53 등으로 traffic failover
```

## 핵심

```text
Pilot Light
→ application compute를 시작해야 할 수 있음

Warm Standby
→ application은 이미 실행 중
→ 주로 scale-up + traffic switch
```

따라서 더 짧은 RTO를 목표로 한다.
