# u2. AWS Shield / Shield Advanced

AWS Shield는 DDoS 공격 방어 서비스다.

## Shield Standard

강의 핵심:

```text
모든 AWS 고객에게 기본 활성화
무료
Layer 3 / Layer 4 공격 방어
SYN / UDP Flood
Reflection attack
```

## Shield Advanced

더 강한 DDoS 보호를 제공하는 유료 서비스다.

강의에서는 다음 보호 대상을 언급한다.

```text
EC2
ELB
CloudFront
Global Accelerator
Route 53
```

추가 기능:

```text
전문 DDoS 대응 지원
advanced reporting
DDoS usage spike 비용 보호
automatic application-layer DDoS mitigation
→ WAF rule 자동 생성/평가/배포
```

## 기억할 문장

> 일반 DDoS 기본 방어는 Shield Standard, 반복적/고위험 DDoS와 전문 대응이 필요하면 Shield Advanced다.
