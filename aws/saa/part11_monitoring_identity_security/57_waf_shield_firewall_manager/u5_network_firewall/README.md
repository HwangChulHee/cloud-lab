# u5. AWS Network Firewall

AWS Network Firewall은 **VPC 전체 네트워크 트래픽을 Layer 3부터 Layer 7까지 검사**하는 managed firewall이다.

## 검사 가능한 경로

강의에서 다음을 언급한다.

```text
VPC ↔ VPC
Outbound → Internet
Inbound ← Internet
Direct Connect 트래픽
Site-to-Site VPN 트래픽
```

## Rule

```text
IP / Port
Protocol
Stateful domain list
Regex pattern
Allow / Drop / Alert
```

Active flow inspection과 intrusion-prevention 기능을 제공한다.

## Logging

Rule match log를 다음으로 보낼 수 있다.

```text
S3
CloudWatch Logs
Kinesis Data Firehose
```

## Firewall Manager 연동

Network Firewall rule도 Firewall Manager로 여러 Account/VPC에 중앙 적용할 수 있다.

## 기억할 문장

> WAF가 HTTP 요청용이라면 Network Firewall은 VPC 전체 네트워크 흐름을 더 넓은 계층에서 검사한다.
