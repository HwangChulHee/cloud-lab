# u3. API Gateway Endpoint Types

강의에서는 세 가지 endpoint type을 구분한다.

## 1. Edge-Optimized

```text
Global Clients
   ↓
CloudFront Edge Locations
   ↓
API Gateway in one Region
```

강의에서는 default endpoint type으로 설명하며, global client latency 개선에 적합하다고 설명한다.

## 2. Regional

```text
Clients
   ↓
Regional API Gateway
```

같은 Region 또는 직접 CloudFront 전략을 제어하고 싶을 때 고려한다.

강의에서는 필요하면 Regional API 앞에 CloudFront를 직접 결합해 caching/distribution 제어를 더 세밀하게 할 수 있다고 설명한다.

## 3. Private

```text
VPC
 │
 │ Interface VPC Endpoint
 ▼
Private API Gateway
```

VPC 내부에서만 접근하는 API다.

강의 핵심:

```text
Interface VPC Endpoint (ENI)
Resource Policy
```

를 이용해 접근한다.

## SAA 판단

```text
global clients
→ Edge-Optimized

regional clients / own CloudFront control
→ Regional

VPC 내부 전용 API
→ Private
```
