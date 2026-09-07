# u2. EBS Snapshots

## 지도 확인

Snapshot은 EBS Volume의 특정 시점 백업이다.

```text
EBS Volume
   ↓ snapshot
EBS Snapshot
   ↓ restore
New EBS Volume
```

---

## 개념

EBS Snapshot은 Volume의 point-in-time backup이다.

Volume을 반드시 detach해야 Snapshot을 만들 수 있는 것은 아니지만, 데이터 일관성 측면에서는 I/O를 정리한 상태에서 생성하는 편이 좋다.

Snapshot을 이용하면:

- 같은 AZ에서 새 Volume 생성
- 다른 AZ에서 새 Volume 생성
- 다른 Region으로 Snapshot 복사

같은 작업이 가능하다.

즉 EBS 자체는 AZ에 묶여 있지만 Snapshot이 이동의 연결고리가 된다.

---

## Snapshot 기능

### Snapshot Archive

오랫동안 보관할 Snapshot을 더 저렴한 Archive tier로 이동할 수 있다.
대신 복원에 시간이 오래 걸린다.

### Recycle Bin

삭제한 Snapshot을 일정 기간 보존해 실수로 삭제한 경우 복구할 수 있다.

### Fast Snapshot Restore

Snapshot에서 만든 Volume을 처음 사용할 때 발생할 수 있는 초기 성능 지연을 줄이기 위해 미리 초기화하는 기능이다.
비용이 추가된다.

---

## SAA 연결

```text
EBS를 다른 AZ로 이동
→ Snapshot → 대상 AZ에 Restore

실수로 삭제한 Snapshot 복구
→ Recycle Bin

장기 보관 비용 절감
→ Snapshot Archive

Snapshot 복원 직후부터 높은 성능 필요
→ Fast Snapshot Restore
```

이번 유닛은 기능별 선택 기준 중심으로 본다.
