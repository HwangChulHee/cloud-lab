---
id: NET-FD-001
title: 두 PC 간 Ethernet 통신과 ARP
level: CCNA
pass: A
prerequisites: []
tools: [Cisco Packet Tracer]
document_status: ready
lab_status: verified-core
---

# Lab 01 — 두 PC 간 Ethernet 통신과 ARP

> **목표:** 스위치를 통해 같은 서브넷의 PC 두 대가 통신할 때 ARP, MAC 학습, ICMP의 역할을 설명하고 직접 관찰한다.  
> **실습 상태:** 핵심 흐름 사용자 실습 검증 완료 · 선택 케이블 장애 미실시 · `.pkt` 파일 미첨부  
> **학습 순서:** 핵심 개념 → 토폴로지 구축 → 패킷 관찰 → 장애 진단 → 복습

## 1. 학습 목표와 선수 지식

- 동일 서브넷 내에서 IP 주소와 MAC 주소가 각각 수행하는 역할을 구분한다.
- 스위치의 출발지 MAC 학습과 브로드캐스트 전달을 설명한다.
- ARP Request/Reply와 ICMP Echo Request/Reply를 구분해 관찰한다.
- 의도적인 IP 설정/링크 장애를 진단하고 복구한다.

**선수 Lab:** 없음. 이더넷과 서브넷의 기본 개념은 아래에서 설명한다. 아직 라우터·기본 게이트웨이 설정은 필요 없다.

## 2. 실습 전 핵심 개념

### 왜 ARP가 필요한가?

PC-A가 PC-B의 IP 주소(192.168.10.20)를 알더라도, 같은 Ethernet LAN에서 프레임을 전송하려면 **B의 MAC 주소**를 알아야 한다. IPv4에서 이를 찾는 프로토콜이 ARP다.

- **Ethernet / 프레임:** 같은 링크 계층에서 전송되는 단위. 헤더에 출발지/목적지 MAC 주소가 있다.
- **MAC 주소:** Ethernet에서 장비 인터페이스를 구분하는 링크 계층 주소.
- **IPv4 / 서브넷 마스크:** 논리 주소와 로컬 네트워크 범위. `/24`는 이 예제에서 앞 24비트가 네트워크 부분임을 뜻한다.
- **ARP:** 로컬 IPv4 네트워크의 목적지 또는 다음 홉 IP에 대응하는 MAC을 확인한다.
- **스위치 MAC 테이블:** 수신한 프레임의 **출발지 MAC과 입력 포트**를 학습한다. 알려진 목적지 MAC은 해당 포트로 전달하고, 브로드캐스트와 미지의 유니캐스트는 VLAN 내 다른 포트로 플러딩한다.
- **ICMP Echo:** `ping`의 요청/응답 메시지. TCP·UDP 포트 번호를 사용하지 않는다.

### 실제 프레임이 이동하는 순서

PC-A = `192.168.10.10/24`, PC-B = `192.168.10.20/24`. 아래 MAC 값은 설명용 가상값이다.

1. A가 자신의 주소·서브넷 마스크를 보고 B가 같은 서브넷이라고 판단한다.
2. ARP 캐시에 B의 MAC이 없으면 A는 목적지 MAC `FF:FF:FF:FF:FF:FF`로 ARP Request를 브로드캐스트한다.
3. 스위치는 A의 **출발지 MAC**을 입력 포트에 학습하고 요청을 다른 포트로 전달한다.
4. B는 자신의 주소에 대한 ARP Request를 받고 B의 MAC 주소가 담긴 ARP Reply를 보낸다(통상 유니캐스트).
5. A는 ARP 캐시에 B의 IP–MAC 매핑을 저장하고, Ethernet 목적지 MAC을 B로 지정해 ICMP Echo Request를 전송한다.
6. 스위치는 학습된 MAC 테이블로 프레임을 전달하고 B의 Echo Reply가 되돌아온다.

**주의할 점:** ARP는 이 시나리오에서 각 PC가 실행하는 것이지 L2 스위치가 대신 주소를 찾아주는 것이 아니다. 다른 서브넷으로 전송한다면 PC는 목적지 호스트가 아닌 **기본 게이트웨이의 MAC**을 알아내야 한다. IPv6에서는 ARP 대신 Neighbor Discovery를 사용한다. 캐시 상태나 링크 초기화에 따라 최초 `ping`의 일부 응답이 실패할 수 있다.

### 실습 전 확인 질문

1. 목적지 IP를 알고 MAC을 모르면 처음 어떤 프레임을 보내는가?
2. 스위치는 출발지 MAC과 목적지 MAC 중 무엇으로 테이블을 학습하는가?
3. PC-B가 다른 서브넷에 있고 기본 게이트웨이가 없다면 A는 왜 전송할 수 없는가?

## 3. 토폴로지와 IP 설계

```text
PC-A Fa0 ---- Fa0/1 [Switch0 / 2960] Fa0/2 ---- Fa0 PC-B
```

| 장비 | 연결 인터페이스 | IPv4 | 마스크 | 게이트웨이 |
| --- | --- | --- | --- | --- |
| PC-A | FastEthernet0 | 192.168.10.10 | 255.255.255.0 | 비움 |
| PC-B | FastEthernet0 | 192.168.10.20 | 255.255.255.0 | 비움 |
| Switch0 | Fa0/1, Fa0/2 | 설정 불필요 | — | — |

사용 도구: **Cisco Packet Tracer** (PC 2개, Cisco 2960 L2 스위치 1개, Copper Straight-Through 2개).

## 4. 실습: 네트워크 구축

1. Packet Tracer를 열고 PC-A, PC-B와 2960 스위치를 배치한다.
2. PC-A Fa0 → Switch0 Fa0/1, PC-B Fa0 → Switch0 Fa0/2를 Copper Straight-Through(또는 자동 연결)로 잇는다.
3. 각 PC에서 **Desktop → IP Configuration**을 열고 주소 설계표의 IP와 마스크를 설정한다.
4. 링크 상태가 활성화될 때까지 확인한다. 최초 연결 시 스위치 포트 초기화로 약간의 대기가 필요할 수 있다.

## 5. 정상 통신 검증

PC-A의 **Desktop → Command Prompt**:

```text
ping 192.168.10.20
arp -a
```

첫 시도에 일부 타임아웃이 있으면 다시 Ping을 실행한다. `arp -a` 출력에서 `192.168.10.20`과 연결된 MAC을 확인한다(지원되는 Packet Tracer 버전에 따라 표시가 다를 수 있음).

Switch0의 CLI:

```text
enable
show mac address-table
show interfaces status
```

`show interfaces status`가 사용 중인 장비/버전에서 지원되지 않으면 `show interfaces fa0/1`·`show interfaces fa0/2`로 링크 상태를 확인한다.

**기대 결과:** Ping 성공, 스위치 MAC 테이블에 PC-A와 PC-B가 각자 연결된 포트로 학습된 항목 확인. 실제 MAC 주소는 실행 환경마다 다르므로 값 자체를 미리 단정하지 않는다.

## 6. 패킷 흐름 관찰 (Simulation Mode)

1. **Simulation Mode**로 전환하고 이벤트 필터에서 ARP와 ICMP를 선택한다.
2. 최초 ARP부터 보려면 새 토폴로지에서 시작하거나 캐시를 초기화한 후 PC-A에서 Ping을 보낸다.
3. **Capture/Forward**로 각 이벤트를 진행하면서 패킷 상세를 확인한다.
4. ARP Request에서 Ethernet 목적지 MAC이 브로드캐스트인지, 대상 IP가 `192.168.10.20`인지 확인한다.
5. ARP Reply에서 B의 IP·MAC 매핑을 확인한다.
6. ICMP Echo의 **IP 목적지는 B의 IP**, Ethernet **목적지 MAC은 B의 MAC**인지 확인한다.
7. `show mac address-table`의 입력 포트 학습 결과를 패킷의 출발지 MAC과 연결해 설명한다.

Packet Tracer Simulation Mode는 교육용 패킷 시각화로, Wireshark의 실제 pcap 캡처와는 구별한다.

## 7. 장애 재현 및 복구

### Case A — IP 대역 오류

1. 먼저 PC-A → PC-B 정상 Ping 성공을 기록한다.
2. PC-B를 `192.168.20.20/24`로 변경하고 게이트웨이는 비워둔다.
3. PC-A에서 `ping 192.168.20.20`을 실행한다. **실패 예상**: A는 목적지가 로컬 `192.168.10.0/24` 밖에 있는데 기본 게이트웨이가 없다.
4. PC-A의 IP/마스크/게이트웨이를 살펴 원인을 설명한다.
5. PC-B를 `192.168.10.20/24`로 되돌린 후 Ping 성공을 확인한다.

### Case B — 케이블 분리

1. 정상 상태에서 PC-B와 Switch0 사이 케이블을 제거한다.
2. Ping 결과, 링크 상태, MAC 테이블 변화를 관찰한다. 동적 MAC 항목은 일정 시간이 지난 뒤 삭제될 수 있다.
3. 케이블을 다시 연결하고 링크 활성화 및 Ping 복구를 확인한다.

### 진단 순서

**물리 링크 → 인터페이스 설정 → IP/서브넷 → ARP 캐시 → 스위치 MAC 테이블 → Ping 결과** 순서로 검증한다.

## 8. 복습과 다음 단계

- ARP Request가 브로드캐스트이고 Reply가 보통 유니캐스트인 이유는?
- 같은 LAN에 라우터가 없어도 Ping이 가능한 이유는?
- B를 다른 VLAN에 넣는다면 통신 경로에 무엇이 추가되어야 할까?
- 후속 학습: **서브넷·기본 게이트웨이 → VLAN → Inter-VLAN Routing → ARP 보안(DAI)**. 아직 없는 Lab 링크는 생성하지 않는다.

## 8-1. 종료 주관식 퀴즈 (실습 후 별도 진행)

> **상태: 완료 (2026-11-02, 주관식 2문항 통과).** 아래 2문항에 답했고 보완 설명까지 마쳤다. LLM은 질문을 한 번에 1개씩 출제하고 사용자가 답하기 전 모범 답안을 공개하지 않는다.

1. 같은 서브넷에서 PC0이 PC1로 Ping을 보내는 과정에서 **ARP·스위치·ICMP가 각각 어떤 역할을 하는지** 흐름으로 설명하라.
2. 목적지가 다른 서브넷이고 기본 게이트웨이가 없는 상황에서는 **왜 통신에 실패하는지** 설명하라.
3. (선택) Ping 실패만 보고 장애 원인을 단정할 수 없는 이유와 추가 확인 방법 한 가지를 말해보라.

**평가 기준:** 핵심 정확성, 원인과 결과의 연결, 관측 증거 사용. 부분적으로 맞으면 부족한 지점을 짚고 다른 사례로 재질문한다.

## 9. 실습 기록

- [x] 핵심 질문 설명 (Ethernet, LAN/WAN, VLAN, 서브넷, 게이트웨이, ARP/ICMP)
- [x] 토폴로지 구축
- [x] Ping 및 MAC 테이블 검증
- [x] ARP/ICMP 패킷 흐름 확인
- [x] 서브넷 불일치 장애 재현·원인 분석·복구
- [ ] 선택 과제: 케이블 분리 장애
- [x] 종료 주관식 퀴즈 (2문항 응답·피드백 완료, 통과)
- 수행일: 2026-11-02 (대화 및 사용자가 공유한 실행 화면 기준)
- Packet Tracer 버전: 미확인
- PC0 / PC1 실제 MAC: `0030.A372.9018` / `0060.2FE4.558C`
- 정상 Ping 및 ARP 관찰: Echo Reply 4/4 성공, `arp -a`에 `192.168.10.20 → 0060.2fe4.558c` 표시, 스위치 VLAN 1에서 Fa0/1·Fa0/2 동적 MAC 학습 확인.
- Simulation 관찰: ARP Request 브로드캐스트 → ARP Reply 유니캐스트 → ICMP Echo Request(Type 8) → Reply(Type 0).
- 오류 원인·복구 확인: PC1을 `192.168.20.20/24`로 변경했을 때 Ping 실패. PC0에서 동일 /24 밖 목적지임을 인식하고 기본 게이트웨이 부재로 패킷을 폐기하는 Simulation 메시지 확인. PC1 주소 복구 후 Ping 성공은 사용자 확인.
- 실제 실습 검증 여부: [x] 핵심 과정 (선택 케이블 장애 제외)

## 10. 실제 학습 기록 — 질문과 내부 동작 연결

> 본 기록은 대화에서 질문·확인한 사항만 압축했다. 추가로 설명한 개념을 **별도 Lab으로 실습했다고 간주하지 않는다.**

| 질문·혼동 지점 | 정리된 이해 | 확인 수준 / 후속 학습 |
| --- | --- | --- |
| 2960, Fa0/1의 숫자는? | 2960은 Cisco 제품군, Fa0/1은 FastEthernet 인터페이스 식별자. | 이론·장비 명칭 확인 |
| Ethernet·LAN·WAN·VLAN의 차이? | Ethernet은 L1/L2 기술, LAN/WAN은 망의 역할·범위 분류, VLAN은 L2 브로드캐스트 도메인의 논리적 분리. | 개념 토론, VLAN은 향후 Lab |
| Straight-Through와 Cross-Over? | 구리선을 펴는 것이 아니라 양 끝 RJ45 핀 배선 방식의 차이. Twisted Pair는 꼬인 선 구조이며 Auto-MDI/MDIX는 포트에서 송수신 방향을 자동 조정. | 개념 설명, Straight 케이블 실습 |
| 같은 서브넷 vs 같은 VPC? | 같은 서브넷의 직접 전달과 다른 서브넷의 L3 라우팅을 구별. AWS VPC는 local 라우트를 통해 서로 다른 서브넷의 사설 IP 통신을 제공할 수 있음. | 개념 비교, AWS 실습으로 오인하지 않음 |
| ARP는 누구에게 묻나? | PC가 ARP Request를 브로드캐스트하며, L2 스위치는 프레임 전달·출발지 MAC을 학습. 목적지 MAC 미학습 시 Unknown Unicast Flooding과 ARP 브로드캐스트의 차이를 구별. | Simulation에서 ARP Request/Reply 검증 |
| Ping·ICMP·TTL의 의미? | ICMP Echo Type 8 요청/Type 0 응답. TTL은 라우터 경유 시 감소, L2 스위칭 자체로는 감소하지 않음. | Simulation에서 Type 8/0 확인 |
| Ping timeout이면 서브넷 구분을 못한 걸까? | Timeout만으로 장애 원인 확정 불가. 다른 서브넷의 목적지는 라우팅 경로 확인 후 기본 게이트웨이가 없으면 전송 실패. | **직접 검증:** Packet Tracer에서 “destination ... not in same subnet” 및 “default gateway is not set ... drops the packet” 확인 |

### 다음 Lab에서 되짚기
- 서브넷 마스크 / CIDR 비트 계산과 기본 게이트웨이·라우팅 테이블 판정
- Broadcast와 Unknown Unicast Flooding의 차이
- VLAN을 실제로 분리하고 Inter-VLAN 라우팅 구성
- 선택 미수행: 케이블 분리와 링크 상태 변화

### 종료 주관식 퀴즈 학습 기록 (2026-11-02)

- **Q1 (ARP·Switch·ICMP 역할): 통과, 보완 1건.** ARP를 IP→MAC 확인, ICMP를 통신 확인에 사용하는 프로토콜로 정확히 설명. 스위치를 처음에는 '물리적 연결 장치'로 설명하여 **출발지 MAC 기반 학습 및 목적지 MAC 기반 프레임 포워딩**을 보충했다. ICMP는 Ping뿐 아니라 오류 알림에도 사용됨을 확인.
- **Q2 (다른 서브넷·게이트웨이): 통과.** 같은 서브넷은 L2 전달로 통신 가능하고, 다른 서브넷 간에는 L3 경로가 필요하다는 점을 올바르게 설명. 다만 목적지에 대한 구체적인 경로가 있으면 기본 게이트웨이 없이도 전달할 수 있다는 점을 추가 설명.
- **다음 복습 우선순위:** 스위치의 *MAC 학습과 전달 판단* / 라우팅 테이블의 *더 구체적인 경로와 기본 경로의 관계*.
- **채점 메모:** 추가 선택 3번 문항은 출제하지 않았으므로 미응답을 오답으로 처리하지 않음.

## 참고 자료

- [RFC 826 — ARP](https://www.rfc-editor.org/rfc/rfc826)
- [RFC 792 — ICMP](https://www.rfc-editor.org/rfc/rfc792)
- [Cisco Packet Tracer](https://www.netacad.com/courses/packet-tracer)
