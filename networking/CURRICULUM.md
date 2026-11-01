# Networking Curriculum — 실행 계획 v0.2

> 작성일: 2026-11-02. **A01 실습 핵심 경로 검증 및 주관식 퀴즈 통과**, A02~A30은 설계 단계이며 README·.pkt·명령 실행 검증은 아직 없다.

## 학습 목적

- **Pass A**: CCNA 핵심 이론과 작은 실습을 통해 패킷, 장비 내부 판단, 오류 복구를 이해한다.
- **Pass B**: ENCOR/ENARSI 기반 Enterprise 심화 (VLAN/STP/OSPF/BGP, 가용성·라우팅 정책·VRF·QoS·관측성).
- **Pass C**: VPN/보안/데이터센터/ISP/클라우드 전문화.
- **Pass D**: 다중 영역 통합 프로젝트, 운영 기록 및 장애 시뮬레이션.
- Pass A의 초기 20개는 빠른 첫 순환이며, 뒤쪽 10개로 물리·장비 관리·무선·자동화와 진단을 보강한다. **30개가 공식 CCNA 전체 출제항목을 100% 커버한다고 주장하지 않는다.** 공식 토픽과 별도 매핑 필요.

## 공통 Lab 운영 형식

1. Overview와 선수개념 → 실제 주소·프레임·패킷으로 내부 판단을 설명
2. 소규모 토폴로지 설계 → 한 단계씩 구성
3. CLI/Simulation/캡처를 통해 예상값과 실제값 비교
4. 의도된 장애(실패 증상 → 가설 → 근거 → 수정 → 재검증)
5. 핵심 주관식 **2~3문항**(원리 + 적용/장애), 피드백
6. 핵심 3가지 요약, 실습 증거, 학습 중 질문한 **추가 개념 메모**, 다음 Lab 선수 지식으로 연결

개별 Lab은 기본적으로 단일 README.md. 상태는 planned/ready와 not-tested/in-progress/verified-core/verified를 **독립적으로** 관리한다.

## Pass A — 30개 Lab 상세 백로그

| ID | Lab 이름 | 구축·내부 동작 관찰 | 유도 장애 | 선수 Lab |
|---|---|---|---|---|
| A01 | Ethernet·ARP·ICMP | 2 PC + L2 Switch; ARP Request/Reply, MAC learning | 서브넷 변경·게이트웨이 없음 | — |
| A02 | IPv4/CIDR·서브넷 설계 | /24·/26·/30 주소 설계, on-link 판정, ping 비교 | 마스크 오설정·중복 IP | A01 |
| A03 | 기본 게이트웨이·라우터 포워딩 | 2 LAN + R1, hop별 MAC 교체·TTL 변화 관측 | 게이트웨이 누락·역방향 경로 | A02 |
| A04 | 정적·기본 경로 | 3 라우터, route lookup/longest prefix, 리턴 경로 | 정적 경로 누락·잘못된 next hop | A03 |
| A05 | VLAN·Access 포트 | 2 VLAN 분리, broadcast 범위 관측 | 잘못된 access VLAN | A01,A02 |
| A06 | 802.1Q Trunk | 2 Switch, tagged/untagged, native VLAN | allowed VLAN 누락·native mismatch | A05 |
| A07 | Inter-VLAN Routing | Router-on-a-Stick 및 L3 SVI 비교 | subinterface/SVI·trunk 설정 오류 | A03,A06 |
| A08 | DHCPv4·Relay | DORA, 로컬/다른 VLAN DHCP | pool·helper 주소 오류 | A07 |
| A09 | DNS·TCP/UDP·HTTP | 이름 해석 → 3-way handshake → HTTP 흐름 | DNS 오설정·서비스 포트 실패 | A03 |
| A10 | NAT/PAT | inside/outside, translation table, source port | inside/outside 뒤바뀜·ACL 누락 | A04,A09 |
| A11 | IPv4 ACL | 표준/확장 ACL, 순서·implicit deny | 잘못된 순서·방향 | A07 |
| A12 | IPv6·NDP | 주소/Prefix·SLAAC·Neighbor Solicitation | prefix/default route 누락 | A03 |
| A13 | STP/RSTP | 삼각 스위치, 루프 차단·root bridge | 링크 중단·root 선정 오류 | A06 |
| A14 | EtherChannel/LACP | 2 링크 집성·port channel 상태 | 양쪽 mode 불일치 | A06 |
| A15 | OSPF 단일 영역 | 인접성·LSDB·SPF·route 변화 | area/네트워크/hello 불일치 | A04 |
| A16 | HSRP·게이트웨이 이중화 | VIP·active/standby·failover | 우선순위·uplink 장애 | A07 |
| A17 | Syslog·SNMP·NTP | 로그·시간·상태 수집 | time drift·로그 수신 실패 | A03 |
| A18 | WLAN·AP·WPA2/WPA3 개념 | SSID·채널·클라이언트 인증·WLC 범위 | 잘못된 PSK·채널 간섭 시뮬 한계 | A08 |
| A19 | WAN·터널 입문 | WAN 연결과 GRE/IPsec 개념·캡슐화 비교 | route/tunnel endpoint 누락; 구현 환경 분리 | A04 |
| A20 | 소규모 기업망 통합 | VLAN+InterVLAN+DHCP+ACL+NAT+Syslog | 복수 장애, 단계별 isolation | A07,A08,A10,A11,A17 |
| A21 | 물리 계층·인터페이스 진단 | copper/fiber, duplex/speed, counters | duplex/speed mismatch 및 cable fault | A01 |
| A22 | 스위치 보안 | port-security·DHCP snooping·DAI 개념 | MAC violation·rogue DHCP | A05,A08 |
| A23 | CDP/LLDP·SSH·관리 접속 | neighbor discovery·관리 VLAN·AAA 입문 | 관리 IP·VTY/SSH 오설정 | A06 |
| A24 | FHRP·라우트 선택 종합 | static/OSPF/HSRP 복합 경로 failover | cost·AD·floating route | A15,A16 |
| A25 | IP 서비스 확장 | DHCP troubleshooting·DNS·NTP·QoS 표식 기초 | DHCP scope·DNS·시계 오염 | A08,A09,A17 |
| A26 | WLC·무선 보안 | WLC·WLAN·PSK/802.1X 구분 및 클라이언트 확인 | association·authentication 실패 | A18 |
| A27 | L2/L3 보안 종합 | ACL, port security, device hardening, segmentation | 정책 허용/차단 뒤집힘 | A11,A22,A23 |
| A28 | REST·JSON·기초 자동화 | API polling, JSON, Python/Ansible 설정 비교 | 인증/파싱·idempotency 오류 | A17 |
| A29 | Wireshark·트러블슈팅 | capture, ARP/DNS/TCP/ICMP와 PT 차이 | 실패 원인 추정→검증 | A09,A21 |
| A30 | CCNA 종합 운영 시나리오 | 다수 VLAN/라우터/무선/ACL/관측 | 숨겨진 3종 장애와 변경/롤백 | A20,A24,A26,A27,A28,A29 |

- 위 ID는 **계획 식별자**다. 실제 파일 메타데이터의 고유 ID는 기존 `NET-FD-001`처럼 분야별 불변 ID를 부여한다. Lab 경로는 각 분야 폴더에 분배하고 학습 순서는 이 표로 관리한다.
- 모든 Lab은 내부 동작/검증/오류 유도/복구/종료 퀴즈·질문 기록이 필수. Packet Tracer로 지원되지 않는 세부 패킷 또는 무선 기능은 Wireshark·Linux·GNS3로 대체하며 구현 전 기능 지원을 확인한다.
- A19는 터널 기본 개념 중심이며 **강한 IPsec 구현이 완료된 것으로 간주하지 않는다**.

## Pass B — Enterprise 심화 백로그 (12개 묶음)

| 순서 | 실습 묶음 | 핵심 관찰 · 장애 |
|---|---|---|
| B01 | Campus 이중화 STP/MST·EtherChannel | topology change, blocked port, link failover |
| B02 | OSPF 다중 영역 | LSA 유형, SPF·ABR, adjacency 불일치 |
| B03 | OSPF 경로 조정 | cost·summarization·filter와 불안정 경로 |
| B04 | eBGP 기본·AS_PATH | TCP 179 session, best path, 경로 광고 |
| B05 | BGP 정책 | local preference·MED·filter·route map |
| B06 | 재분배·PBR | routing loop/feedback, policy match |
| B07 | VRF·분리 라우팅 | 테이블 분리, route leaking |
| B08 | Gateway HA·ECMP·QoS | failover, hash, queue/drop |
| B09 | L2/L3 운영 보안 | AAA, 802.1X 개념, L2 방어·ACL |
| B10 | IP SLA·NetFlow·모니터링 | 텔레메트리·증거 기반 원인 분석 |
| B11 | Ansible·RESTCONF/NETCONF | 설정 자동화·검증·롤백 |
| B12 | Enterprise 장애 복합 실습 | 2개 이상 독립 장애, 운영 보고 |

## Pass C — 전문화 백로그 (12개 묶음)

| 순서 | 실습 묶음 | 도구·핵심 |
|---|---|---|
| C01 | GRE, IPsec site-to-site | Linux strongSwan / 허가된 네트워크 OS 이미지 |
| C02 | WireGuard·Remote Access | Linux namespace/VM, routing·MTU |
| C03 | Firewall·DMZ·NAT 정책 | OPNsense/pfSense, stateful filtering |
| C04 | IDS/IPS·침해 탐지 | Suricata/Zeek, 합법적 자체 랩 트래픽 |
| C05 | 중앙 로그·보안 이벤트 대응 | Syslog, correlation, playbook |
| C06 | Leaf-Spine·BGP underlay | ECMP, link failure |
| C07 | VXLAN/EVPN overlay | VTEP·MAC/IP reachability, route type |
| C08 | 데이터센터 보안·멀티테넌시 | VRF, segmentation, underlay/overlay isolation |
| C09 | ISP eBGP·정책 | AS_PATH, route filter, peering |
| C10 | ISP 멀티호밍·장애 전환 | provider failure, path selection |
| C11 | AWS VPC·VPN·TGW | route table, SG/NACL, hybrid |
| C12 | Kubernetes CNI·서비스 경로 | Pod/Node/Overlay, kube-proxy, NetworkPolicy |

## Pass D — 통합 프로젝트 (3개)

1. **기업 본사·지사 네트워크**: VLAN, OSPF, HA, ACL, VPN, Syslog, 장애 대응 보고서
2. **데이터센터 Fabric**: BGP Underlay + ECMP + VXLAN/EVPN + 분리/장애 복구
3. **ISP/Cloud Hybrid**: 다중 AS + 멀티호밍 + 사설망/클라우드 경로 + 운영·보안 관측

각 프로젝트 산출물: 주소/토폴로지 설계, 설정·검증 증거, 장애 시나리오, runbook, 복구 확인, 학습 회고.

## 공식 범위 및 도구 검증

- Cisco CCNA 200-301 **v1.1은 2027-02-02까지**, **v2.0은 2027-02-03부터** 시행 예정. 추후 주제별 매핑 시점의 공식 최신 PDF를 따른다.
- CCNA v2.0은 물리 인터페이스/배선 진단, IPv4·IPv6·DHCP 트러블슈팅, 네트워크 운영·AI 지원 내용을 다루므로 A21/A28~A30에서 보강한다.
- ENCOR 350-401 / ENARSI 300-410은 공식 시험 주제와 개별 Lab별 매핑을 확정하기 전까지 *학습 방향*으로만 분류한다.
- Packet Tracer는 핵심 CCNA 토폴로지. Wireshark는 실제 캡처, GNS3/Containerlab·Linux는 고급 프로토콜 및 시스템 동작, AWS/K8s는 후속 확장.
- 공식 참조: https://learningcontent.cisco.com/documents/marketing/exam-topics/200-301_CCNA_v2.0_Exam_Topics_PDF.pdf
- 공식 참조: https://www.cisco.com/site/us/en/learn/training-certifications/exams/ccna.html
- 공식 참조: https://www.cisco.com/site/us/en/learn/training-certifications/exams/encor.html
- 공식 참조: https://www.cisco.com/site/us/en/learn/training-certifications/exams/enarsi.html

## 후속 제작 우선순위

1. A02 서브넷 설계 → A03 게이트웨이/라우터 → A04 정적 라우팅: **Lab 01의 질문 및 오개념을 그대로 후속 관측으로 연결**.
2. A05 VLAN → A06 Trunk → A07 Inter-VLAN: 실제 L2와 L3 경계 명확히 확인.
3. A08~A11 서비스·보안 완성, 이후 영역별 확장.
4. 각 Lab을 작성할 때 선수 ID, CLI 지원, 장비 모델, 기대 출력, 실제 수행 상태 검증.

