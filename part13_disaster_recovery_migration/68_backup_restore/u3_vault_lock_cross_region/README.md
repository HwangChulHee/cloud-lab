# u3. Backup Vault Lock / Cross-Region / Cross-Account

## Cross-Region / Cross-Account

강의에서는 AWS Backup이 다음을 지원한다고 설명한다.

```text
Cross-Region Backup
Cross-Account Backup
```

DR 관점에서는 원본 Region/Account 문제와 backup을 분리하는 데 사용할 수 있다.

## Backup Vault Lock

Backup Vault Lock은 backup에 **WORM(Write Once Read Many)** 상태를 강제한다.

보호 대상:

```text
실수로 삭제
악의적 삭제
retention 기간 축소/변경
```

강의에서는 Vault Lock이 활성화되면 **root user도 backup을 삭제할 수 없다고 설명**한다.

## 기억할 문장

> Backup Vault Lock은 backup 자체가 지워지거나 retention이 줄어드는 것을 막는 마지막 보호 계층이다.
