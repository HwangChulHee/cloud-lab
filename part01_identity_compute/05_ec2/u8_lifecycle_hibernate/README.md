# u8. EC2 Lifecycle와 Hibernate

## 지도 확인

EC2는 단순히 켜고 끄는 것 외에도 stop, terminate, hibernate의 차이를 이해해야 한다.

강의에서는 특히 어떤 상태가 디스크와 메모리를 보존하는지 비교한다.

---

## 1. Stop

인스턴스를 중지한다.

```text
EC2 compute
→ 중지

EBS data
→ 유지 가능
```

다시 start하면 OS가 부팅되고 애플리케이션 초기화가 다시 필요할 수 있다.

자동 할당 Public IP는 stop/start 이후 바뀔 수 있다.

---

## 2. Terminate

인스턴스를 제거한다.

root EBS가 Delete on Termination으로 설정되어 있다면 해당 데이터도 함께 삭제될 수 있다.

즉 stop과 terminate는 같은 "꺼짐" 상태가 아니다.

```text
Stop
→ 나중에 다시 시작

Terminate
→ 인스턴스 제거
```

---

## 3. Hibernate

Hibernate는 RAM 상태를 root EBS volume에 기록해 메모리 상태를 보존한다.

```text
Running
  ↓ hibernate
RAM state
  ↓
Encrypted root EBS
```

다시 시작하면 일반 stop/start보다 초기화 시간을 줄일 수 있다.

강의에서는 root EBS volume이 암호화되어야 한다는 조건을 강조한다.

사용 사례:

```text
오래 걸리는 초기화
RAM 상태 보존
Long-running processing
```

---

## 4. User Data와 재시작

강의 기준으로 EC2 User Data는 인스턴스의 첫 시작 시 실행된다.

따라서 단순 stop/start를 할 때마다 bootstrap script가 반복 실행된다고 생각하면 안 된다.

```text
First launch
→ OS boot + User Data

Later start
→ OS boot
```

---

## SAA 연결

```text
디스크는 보존하고 compute만 멈춤
→ Stop

인스턴스 제거
→ Terminate

RAM 상태까지 유지해 빠른 재개
→ Hibernate
```

이번 유닛은 상태 차이를 명확히 구분하면 되므로 유제와 3문장 요약은 생략한다.
