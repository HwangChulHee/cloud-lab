# 17. ACM & HTTPS

이 단원은 AWS Certificate Manager(ACM)와 HTTPS/TLS 인증서 운영을 SAA 관점에서 정리한다.

핵심은 인증서 자체의 암호학보다 **어디서 인증서를 발급/관리하고, 어떤 AWS 서비스에 붙이며, Region 제약이 어떻게 되는지**를 이해하는 것이다.

## Units

- [ ] u1. TLS Certificate & ACM Basics
- [ ] u2. Public Certificate Validation & Renewal
- [ ] u3. ALB, CloudFront & API Gateway Integration
- [ ] u4. Imported Certificates & Expiration Monitoring

## SAA 선택 지도

```text
HTTPS 인증서 발급/관리
→ ACM

DNS 자동화 친화적 인증서 검증
→ DNS Validation

ALB에서 HTTPS 종료
→ ACM Certificate + HTTPS Listener

CloudFront용 ACM 인증서
→ us-east-1

Regional API Gateway 인증서
→ API Gateway와 같은 Region

외부에서 만든 인증서 사용
→ ACM Import

Imported Certificate 갱신
→ 자동 갱신 안 됨, 직접 재수입 필요
```
