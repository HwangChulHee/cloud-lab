---
id: NET-RT-001
title: Lab 03 — 기본 게이트웨이와 라우터의 패킷 포워딩
level: CCNA
pass: A
prerequisites: [NET-FD-002]
tools: [Cisco Packet Tracer]
document_status: ready
lab_status: not-tested
---

# Lab 03 — 기본 게이트웨이와 라우터의 패킷 포워딩

> **상태:** 문서 작성 완료 · 실습과 명령 출력은 아직 검증하지 않음. GPT는 각 단계에서 실제 사용자 결과를 확인하고 다음 단계로 진행한다.

## 1. Overview
목표: 서로 다른 두 /24 LAN 사이에 라우터를 배치하고, 호스트의 라우팅 판단·ARP·홉별 Ethernet 헤더 변경·IP TTL을 관찰한다. [Lab 02](../../01-foundation/02-ipv4-subnetting/README.md)에서 관찰한 off-link 패킷 폐기를 게이트웨이로 해결한다.

**성공 기준:** 양방향 Ping, 각 PC ARP 테이블과 라우터 ARP/직접 연결 경로 확인, Simulation에서 ingress/egress L2 MAC 변경 확인, 게이트웨이 오류 및 복구 완료.

## 2. 핵심 개념과 내부 동작
- **Gateway(관문):** 이 Lab에서 호스트의 직접 연결 네트워크 밖으로 패킷을 보내기 위한 *다음 홉* 라우터 인터페이스. 아무 라우터나 되는 게 아니라 호스트가 L2로 도달할 수 있어야 한다.
- **Routing(경로 선택):** 목적지 IP에 일치하는 라우팅 테이블 항목으로 출력 인터페이스와 다음 홉을 결정. 더 구체적인 prefix 경로가 우선되는 일반 원리는 뒤 Lab에서 확장.
- **ARP:** 다른 서브넷의 PC를 찾는 ARP가 아니라 **같은 LAN에 있는 게이트웨이 IP의 MAC**을 찾아 Ethernet 프레임을 구성.
- **MAC 주소는 홉별로 교체:** 라우터가 입력 Ethernet 헤더를 벗겨 IP 목적지를 보고 경로를 찾은 후 출력 링크용 Ethernet 헤더를 새로 씌운다. IP 목적지·출발지는 보통 그대로이고 **TTL은 라우터 포워딩마다 감소**한다. IP 헤더 체크섬도 IPv4에서 갱신. NAT는 수행하지 않는다.
- **돌아오는 경로:** 요청 전달 성공만으로 Ping 성공을 보장하지 않는다. Reply를 보낼 PC1도 올바른 게이트웨이가 필요하다.

### 실제 패킷 흐름 (개념적 MAC)
1. PC0 `192.168.10.10/24`에서 PC1 `192.168.20.20`으로 Ping.
2. PC0은 off-link로 판단, PC0의 gateway `192.168.10.1`에 대한 ARP. 예시 R1 LAN10 MAC=R10.
3. Ethernet `PC0_MAC → R10`; IP `192.168.10.10 → 192.168.20.20`.
4. R1은 `192.168.20.0/24` 직접 연결 경로를 선택, PC1 MAC을 ARP로 해결.
5. 새 Ethernet `R20 → PC1_MAC`; IP 출발/목적은 동일, TTL 감소.
6. PC1은 응답을 자신의 gateway `192.168.20.1`로 보내며 역순으로 귀환한다.

**이해 확인:** PC0이 PC1 MAC 대신 게이트웨이 MAC을 찾는 이유는? R1의 두 인터페이스 MAC은 왜 달라야 하나?

## 3. 토폴로지와 주소 설계
```text
PC0 Fa0 -- Fa0/1 SW-A Fa0/24 -- G0/0 R1 G0/1 -- Fa0/24 SW-B Fa0/1 -- Fa0 PC1
```
Packet Tracer PC 2대, 2960 Switch 2대, GigabitEthernet 포트가 두 개 이상 있는 1941 Router 1대 권장. 스위치 Fa0/24↔라우터 G0/x, PC↔스위치 Fa0/1. 모든 링크 copper straight-through. 실제 모델의 포트 표기를 우선 확인.

| 노드 | Interface | IP / Prefix | Gateway |
|---|---|---|---|
| PC0 | Fa0 | 192.168.10.10/24 | 192.168.10.1 |
| R1 | G0/0 | 192.168.10.1/24 | — |
| R1 | G0/1 | 192.168.20.1/24 | — |
| PC1 | Fa0 | 192.168.20.20/24 | 192.168.20.1 |

## 4. 단계별 구축 (GPT는 한 단계씩 안내)
1. 장비를 배치하고 배선, 인터페이스 명칭·링크 상태 확인.
2. PC0/PC1에서 Desktop → IP Configuration으로 주소·마스크·gateway 입력.
3. R1 CLI에서 아래 설정을 입력. 프롬프트/장비 실제 인터페이스를 먼저 확인한다.

```ios
enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 description TO_LAN10
 ip address 192.168.10.1 255.255.255.0
 no shutdown
exit
interface gigabitEthernet0/1
 description TO_LAN20
 ip address 192.168.20.1 255.255.255.0
 no shutdown
end
```
4. `show ip interface brief`에서 G0/0·G0/1가 **up/up**인지 확인. 다르면 배선·shutdown·STP 대기부터 확인.
5. `show ip route`에서 `C 192.168.10.0/24`와 `C 192.168.20.0/24`를 찾아 직접 연결 경로 설명.

## 5. 검증 및 패킷 관찰
PC0 `ipconfig` → `ping 192.168.10.1` → `ping 192.168.20.20` → `arp -a`; PC1에서도 역방향 `ping 192.168.10.10`.

R1:
```ios
show ip interface brief
show ip route
show arp
```
- **기대:** PC0의 ARP 엔트리는 `192.168.10.1`(게이트웨이)이어야 한다. PC1 `192.168.20.20` MAC을 로컬 ARP로 직접 찾지 않는다.
- Simulation ARP/ICMP 필터: PC0→R1 구간과 R1→PC1 구간 **Ethernet src/dst MAC**, IP src/dst, TTL 비교. ARP 캐시가 이미 찼다면 초기화 후 재실행. Packet Tracer 세부 표시·첫 Ping 일부 지연은 버전에 따라 다름.
- Reply 방향도 같은 항목으로 검증. 단순 Ping 성공만으로 홉별 동작을 검증했다고 표시하지 않는다.

## 6. 장애 재현과 복구
**필수 A — PC0 gateway 누락:** 정상 구성/통신 확인 후 PC0 Default Gateway를 비운다. PC0→PC1 ping 실패, PC0→R1(.1) ping은 성공할 수 있음. `ipconfig`와 Simulation으로 PC0이 off-link 목적지 송신 시 실패하는 곳 확인. gateway 복원 후 양방향 Ping 재검증.

**필수 B — 응답 경로 장애:** 정상 상태로 복귀한 뒤 PC1 gateway를 제거한다. PC0 요청이 PC1에 도달하는지, PC1 응답이 왜 실패하는지 Simulation으로 각각 관찰. PC1 gateway를 복원하고 Ping 재검증. **실제 UI의 처리 순서는 관측 후 기록**한다.

**선택:** R1 G0/1 `shutdown` → 직접 연결 경로 변화·링크 down 확인 → `no shutdown` 복원. 물리 포트 상태에 따라 인터페이스는 down/down 또는 administratively down 등으로 보일 수 있다.

진단 순서: 링크 → PC IP/Mask/GW → R1 인터페이스 → R1 route → 각 구간 ARP → 요청/응답 방향.

## 7. 종료 주관식 (기본 2문항)
1. 다른 서브넷의 PC로 Ping할 때 송신 PC가 왜 목적지 PC가 아닌 게이트웨이의 MAC을 찾는지 설명해 봐.
2. 라우터를 지날 때 Ethernet MAC 주소와 IP 출발지/목적지, TTL은 각각 어떻게 변하며 왜 그런지 설명해 봐.
3. (필요시) 한 방향 Ping 요청은 도착하지만 응답이 돌아오지 않을 때 먼저 어디를 점검할까?

## 8. 핵심 3가지와 다음 Lab
- 게이트웨이는 off-link 목적지로 나가기 위한 로컬 다음 홉이다.
- 라우터는 IP 목적지로 경로를 고르고 L2 프레임을 링크마다 새로 만든다.
- 양방향 경로가 모두 필요하다. 다음 [Lab 04](../02-static-routing/README.md)에서는 라우터 여러 대 사이의 경로를 추가한다.

## 9. 실습·퀴즈 진행 기록
- [ ] 개념·질문 확인
- [ ] 구축·라우터 인터페이스 검증
- [ ] 양방향 Ping·ARP·라우팅 테이블 확인
- [ ] Simulation 홉별 L2/IP/TTL 관측
- [ ] 필수 A/B 장애·복구
- [ ] 종료 주관식 2~3문항
- 수행일 / Packet Tracer 버전 / 실제 출력: **미실시**
- 선택 실습: [ ] R1 링크 장애

## 10. 실제 질문·학습 메모 (Lab 종료 후만 작성)
| 실제 사용자 질문·오개념 | 교정된 이해 | 패킷/CLI 증거 | 다음 복습 |
|---|---|---|---|
| 미실시 | — | — | — |

