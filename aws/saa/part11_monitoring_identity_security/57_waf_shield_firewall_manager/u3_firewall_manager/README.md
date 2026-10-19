# u3. AWS Firewall Manager

AWS Firewall Manager는 **AWS Organizations의 여러 Account에 공통 보안 규칙을 중앙 관리**하는 서비스다.

## Security Policy

강의에서는 다음 정책을 중앙 관리할 수 있다고 설명한다.

```text
AWS WAF rules
AWS Shield Advanced
Security Groups
AWS Network Firewall
Route 53 Resolver DNS Firewall
```

## 조직 단위 적용

```text
AWS Organization
   ↓
Firewall Manager Policy
   ↓
여러 Account / Resource
```

새 resource가 생성될 때도 policy가 자동 적용될 수 있어 compliance 유지에 도움이 된다.

## Region

강의에서는 Firewall Manager policy가 Region 단위로 생성된다고 설명한다.

## 기억할 문장

> Firewall Manager는 방화벽 자체가 아니라 여러 계정의 보안 정책을 중앙 배포/관리하는 control plane 성격의 서비스다.
