# Networking Curriculum — 초안 v0.1

## 목표와 범위

- CCNA의 기본 L2/L3·IP 서비스·보안·무선·자동화를 실습 중심으로 습득.
- CCNP Enterprise: ENCOR 핵심 영역과 ENARSI의 고급 라우팅·VPN·문제 해결로 확장.
- CCNP Security / Data Center 전체 시험 합격용 코스가 **아니며**, 관련 전문 주제는 추가 심화 트랙으로 다룬다.
- 136개는 *초기 아이디어의 상한 규모 추산*으로 확정된 Lab 개수가 아니다. 하나의 의미 있는 실습을 기준으로 쪼개되 중복 Lab은 통합한다.

## 분야별 폴더 (추후 콘텐츠 추가 시 생성)

| 코드 | 분야 | 주요 내용 | 기준 레벨 |
| --- | --- | --- | --- |
| 01-foundation | 기초 | Ethernet, MAC, ARP, 주소 설계, IPv4/IPv6, ICMP | CCNA |
| 02-switching | L2 | VLAN, Trunk, STP/RSTP, LACP, 보안 기능 | CCNA→ENCOR |
| 03-routing | L3 | 정적 경로, OSPF, BGP, 재분배, 정책 | CCNA→ENARSI |
| 04-network-services | IP 서비스 | DHCP, DNS, NAT/PAT, NTP, IPv6 | CCNA |
| 05-wireless | 무선 | WLAN, WLC, 인증, 설계 | CCNA→ENCOR |
| 06-security | 보안 | ACL, AAA, Firewall, DMZ, IDS/IPS | CCNA→전문화 |
| 07-vpn-wan | 터널/WAN | GRE, IPsec, WireGuard, VRF, MPLS | ENARSI→전문화 |
| 08-high-availability-qos | 가용성 | HSRP, ECMP, QoS, 장애 전환 | ENCOR |
| 09-operations | 운영 | SNMP, Syslog, NetFlow, 패킷 분석 | CCNA→ENCOR |
| 10-automation-sdn | 자동화 | REST API, JSON, Python, Ansible, SDN | CCNA→ENCOR |
| 11-datacenter | DC 네트워크 | Leaf-Spine, Underlay, VXLAN/EVPN | 전문화 |
| 12-isp-internet | 인터넷/ISP | ASN, 피어링, 경로 정책, 멀티호밍 | 전문화 |
| 13-cloud-hybrid | 클라우드 | AWS VPC, VPN, Transit Gateway, K8s CNI | 전문화 |
| 14-scenarios | 복합 실습 | 2~4개 기술 결합, 장애 시나리오 | 중급→심화 |
| 15-projects | 대형 프로젝트 | 기업 WAN·데이터센터·ISP/Hybrid | 최종 |

## 나선형 학습: 한 분야만 끝까지 파지 않기

### Pass A — 기초 (CCNA 중심)
1. Ethernet·ARP → IPv4·서브넷 → 스위칭/VLAN
2. 기본 라우팅 → DHCP/DNS/NAT → ACL
3. 무선 기초 → 기초 운영/모니터링 → 자동화 입문
4. 작은 복합 시나리오로 연결

### Pass B — 심화 (ENCOR/ENARSI 중심)
1. STP·EtherChannel·게이트웨이 이중화 → OSPF 고급
2. BGP 피어링/정책 → 재분배·VRF → WAN/VPN 기초
3. QoS·Network Assurance → API·자동화 → 복합 장애 진단

### Pass C — 전문화 (선택 심화)
1. IPsec·Remote Access·WireGuard 및 방화벽 운영
2. IDS/IPS·세그멘테이션·중앙 로그
3. Leaf-Spine → BGP Underlay → VXLAN/EVPN
4. ISP 멀티호밍 → AWS·Kubernetes 하이브리드 연결
5. 최종 통합 프로젝트 3종: 기업 WAN, 데이터센터, ISP/Hybrid

## 예시: BGP 나선형 연결

| 단계 | 선행 개념 | 실습 |
| --- | --- | --- |
| A | IP 라우팅, ASN 개념 | 두 라우터의 eBGP 경로 광고 |
| B-1 | BGP 기본, 경로 선택 | Local Preference, AS_PATH, 필터링 |
| B-2 | iBGP, 경로 정책 | RR/재분배/실패 시나리오 |
| C-1 | IP Fabric, ECMP | Leaf-Spine BGP Underlay |
| C-2 | ISP 운영 | 두 ISP 멀티호밍, 회선 장애 복구 |

## Lab 문서 및 의존성 규칙

- 각 독립 Lab은 기본적으로 **README.md 단일 파일**에 핵심 개념 → 토폴로지 → 구축 → 검증 → 장애 분석 → 복습을 담는다.
- 각 Lab에 고유 ID, 선수 Lab ID, 난이도, 나선형 Pass, 사용 도구와 문서/실습 상태를 기록한다.
- 선수 Lab은 실제 존재하는 항목만 참조한다. 미래 Lab은 링크 대신 학습 주제로 기재한다.
- [공통 템플릿](./templates/LAB-TEMPLATE.md) 및 [NET-FD-001](./01-foundation/01-ethernet-arp/README.md)을 기준으로 확장한다.

## 실습의 공통 완료 기준

- **이론**: 개념·필요성·프레임/패킷 처리 순서를 설명.
- **구축**: 주소 설계표와 장비별 설정을 재현.
- **검증**: 정상 성공뿐 아니라 예상되는 실패/격리도 확인.
- **진단**: 출력·로그·패킷 흐름의 근거와 함께 원인 규명.
- **복구**: 수정 후 재검증, 필요하면 원래 토폴로지 복원.
- **기록**: 문서 작성 / 실제 실습 수행 / 검증 완료를 구분 체크.

## 시험 범위 관리

CCNA, 350-401 ENCOR, 300-410 ENARSI의 **공식 시험 토픽을 별도 대조표로 관리**한다. 시험 업데이트와 시뮬레이터 지원 차이를 확인하기 전에는 특정 Lab이 공식 시험의 모든 요구사항을 충족한다고 주장하지 않는다.

공식 자료:
- https://www.cisco.com/site/us/en/learn/training-certifications/exams/ccna.html
- https://www.cisco.com/site/us/en/learn/training-certifications/exams/encor.html
- https://www.cisco.com/site/us/en/learn/training-certifications/exams/enarsi.html
- https://www.netacad.com/courses/packet-tracer

## 계획된 3개 통합 프로젝트

1. 기업 본사-지사 WAN: VLAN, OSPF, 방화벽, IPsec, 관측성, 이중화.
2. 데이터센터 Fabric: Leaf-Spine, BGP/ECMP, VXLAN/EVPN, 격리, 장애 대응.
3. ISP/Hybrid: 다중 AS, 피어링/멀티호밍, 사설망과 클라우드 연결.

현재 프로젝트는 **계획 상태**이고, 단계별 개별 Lab을 학습한 뒤 구현한다.
