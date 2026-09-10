# u4. S3 Versioning

Versioning은 같은 Key의 Object가 덮어써지거나 삭제될 때 **이전 버전을 보존**하는 기능이다.

## 1. Versioning이 없으면

```text
report.csv 업로드
↓
새 report.csv 업로드
↓
기존 내용이 덮어써짐
```

실수로 잘못된 파일을 올리면 이전 상태로 돌아가기 어렵다.

---

## 2. Versioning을 켜면

같은 Key라도 버전이 여러 개 남는다.

```text
report.csv
├── Version A
├── Version B
└── Version C
```

사용자는 최신 버전을 기본적으로 보지만, 필요하면 이전 버전을 다시 가져올 수 있다.

### 예시

상품 이미지가 잘못 덮어써졌다고 하자.

```text
products/1001/main.jpg
```

Versioning이 켜져 있으면 이전 버전의 이미지를 복구할 수 있다.

---

## 3. 삭제도 버전으로 처리된다

Versioning이 활성화된 Bucket에서 Object를 일반 삭제하면 즉시 모든 데이터가 영구 삭제되는 것이 아니라 `Delete Marker`가 최신 버전으로 추가될 수 있다.

```text
main.jpg
├── v1
├── v2
└── Delete Marker ← 최신
```

그래서 기본 조회에서는 삭제된 것처럼 보이지만, 이전 버전은 남아 있을 수 있다.

Delete Marker를 제거하면 이전 Object가 다시 보이게 만들 수 있다.

---

## 4. Versioning 상태

Versioning은 한 번 활성화한 뒤 완전히 "없었던 상태"로 되돌리는 것이 아니라 Suspend할 수 있다.

```text
Disabled
→ 아직 활성화한 적 없음

Enabled
→ 버전 보존

Suspended
→ 새 Object에 대한 버전 관리 중지
```

기존에 만들어진 버전들은 그대로 남는다.

---

## 5. 비용과의 관계

버전을 여러 개 보관하면 그만큼 저장 공간을 사용한다.

```text
100MB 파일을 5번 수정
→ 이전 버전까지 보존
→ 저장 비용도 증가
```

그래서 오래된 버전을 Lifecycle Rule로 정리하는 패턴이 자주 사용된다.

---

## SAA 포인트

```text
실수로 덮어쓴 Object 복구
→ Versioning

실수로 삭제한 Object 복구
→ Versioning + 이전 버전/Delete Marker 확인

이전 버전이 계속 쌓여 비용 증가
→ Lifecycle로 old version 정리

Replication 사용
→ source와 destination 모두 Versioning 필요
```
