# u3. Redshift Snapshots / DR / Multi-AZ

## 1. Snapshots

Redshift snapshot은 point-in-time cluster backup이다.

강의 핵심:

```text
S3 내부 저장
incremental
새 cluster로 restore
```

## 2. Automated Snapshot

강의에서는 다음 trigger를 설명한다.

```text
every 8 hours
or every 5 GB
or schedule
```

Retention:

```text
1 ~ 35 days
```

## 3. Manual Snapshot

직접 삭제할 때까지 유지할 수 있다.

## 4. Cross-Region Copy

Snapshot을 다른 Region으로 자동 copy할 수 있다.

```text
Region A
Redshift
 ↓ snapshot
Cross-Region Copy
 ↓
Region B Snapshot
 ↓ restore
New Redshift Cluster
```

## 5. Multi-AZ

강의는 일부 Redshift cluster에서 Multi-AZ mode를 지원한다고 설명한다.

## SAA 판단

```text
DR용 다른 Region backup
→ Cross-Region Snapshot Copy

장기 보관
→ Manual Snapshot

point-in-time cluster backup
→ Snapshot
```
