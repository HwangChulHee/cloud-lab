# u3. EFS Storage Classes / Lifecycle

EFS는 접근 빈도에 따라 storage tier를 사용할 수 있다.

## Storage Tiers

```text
EFS Standard
→ frequently accessed files

EFS Infrequent Access
→ 저장 비용 낮음
→ retrieval cost 있음

EFS Archive
→ 매우 드물게 접근
→ 강의에서는 연 몇 회 수준의 data 예시
```

## Lifecycle Policy

일정 기간 접근하지 않은 파일을 더 저렴한 tier로 이동할 수 있다.

```text
EFS Standard
   ↓ no access for N days
EFS IA / Archive
```

## Availability Class

강의에서는 다음도 구분한다.

```text
EFS Standard
→ Multi-AZ
→ production에 적합

EFS One Zone
→ Single AZ
→ dev 등 비용 절감
→ backup enabled by default
→ One Zone-IA와 조합 가능
```

## 기억할 문장

> EFS Lifecycle은 접근 빈도가 낮아진 파일을 IA/Archive로 이동해 비용을 줄이는 기능이다.
