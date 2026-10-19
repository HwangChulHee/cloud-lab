# u2. All-AWS Multi-Region

강의는 on-premises + AWS뿐 아니라 **AWS Region A와 Region B를 모두 production 환경으로 운영**하는 구조도 보여준다.

```text
Region A
├─ ELB
├─ EC2 Auto Scaling (production)
└─ Aurora Global Primary
        ↕ data replication
Region B
├─ ELB
├─ EC2 Auto Scaling (production)
└─ Aurora Global Secondary
```

Route 53을 이용해 failover / traffic routing에 연결할 수 있다.

## DR Tips와 연결

강의는 다음 기술을 DR 요소로 함께 언급한다.

```text
Route 53
Cross-Region RDS Replication
Aurora Global Database
S3 Cross-Region Replication
RDS Multi-AZ
Site-to-Site VPN as DX recovery path
```

각 기술이 곧 Multi-Site 전략 자체라는 뜻은 아니고, DR architecture를 구성하는 building block으로 본다.
