# u6. EBS Encryption

## 지도 확인

EBS는 KMS를 이용해 암호화할 수 있다.

암호화는 Volume만 따로 보는 것이 아니라 Snapshot과 새 Volume까지 이어지는 흐름으로 이해한다.

---

## 개념

암호화된 EBS Volume을 사용하면 다음이 암호화된다.

- Volume 안의 data at rest
- EC2와 EBS 사이의 data in transit
- 해당 Volume에서 만든 Snapshot
- 해당 Snapshot에서 만든 새 Volume

암호화/복호화는 투명하게 처리되며 KMS key를 사용한다.

---

## 암호화되지 않은 EBS를 암호화하는 흐름

```text
Unencrypted EBS
→ Snapshot 생성
→ Snapshot Copy 시 Encryption 적용
→ 암호화된 Snapshot에서 새 EBS 생성
→ EC2에 연결
```

암호화된 Volume의 Snapshot은 계속 암호화된 상태를 유지한다.

---

## SAA 연결

```text
기존 unencrypted EBS를 encrypted EBS로 변경
→ Snapshot → encrypted copy → new encrypted Volume

EBS 암호화 키 관리
→ KMS

암호화된 Volume에서 만든 Snapshot
→ 암호화 상태 유지
```

이번 유닛은 암호화 전파 관계와 변환 절차를 기억하면 충분하다.
