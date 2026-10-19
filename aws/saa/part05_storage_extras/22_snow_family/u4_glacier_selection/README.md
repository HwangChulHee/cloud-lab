# u4. Snowball → Glacier / SAA Selection

## Snowball에서 Glacier로 바로 갈 수 있나?

강의에서는 **Snowball이 Glacier로 직접 import할 수 없다고 설명**한다.

필요한 흐름:

```text
Snowball
   ↓ import
Amazon S3
   ↓ Lifecycle Policy
S3 Glacier / Glacier Deep Archive
```

즉 archive 목적이어도 먼저 S3에 import한 뒤 Lifecycle을 사용한다.

## 최종 선택 지도

```text
대량 offline migration
→ Snowball

network transfer가 1주 이상
→ Snowball 고려

edge location에서 local compute
→ Snowball Edge

대량 data를 network로 자동 sync
→ DataSync

on-prem application이 cloud storage를 계속 사용
→ Storage Gateway
```

## 면접용 설명

> Snowball Edge는 대규모 데이터를 physical device로 AWS에 옮기거나 제한된 네트워크 환경에서 edge compute를 수행하는 서비스입니다. Glacier로 직접 import하는 것이 아니라 S3에 먼저 적재한 뒤 Lifecycle Policy로 Glacier 계층으로 이동합니다.
