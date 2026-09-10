# u7. MFA Delete, Object Lock & Glacier Vault Lock

이 유닛은 **실수나 악의적인 삭제를 막고 일정 기간 데이터를 반드시 보존**해야 하는 상황을 다룬다.

## 1. MFA Delete

MFA Delete는 Versioning이 활성화된 Bucket에서 중요한 삭제 작업에 MFA 인증을 추가하는 기능이다.

즉 비밀번호/권한만 탈취된 상황에서도 삭제 작업에 추가 인증을 요구할 수 있다.

## 2. WORM

Object Lock과 Glacier Vault Lock에서 반복해서 나오는 용어가 WORM이다.

```text
Write Once Read Many
```

한 번 기록한 데이터는 정해진 기간 동안 변경/삭제하지 못하고 읽기만 가능하게 하는 보존 모델이다.

예:

```text
회계 감사 자료
의료 기록
규제 대상 거래 로그
```

## 3. S3 Object Lock

Object Lock은 Versioning이 필요한 기능이며 특정 Object Version을 일정 기간 삭제/덮어쓰기하지 못하게 보호한다.

### Compliance Mode

가장 강한 모드다.

```text
일반 사용자 삭제 불가
관리자 삭제 불가
Root 사용자도 삭제 불가
보존 기간 단축 불가
```

규정 준수가 최우선일 때 사용한다.

### Governance Mode

기본적으로 삭제/변경을 막지만 특별한 권한을 가진 사용자는 보호를 우회할 수 있다.

```text
일반 사용자 → 변경/삭제 불가
특별 권한 관리자 → 필요 시 우회 가능
```

즉 Compliance보다 운영 유연성이 있다.

## 4. Retention Period와 Legal Hold

`Retention Period`는 정해진 기간 동안 보호한다.

```text
7년간 삭제 금지
```

`Legal Hold`는 날짜를 미리 정하기보다 해제할 때까지 무기한 보호하는 개념이다.

```text
소송 진행 중
→ Legal Hold ON
→ 사건 종료 후 권한 있는 사용자가 해제
```

## 5. Glacier Vault Lock

Glacier Vault Lock도 WORM 모델을 위한 기능이다.

Vault Lock Policy를 만들고 Lock하면 이후 정책을 변경하거나 삭제할 수 없도록 고정할 수 있다.

핵심 목적은 장기 아카이브 데이터의 **규정 준수와 변경 불가능한 보존 정책**이다.

## SAA 판단

```text
중요한 Version 삭제에 MFA 요구
→ MFA Delete

S3 Object Version을 일정 기간 삭제 불가능하게 보존
→ Object Lock

Root도 삭제 못 해야 함
→ Object Lock Compliance Mode

특별 권한 관리자는 우회 가능해야 함
→ Governance Mode

기간 없이 사건 종료까지 보존
→ Legal Hold

Glacier 보존 정책 자체를 잠가 변경 불가능하게 함
→ Glacier Vault Lock
```
