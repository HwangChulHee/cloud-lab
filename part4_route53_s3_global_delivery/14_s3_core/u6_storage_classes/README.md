# u6. S3 Storage Classes

S3 Storage Class는 **데이터를 얼마나 자주 접근하는지, 얼마나 빨리 복구해야 하는지, 어느 정도 비용을 감수할지**에 따라 선택하는 저장 등급이다.

단순히 "싼 것"을 고르는 문제가 아니라 접근 패턴과 복구 요구사항을 함께 본다.

## 1. S3 Standard

자주 접근하는 일반적인 데이터에 사용한다.

```text
자주 읽음
빠른 접근 필요
높은 가용성 필요
```

예:

```text
상품 이미지
웹 콘텐츠
애플리케이션 데이터 파일
```

---

## 2. S3 Standard-IA

IA는 `Infrequent Access`, 즉 **자주 접근하지는 않지만 필요할 때는 즉시 꺼내야 하는 데이터**라는 뜻이다.

Standard보다 저장 비용은 낮지만, 데이터를 꺼낼 때 Retrieval 비용이 발생할 수 있다.

예:

```text
백업
재해복구용 파일
가끔만 조회하는 오래된 문서
```

여러 AZ에 데이터를 보관한다.

---

## 3. S3 One Zone-IA

Standard-IA와 비슷하지만 데이터를 **하나의 AZ에만 저장**한다.

그래서 더 저렴하지만 해당 AZ 자체가 파괴되는 극단적 상황에서는 데이터를 잃을 수 있다.

따라서:

```text
잃어도 다시 만들 수 있는 데이터
다른 곳에 원본이 있는 secondary copy
```

같은 경우가 적합하다.

### 예시

온프레미스에 원본 백업이 있고 AWS에는 추가 복사본만 두는 경우:

```text
원본: On-Premise
보조 복사본: S3 One Zone-IA
```

---

## 4. S3 Intelligent-Tiering

접근 패턴을 예측하기 어려울 때 사용한다.

S3가 Object의 접근 빈도를 관찰하고 적절한 Access Tier로 자동 이동한다.

```text
Frequent Access
↓ 일정 기간 미사용
Infrequent Access
↓ 더 오래 미사용
Archive 계열 Tier
```

작은 모니터링/자동 계층화 비용이 있지만, 사람이 직접 "이 파일은 30일 뒤 IA로 보내자"를 일일이 관리하지 않아도 된다.

### 적합한 상황

```text
어떤 Object가 자주 읽힐지 모름
접근 패턴이 계속 변함
```

---

## 5. Glacier 계열

장기 보관과 Archive 목적이다.

### Glacier Instant Retrieval

오래 보관하지만 필요할 때는 millisecond 수준으로 빠르게 가져와야 하는 데이터.

```text
접근 빈도 매우 낮음
하지만 꺼낼 때는 즉시 필요
```

### Glacier Flexible Retrieval

복구까지 몇 분~몇 시간이 걸려도 되는 Archive 데이터.

### Glacier Deep Archive

가장 장기적인 보관 목적의 저비용 계층이다.

```text
수년간 거의 읽지 않음
복구에 수 시간 이상 걸려도 됨
```

예:

```text
법적 장기 보존 자료
오래된 감사 로그
장기 백업
```

---

## 6. 최소 보관 기간과 Retrieval Cost

저렴한 Storage Class일수록 다음 조건이 붙을 수 있다.

```text
Minimum Storage Duration
Retrieval Fee
```

예를 들어 3일만 저장했다가 바로 삭제할 데이터를 장기 Archive Class에 넣으면, 저장 단가만 보고 기대한 만큼 저렴하지 않을 수 있다.

그래서 문제에서는:

```text
얼마나 오래 보관?
얼마나 자주 조회?
조회 시 얼마나 빨리 필요?
AZ 장애까지 견뎌야 하나?
```

를 같이 본다.

---

## 선택 예시

```text
상품 이미지
→ Standard

6개월에 한 번 볼 수도 있는 백업, 즉시 조회 필요
→ Standard-IA

재생성 가능한 보조 백업
→ One Zone-IA

접근 패턴을 전혀 예측 못함
→ Intelligent-Tiering

분기에 한 번 조회하지만 즉시 필요
→ Glacier Instant Retrieval

오래 보관하고 몇 시간 뒤 복구해도 됨
→ Glacier Flexible Retrieval

7년 보관, 거의 조회 안 함
→ Glacier Deep Archive
```

## SAA 포인트

Storage Class 문제는 서비스 이름보다 **Access Frequency + Retrieval Time + Resiliency + Cost**를 읽고 선택한다.
