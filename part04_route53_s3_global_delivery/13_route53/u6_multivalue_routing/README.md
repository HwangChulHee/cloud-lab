# u6. Multi-Value Routing

Multi-Value Routing은 하나의 DNS 질의에 대해 **여러 개의 건강한 리소스 값을 반환**할 수 있는 정책이다.

예:

```text
api.example.com
→ 203.0.113.10
→ 203.0.113.11
→ 203.0.113.12
```

Route 53는 여러 레코드 중 Health Check를 통과한 값들을 반환할 수 있다.

강의 기준으로 한 번의 Multi-Value 응답에는 최대 8개의 healthy record가 반환될 수 있다.

---

## 왜 쓰는가

클라이언트가 여러 endpoint 중 하나를 선택하게 하면서, 비정상 endpoint는 DNS 응답에서 빼고 싶을 때 사용할 수 있다.

```text
Server A healthy   → 반환 가능
Server B unhealthy → 반환하지 않음
Server C healthy   → 반환 가능
```

---

## ELB와 차이

Multi-Value는 Load Balancer의 대체제가 아니다.

```text
Multi-Value
→ DNS가 여러 주소를 반환
→ 실제 연결 선택은 클라이언트/DNS 동작의 영향을 받음

ELB
→ 요청이 Load Balancer에 도착
→ Load Balancer가 healthy target으로 직접 분산
```

즉 둘 다 "여러 서버"와 관련 있어 보여도 동작 계층이 다르다.

### 예시

```text
DNS 기반으로 여러 공개 endpoint를 반환
→ Multi-Value

HTTP 요청을 여러 EC2에 안정적으로 분산
→ ALB
```

---

## SAA 포인트

```text
여러 healthy DNS record 반환
→ Multi-Value

최대 8개 healthy record 반환 가능
→ Multi-Value 특징

Load Balancer 자체가 필요한 상황
→ Multi-Value로 대체하지 않음
```
