# 12부 — VPC & Networking

이 파트는 `examples/05` 이후 거의 모든 AWS 실습의 네트워크 기반이다.

강의 순서에서는 뒤쪽에 나오지만, Guided Examples를 시작하기 전에는 이 파트를 먼저 끝내는 것을 권장한다.

## 학습 순서

- [59. VPC](./59_vpc/README.md)
- [60. Subnet과 Route Table](./60_subnet_route_table/README.md)
- [61. Internet Gateway와 NAT Gateway](./61_igw_nat_gateway/README.md)
- [62. Security Group과 NACL](./62_security_group_nacl/README.md)
- [63. VPC Peering / Transit Gateway](./63_vpc_peering_transit_gateway/README.md)
- [64. VPC Endpoint / PrivateLink](./64_vpc_endpoint_privatelink/README.md)
- [65. VPN / Direct Connect](./65_vpn_direct_connect/README.md)
- [66. VPC Flow Logs / Networking Troubleshooting](./66_vpc_flow_logs_troubleshooting/README.md)

## Examples와 직접 연결되는 핵심

특히 59, 60, 61, 62, 64, 66은 실습 전에 충분히 이해한다.

```text
VPC / CIDR
   ↓
Subnet
   ↓
Route Table
   ↓
IGW / NAT / Endpoint
   ↓
Security Group / NACL
   ↓
ALB / EC2 / RDS
   ↓
Flow Logs로 진단
```

63과 65는 SAA 선택 문제를 위해 개념과 사용 기준까지 이해하면 충분하며, 현재 core examples에서 직접 구축하지는 않는다.

## 완료 기준

아래 요청 흐름을 말로 추적할 수 있으면 된다.

```text
Internet Client
   ↓
IGW
   ↓
Public Subnet의 ALB
   ↓
Private Subnet의 EC2
   ↓
Private Subnet의 RDS
```

그리고 private EC2가 인터넷 또는 AWS 서비스로 나갈 때 어떤 경로를 사용하는지도 설명할 수 있어야 한다.
