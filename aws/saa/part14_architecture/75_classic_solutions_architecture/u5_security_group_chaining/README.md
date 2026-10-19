# u5. Security Group Chaining

강의의 3-tier architecture는 Security Group을 **CIDR보다 상위 계층 SG reference**로 연결하는 패턴을 보여준다.

```text
Internet
   ↓ 80/443
ALB-SG
   ↓ only from ALB-SG
EC2-SG
   ├→ DB port only to RDS-SG
   └→ Cache port only to Cache-SG
```

## 원칙

```text
ALB
→ Internet HTTP/HTTPS 허용

EC2
→ ALB SG에서 오는 traffic만 허용

RDS
→ EC2 SG에서 오는 DB traffic만 허용

ElastiCache
→ EC2 SG에서 오는 cache traffic만 허용
```

## 기억할 문장

> 3-tier 보안은 각 계층의 Security Group을 다음 계층에 reference해 필요한 path만 열어두는 방식으로 설계한다.
