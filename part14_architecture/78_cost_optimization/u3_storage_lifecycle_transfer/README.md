# u3. Storage Lifecycle / Data Transfer

데이터는 접근 빈도와 복구 요구에 맞춰 storage class를 선택한다.

## Storage Lifecycle

```text
자주 접근
→ Standard 계열

접근 빈도 감소
→ IA 계열

장기 archive
→ Glacier 계열
```

S3 Lifecycle Policy, EFS Lifecycle 같은 기능으로 자동 tiering을 적용할 수 있다.

## Data Transfer

대량 데이터 이동에서는 network 시간과 비용도 고려한다.

```text
ongoing online transfer
→ DataSync / DX / VPN 등

network로 1주 이상 걸릴 수준의 offline migration
→ Snowball 고려
```

## 기억할 문장

> 저장 비용뿐 아니라 retrieval 비용, transfer 시간, access pattern을 함께 보고 storage tier와 migration 방식을 선택한다.
