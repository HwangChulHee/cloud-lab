# u4. EC2 Instance Store

## 지도 확인

EBS가 네트워크 스토리지라면 Instance Store는 EC2 호스트에 직접 연결된 로컬 스토리지다.

```text
EC2 Host
 ├─ EC2 Instance
 └─ Local Instance Store
```

---

## 개념

Instance Store는 매우 높은 I/O 성능과 낮은 지연시간이 장점이다.

하지만 데이터가 EC2 인스턴스의 생명주기에 강하게 묶여 있다.

특히 인스턴스를 stop/terminate하거나 호스트에 문제가 생기면 데이터를 잃을 수 있으므로 **영구 저장소로 사용하면 안 된다.**

적합한 용도:

- cache
- buffer
- scratch data
- 임시 처리 데이터
- 복제본이 다른 곳에 존재하는 데이터

백업과 복제는 사용자가 직접 설계해야 한다.

---

## EBS와 비교

```text
영속성 / 인스턴스와 분리
→ EBS

매우 높은 로컬 I/O / 데이터 유실 허용
→ Instance Store
```

Instance Store의 핵심은 '빠르다'보다 **ephemeral storage**라는 점을 같이 기억하는 것이다.

---

## SAA 연결

```text
최고 수준의 로컬 디스크 성능이 필요하고 데이터가 임시 데이터
→ Instance Store

EC2가 사라져도 데이터를 유지해야 함
→ EBS 등 영속 스토리지
```

이번 유닛은 비교 기준만 명확히 잡고 넘어간다.
