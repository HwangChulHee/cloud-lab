# u3. Pilot Light vs Backup & Restore

## Backup & Restore

```text
평상시
→ backup만 유지

재해 시
→ restore + infrastructure 재구성
```

## Pilot Light

```text
평상시
→ critical core가 cloud에서 실행
→ data replication 유지

재해 시
→ compute/application layer 시작 및 확장
```

## SAA 판단

```text
Backup & Restore보다 빠른 복구 필요
하지만 full standby 비용은 부담
→ Pilot Light

critical database/core가 항상 준비되어 있어야 함
→ Pilot Light
```
