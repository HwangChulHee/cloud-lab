# u4. Backup & Restore SAA Selection

```text
가장 낮은 비용의 DR
→ Backup & Restore

복구 시간이 길어도 괜찮음
→ Backup & Restore

여러 AWS 서비스 backup 중앙 관리
→ AWS Backup

다른 Region에 backup 보관
→ Cross-Region Backup

다른 Account에 backup 분리
→ Cross-Account Backup

backup 삭제 방지 / WORM
→ Backup Vault Lock
```

## 다른 DR 전략과 비교

```text
Backup & Restore
→ standby application 없음

Pilot Light
→ critical core는 이미 실행

Warm Standby
→ 전체 application 최소 크기로 실행

Multi-Site
→ production scale 실행
```
