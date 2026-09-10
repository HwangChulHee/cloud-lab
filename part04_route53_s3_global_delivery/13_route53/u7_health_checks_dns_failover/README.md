# u7. Health Checks와 DNS Failover

Route 53 Health Check는 DNS Routing Policy와 결합해 **비정상 리소스를 DNS 응답에서 제외하거나 Failover를 수행**하게 해준다.

## 1. Endpoint Health Check

공개 endpoint를 직접 모니터링한다.

예:

```text
Route 53 Health Checker
  ↓ HTTP/HTTPS/TCP
Public ALB / EC2 / Endpoint
```

HTTP Health Check는 공개 리소스를 대상으로 사용한다.

### 예시

```text
https://shop.example.com/health
→ 정상 응답
→ healthy
```

반대로 정해진 조건을 만족하지 못하면 unhealthy로 판단할 수 있다.

---

## 2. Calculated Health Check

여러 Child Health Check 결과를 하나의 Parent Health Check로 합친다.

```text
Health Check A ─┐
Health Check B ─┼→ Calculated Health Check
Health Check C ─┘
```

AND, OR, NOT 같은 논리를 사용할 수 있다.

예:

```text
A와 B가 모두 정상이어야 서비스 정상
→ AND
```

또는 여러 하위 체크 중 일정 수 이상이 통과해야 정상으로 판단하는 식으로 구성할 수 있다.

강의에서는 최대 256개의 Child Health Check를 모니터링할 수 있다고 설명한다.

---

## 3. CloudWatch Alarm 기반 Health Check

Route 53 Health Check가 직접 접근하기 어려운 private resource의 상태도 CloudWatch Alarm을 이용해 간접적으로 판단할 수 있다.

예:

```text
Private RDS
 ↓ metric
CloudWatch Alarm
 ↓
Route 53 Health Check
```

즉 "Route 53이 private RDS에 직접 HTTP 요청"을 보내는 것이 아니라, CloudWatch Alarm 상태를 활용하는 식이다.

---

## 4. Automated DNS Failover

Health Check와 Failover Routing을 연결하면:

```text
Primary healthy
→ Primary DNS 응답

Primary unhealthy
→ Secondary DNS 응답
```

구성이 가능하다.

예:

```text
서울 ALB   = Primary
도쿄 ALB   = Secondary
Health Check = 서울 ALB 확인
```

서울 서비스 장애 시 Route 53이 도쿄 쪽 레코드를 반환하게 만들 수 있다.

---

## 5. DNS Failover의 특성

DNS 기반이므로 "장애가 감지되는 순간 모든 사용자가 즉시 Secondary로 이동"한다고 단순하게 생각하면 안 된다.

이미 Resolver나 클라이언트에 캐시된 DNS 응답은 TTL의 영향을 받을 수 있다.

그래서:

```text
Health Check
+ Routing Policy
+ TTL
```

을 같이 생각해야 한다.

---

## SAA 포인트

```text
공개 endpoint 직접 상태 확인
→ Endpoint Health Check

여러 Health Check를 논리적으로 결합
→ Calculated Health Check

private resource/custom metric 기반 판단
→ CloudWatch Alarm 기반 Health Check

Primary 장애 시 Secondary DNS 응답
→ Failover Routing + Health Check
```
