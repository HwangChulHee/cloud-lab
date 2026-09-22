# 72. AWS DMS / SCT

이 단원은 **database migration에서 data 이동과 schema 변환을 분리해서 이해**한다.

## Units

- [ ] [u1. AWS Database Migration Service](./u1_dms/README.md)
- [ ] [u2. DMS Full Load / CDC / Multi-AZ](./u2_full_load_cdc_multiaz/README.md)
- [ ] [u3. AWS Schema Conversion Tool](./u3_sct/README.md)
- [ ] [u4. DMS + SCT 선택 기준](./u4_selection/README.md)

## 핵심 구분

```text
DMS
→ database data를 이동 / 복제
→ source DB를 migration 중에도 계속 사용 가능
→ homogeneous / heterogeneous migration
→ CDC continuous replication

SCT
→ database schema를 다른 engine용으로 변환
→ heterogeneous migration에 사용
→ 같은 DB engine이면 보통 필요 없음
```

## 대표 구조

```text
Source DB
   ↓ schema conversion
  SCT
   ↓
Target Schema

Source DB
   ↓ Full Load + CDC
  DMS
   ↓
Target DB
```
