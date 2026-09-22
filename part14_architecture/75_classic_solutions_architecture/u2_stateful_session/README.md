# u2. Stateful Web App / Session

웹 애플리케이션이 session을 EC2 local memory에 저장하면 사용자가 다른 instance로 이동할 때 문제가 생길 수 있다.

강의에서는 여러 해결책을 보여준다.

## 1. Sticky Session

ELB sticky session으로 같은 사용자를 같은 instance에 보내는 방법이다.

하지만 instance 자체에 state가 남아 scale/failure 관점의 결합도가 생긴다.

## 2. Client Cookie

일부 상태를 browser cookie에 넣어 web tier를 stateless하게 만들 수 있다.

강의 주의사항:

```text
HTTP request가 무거워질 수 있음
cookie 변조 위험
validation 필요
cookie 크기 제한
```

## 3. External Session Store

강의의 핵심 패턴:

```text
Client
 ↓ session_id
EC2 Auto Scaling
 ↓
ElastiCache
```

DynamoDB도 session store 대안으로 언급된다.

## 기억할 문장

> Scale 가능한 web tier에서는 session을 특정 EC2에서 분리해 ElastiCache/DynamoDB 같은 외부 store로 옮기는 패턴이 중요하다.
