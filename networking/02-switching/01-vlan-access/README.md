---
id: NET-SW-001
title: Lab 05 — VLAN, Access Port와 브로드캐스트 도메인
level: CCNA
pass: A
prerequisites: [NET-FD-002]
tools: [Cisco Packet Tracer]
document_status: ready
lab_status: not-tested
---

# Lab 05 — VLAN, Access Port와 브로드캐스트 도메인

> **상태:** 문서 작성 완료 · 실습과 명령 출력은 아직 검증하지 않음. GPT는 각 단계에서 실제 사용자 결과를 확인하고 다음 단계로 진행한다.

## 1. Overview
목표: 하나의 2960 스위치에서 VLAN 10/20을 구성하고 동일/다른 VLAN의 ARP 브로드캐스트·MAC 테이블·Ping 차이를 관찰한다. 물리 포트가 같은 스위치에 있다는 사실과 **L2 브로드캐스트 도메인이 같다**는 것은 다르다.

선수: [Lab 01](../../01-foundation/01-ethernet-arp/README.md), [Lab 02](../../01-foundation/02-ipv4-subnetting/README.md). Inter-VLAN 라우팅은 이 Lab의 범위가 아니며 후속 Lab 07에서 다룬다.

## 2. 핵심 개념과 내부 판단
- **VLAN = Virtual Local Area Network:** 같은 물리 스위치에서 논리적으로 분리한 L2 브로드캐스트 도메인.
- **Access Port:** 하나의 VLAN에 속하는 최종 단말 연결 포트. 일반적인 access 포트로 나가는 Ethernet 프레임은 802.1Q VLAN 태그가 붙지 않는다(특수 음성 VLAN 등은 별도).
- **CAM/MAC Table:** 스위치는 출발지 MAC을 **VLAN + MAC + 수신 포트** 조합으로 학습하고, 같은 VLAN 안에서 목적지 MAC에 따라 전달. 모르는 목적지 MAC/브로드캐스트를 다른 VLAN에 무조건 퍼뜨리지 않는다.
- **VLAN은 L2 범위 구분, Subnet은 L3 범위:** 관례적으로 VLAN별로 서로 다른 IP 서브넷을 할당하지만 두 개념은 동일하지 않다.
- **통신의 충분조건이 아님:** 같은 VLAN이어도 PC의 IP/Mask가 맞지 않으면 통신이 실패할 수 있다. 다른 VLAN 간 통신에는 라우터나 L3 스위치의 Inter-VLAN Routing 필요.
- 이 Lab은 *스위치 내부에서 ARP 브로드캐스트가 VLAN을 넘어가지 않는 것*을 직접 검증한다. PC0이 서로 다른 IP 서브넷이라고 판단하면 ARP를 내보내지 않으므로, L2 격리 관찰을 위해 **초기 테스트에서는 동일 IP 서브넷에 배치**한다.

## 3. 토폴로지와 주소 계획
```text
        Fa0/1 PC0 (.10) -- VLAN 10
        Fa0/2 PC1 (.20) -- VLAN 10
SW0 2960
        Fa0/3 PC2 (.30) -- VLAN 20
        Fa0/4 PC3 (.40) -- VLAN 20
```
2960 1대, PC 4대, Copper Straight-Through 4개, 전부 같은 `192.168.10.0/24` 사용, gateway 비움. 이 구성은 VLAN L2 격리 그 자체를 보여주기 위한 **의도적 주소 계획**이다.

| 장비 | IPv4/Mask | 스위치 포트 | VLAN |
|---|---|---|---|
| PC0 | 192.168.10.10/24 | Fa0/1 | 10 |
| PC1 | 192.168.10.20/24 | Fa0/2 | 10 |
| PC2 | 192.168.10.30/24 | Fa0/3 | 20 |
| PC3 | 192.168.10.40/24 | Fa0/4 | 20 |

## 4. 장비 구성
1. 4대 PC 배치·배선, 각 PC IP/Mask 설정. 초기 스위치의 VLAN 1에서 PC 간 Ping이 되는지 기준 확인(ARP 캐시가 차면 Simulation에서 초기화).
2. Switch0 CLI:

```ios
enable
configure terminal
vlan 10
 name USERS_A
exit
vlan 20
 name USERS_B
exit
interface range fastEthernet0/1 - 2
 switchport mode access
 switchport access vlan 10
exit
interface range fastEthernet0/3 - 4
 switchport mode access
 switchport access vlan 20
end
```
3. `show vlan brief`에서 Fa0/1~2는 VLAN10, Fa0/3~4는 VLAN20에 속하는지 확인. 지원되는 모델이 다르면 range 문법 대신 개별 인터페이스에서 설정.
4. 링크/STP 전환이 끝난 뒤 PC0→PC1 및 PC2→PC3 정상 Ping, PC0→PC2 실패를 확인.

## 5. 관측·패킷 분석
```ios
show vlan brief
show mac address-table
show interfaces fastEthernet0/1 switchport
```
- PC0 `ping 192.168.10.20` 성공, PC2 `ping 192.168.10.40` 성공 예상.
- PC0 `ping 192.168.10.30` 실패: IP는 같은 /24라 PC0이 ARP 브로드캐스트를 내보내지만, Switch0이 VLAN10에만 플러딩. VLAN20 PC2는 받지 못한다.
- PC0 `arp -a`에서 .20이 있을 수 있지만 .30은 ARP timeout 이후 미해결. 실제 출력 기준으로 해석.
- Simulation ARP 필터로 PC0→SW0→PC1 도달, PC2/PC3 **미도달** 확인. Switch0의 VLAN별 MAC 학습 항목도 확인한다.
- 스위치 목적지 MAC 기반 전달과 VLAN 분리는 두 판단이 함께 작용한다. VLAN이 같다고 무조건 모든 유니캐스트 프레임이 브로드캐스트되는 것은 아니다.

## 6. 장애 재현과 복구
**필수 A — PC1의 VLAN 오배치:** VLAN10에서 PC0↔PC1 성공을 확인한 뒤 Fa0/2를 VLAN20으로 이동:
```ios
configure terminal
interface fastEthernet0/2
 switchport access vlan 20
end
show vlan brief
```
PC0→PC1이 실패하고 VLAN10의 ARP 브로드캐스트가 Fa0/2로 전달되지 않는지 Simulation에서 확인. `show vlan brief`로 원인 추적하고 Fa0/2를 VLAN10으로 복구, Ping 확인. 캐시가 남아 있다면 `arp -d`로 정리한 다음 다시 관찰.

**선택 B — 같은 VLAN의 서브넷 마스크 오류:** PC1을 `192.168.10.20/28`로 잘못 설정하고 PC0(`.10/24`)과의 양방향 판단을 비교. Lab 02에서 이미 다룬 내용이라 개념 복습에만 사용하고 선택 실습으로 둔다. 복원 시 /24.

## 7. 종료 주관식 (2~3문항)
1. 같은 물리 스위치라도 VLAN이 다르면 왜 ARP 브로드캐스트가 상대 PC까지 전달되지 않는지 설명해 봐.
2. VLAN 10/20을 각기 다른 IP 서브넷으로 사용하는 설계가 일반적이지만 VLAN과 서브넷 자체는 다른 개념인 이유는?
3. (필요시) VLAN 오배치로 통신 실패할 때 `show vlan brief`와 ARP 관찰을 어떻게 연결할 수 있을까?

## 8. 핵심 3가지 및 후속 학습
- VLAN은 L2에서 브로드캐스트 도메인을 나눈다.
- MAC 테이블은 VLAN별로 학습하며 다른 VLAN 간 프레임을 임의로 전달하지 않는다.
- 다른 VLAN 사이 통신은 별도의 L3 라우팅 경로가 있어야 한다. 후속 Lab 06 802.1Q Trunk → Lab 07 Inter-VLAN Routing.

## 9. 실습 증거/진도
- [ ] 개념 설명·이해 확인
- [ ] 4 PC + SW 구성 및 VLAN 1 기준 통신 확인
- [ ] VLAN10/20 생성 및 Access 할당
- [ ] VLAN 내부 Ping, VLAN 간 실패 확인
- [ ] ARP 브로드캐스트 및 VLAN별 MAC 학습 관찰
- [ ] VLAN 오배치 장애·복구
- [ ] 종료 주관식 2~3문항
- [ ] 선택: 같은 VLAN의 서브넷 오류
- 수행일/Packet Tracer 버전/실제 출력: **미실시**

## 10. 실제 질문·학습 기록
| 실제 질문/오개념 | 핵심 설명 | 실습 증거 | 추후 연결 |
|---|---|---|---|
| 미실시 | — | — | — |

