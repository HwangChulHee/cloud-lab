# u4. Simple / Weighted / Latency Routing

Route 53의 Routing Policy는 **DNS 질의에 어떤 레코드를 반환할지 결정하는 규칙**이다. HTTP 요청을 직접 프록시하는 것이 아니라 DNS 응답을 조절한다.

## 1. Simple Routing

가장 기본적인 방식이다.

```text
example.com
→ 203.0.113.10
```

특별한 분산 전략 없이 하나 또는 여러 값을 반환할 수 있다. Health Check와 결합하는 용도의 정책은 아니다.

### 예시

서비스 서버가 하나뿐이면:

```text
shop.example.com
→ ALB
```

처럼 단순하게 연결하면 된다.

---

## 2. Weighted Routing

`Weighted`는 가중치라는 뜻이다. 여러 리소스에 **원하는 비율로 DNS 응답을 나누고 싶을 때** 사용한다.

예:

```text
Server A weight 80
Server B weight 20
```

대략적으로 DNS 응답의 80%는 A, 20%는 B를 선택하도록 유도한다.

가중치의 절대값보다 서로 간의 비율이 중요하다.

```text
80 : 20
과
8 : 2
```

은 같은 비율이다.

### 사용 사례

```text
새 버전 10% 배포
기존 버전 90% 유지

Region A 70%
Region B 30%
```

Blue/Green, Canary와 비슷한 트래픽 전환 상황을 DNS 수준에서 만들 수 있다.

Health Check와 연결하면 unhealthy 레코드를 응답에서 제외하는 구성도 가능하다.

---

## 3. Latency-based Routing

여기서 `Latency`는 요청이 오가는 데 걸리는 지연시간이다.

Latency Routing은 사용자를 **AWS가 측정한 네트워크 지연이 가장 낮은 Region의 리소스**로 보내는 데 사용한다.

예:

```text
한국 사용자
  ↓
서울 Region이 더 낮은 latency
  ↓
서울 리소스

프랑스 사용자
  ↓
아일랜드 Region이 더 낮은 latency
  ↓
아일랜드 리소스
```

중요한 점은 단순한 지리적 거리만 보는 것이 아니라 AWS가 가진 latency 정보를 기준으로 판단한다는 것이다.

### Geolocation과 헷갈리지 않기

```text
가장 낮은 네트워크 latency
→ Latency Routing

사용자의 국가/대륙이라는 위치 자체가 기준
→ Geolocation Routing
```

---

## SAA 선택 기준

```text
특별한 정책 없이 하나의 리소스
→ Simple

트래픽을 90:10, 70:30처럼 비율 분배
→ Weighted

사용자에게 가장 빠른 AWS Region
→ Latency-based
```
