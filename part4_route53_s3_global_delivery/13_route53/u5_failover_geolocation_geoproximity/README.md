# u5. Failover / Geolocation / Geoproximity Routing

## 1. Failover Routing

Failover Routing은 **Primary가 정상일 때는 Primary를 사용하고, 장애가 나면 Secondary로 전환**하는 Active-Passive 패턴이다.

```text
User
 ↓
Route 53
 ├─ Primary   → 정상일 때 사용
 └─ Secondary → Primary 장애 시 사용
```

여기서 핵심은 Primary 레코드에 Health Check를 연결해 상태를 판단하는 것이다.

### 예시

```text
Primary: 서울 Region
Secondary: 도쿄 Region
```

서울 서비스가 정상일 때:

```text
shop.example.com
→ 서울
```

서울 서비스가 장애 상태가 되면:

```text
shop.example.com
→ 도쿄
```

DNS 기반 Failover이므로 이미 캐시된 DNS 응답은 TTL 동안 남아 있을 수 있다는 점도 기억한다.

---

## 2. Geolocation Routing

Geolocation은 **사용자의 위치**를 기준으로 DNS 응답을 다르게 한다.

예:

```text
한국 사용자 → Seoul endpoint
미국 사용자 → Virginia endpoint
그 외 사용자 → Default endpoint
```

대표 기준은 대륙, 국가, 미국의 주 등이다.

### 사용 사례

```text
지역별 콘텐츠
법적/규제 요구사항
지역별 언어 사이트
```

Default Record는 어떤 명시적인 위치 규칙에도 매칭되지 않은 사용자를 처리할 때 중요하다.

### Latency Routing과 차이

```text
가장 빠른 Region
→ Latency

사용자가 어느 나라/지역에 있는가
→ Geolocation
```

가까운 Region이라고 항상 가장 낮은 latency를 보장하는 것은 아니므로 둘의 기준은 다르다.

---

## 3. Geoproximity Routing

Geoproximity는 **사용자와 리소스의 지리적 위치**를 기준으로 트래픽을 라우팅하고, `Bias` 값을 통해 특정 리소스로 가는 트래픽 영역을 넓히거나 줄일 수 있다.

`Bias`는 편향값이라고 생각하면 된다.

```text
Positive Bias
→ 해당 리소스가 담당하는 지리적 영역을 넓힘

Negative Bias
→ 담당 영역을 줄임
```

### 예시

서울과 도쿄에 리소스가 있는데 서울 쪽으로 더 많은 사용자를 보내고 싶다고 하자.

```text
Seoul Resource: +50 bias
Tokyo Resource: 0
```

그러면 원래는 도쿄로 갈 수도 있었던 일부 지역까지 서울 리소스 쪽으로 끌어올 수 있다.

Geoproximity는 단순히 "한국이면 서울"처럼 규칙을 고정하는 Geolocation과 다르다.

---

## SAA 선택 기준

```text
Primary 장애 시 Secondary로 전환
→ Failover

사용자의 국가/대륙 기준
→ Geolocation

리소스와 사용자의 위치 + bias로 트래픽 영역 조절
→ Geoproximity
```
