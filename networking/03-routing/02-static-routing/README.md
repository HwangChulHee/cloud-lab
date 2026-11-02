---
id: NET-RT-002
title: Lab 04 — 정적 경로, 기본 경로와 Longest Prefix Match
level: CCNA
pass: A
prerequisites: [NET-RT-001]
tools: [Cisco Packet Tracer]
document_status: ready
lab_status: not-tested
---

# Lab 04 — 정적 경로, 기본 경로와 Longest Prefix Match

> **상태:** 문서 작성 완료 · 실습과 명령 출력은 아직 검증하지 않음. GPT는 각 단계에서 실제 사용자 결과를 확인하고 다음 단계로 진행한다.

## 1. Overview
목표: 라우터 3대 및 양 끝 LAN을 연결하여 **직접 연결 경로만으로는 멀리 있는 LAN에 접근하지 못함**, 정적 라우트·반환 경로, 기본 경로·Longest Prefix Match(LPM)를 검증한다.

선수: [Lab 03](../01-default-gateway/README.md), CIDR. 구성은 작은 토폴로지로 시작하고 초기 정상 실패를 관찰한 후 경로를 추가한다.

## 2. 핵심 개념 및 내부 처리
- **Routing Table**: 목적지 prefix, 다음 홉 또는 출력 인터페이스, 출처(C/L/S 등), 메트릭 등을 가진 경로 집합.
- **Static Route**: 운영자가 `ip route 목적지 mask next-hop`으로 지정한 경로. 상대 라우터가 알아서 상대방 LAN 경로를 학습하지 않는다.
- **Default Route**: 더 구체적인 경로가 없을 때 사용하는 `0.0.0.0/0`.
- **LPM**: 목적지에 일치하는 후보 경로 중 **prefix 길이가 가장 긴 경로**를 우선 선택. 서로 다른 프로토콜 간 AD 비교는 *같은 prefix의 후보 경로 선택*과 구분한다.
- **Forward vs Return**: ICMP Echo Request와 Reply는 독립적으로 라우팅되므로 양방향 경로가 필요.
- **TTL**: 라우터마다 감소. IPv4 출발지·목적지 IP는 NAT하지 않으면 그대로. 각 링크의 MAC은 새로 씌운다.

### 내부 의사결정 예시
PC-A `192.168.10.10`에서 PC-B `192.168.30.20`으로 Ping → PC-A default gateway R1(.1) → R1에서 `192.168.30.0/24 via 10.0.12.2` → R2의 `via 10.0.23.3` → R3 LAN30 → PC-B. Reply는 R3→R2→R1의 반대 경로가 있어야 한다.

## 3. 토폴로지
```text
PC-A -- SW-A -- G0/0 R1 G0/1 -- G0/0 R2 G0/1 -- G0/0 R3 G0/1 -- SW-B -- PC-B
LAN10              10.0.12.0/30      10.0.23.0/30              LAN30
```
1941 Router 3, 2960 Switch 2, PC 2, copper straight-through/Auto-Connect. R1/R2/R3에 Gi 포트 2개 지원 모델 필요; 실제 장치 포트 표기 점검.

| 장비 | 인터페이스 | IP/CIDR | Default Gateway |
|---|---|---|---|
| PC-A | Fa0 | 192.168.10.10/24 | 192.168.10.1 |
| R1 | G0/0 | 192.168.10.1/24 | — |
| R1 | G0/1 | 10.0.12.1/30 | — |
| R2 | G0/0 | 10.0.12.2/30 | — |
| R2 | G0/1 | 10.0.23.1/30 | — |
| R3 | G0/0 | 10.0.23.2/30 | — |
| R3 | G0/1 | 192.168.30.1/24 | — |
| PC-B | Fa0 | 192.168.30.20/24 | 192.168.30.1 |

## 4. 구축 — 한 장비씩 관측
1. 포트·링크 배선 및 PC IP/Mask/Gateway 설정.
2. 각 R의 인터페이스를 주소표대로 설정한다. 예시 R1:

```ios
enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 no shutdown
exit
interface gigabitEthernet0/1
 ip address 10.0.12.1 255.255.255.252
 no shutdown
end
show ip interface brief
show ip route
```
3. R2 G0/0=`10.0.12.2/30`, G0/1=`10.0.23.1/30`; R3 G0/0=`10.0.23.2/30`, G0/1=`192.168.30.1/24`. R2/R3에서도 각각 인터페이스 `no shutdown`, `show ip route` 검증. PC-A→PC-B Ping을 **정적 경로 없이 먼저** 시도하고 어디까지 도달하는지 관찰.
4. 다음 정적 경로를 **각 라우터에서** 추가:

R1:
```ios
configure terminal
ip route 192.168.30.0 255.255.255.0 10.0.12.2
end
```
R2:
```ios
configure terminal
ip route 192.168.10.0 255.255.255.0 10.0.12.1
ip route 192.168.30.0 255.255.255.0 10.0.23.2
end
```
R3:
```ios
configure terminal
ip route 192.168.10.0 255.255.255.0 10.0.23.1
end
```
5. 각 R의 `show ip route`에서 S 경로와 C 경로, next hop 확인. PC-A↔PC-B 양방향 Ping.

## 5. 검증·내부 동작 관측
- PC-A `ping 192.168.30.20`, PC-B `ping 192.168.10.10`. Ping이 성공해도 모든 홉을 검증했다는 뜻은 아니므로 Simulation ARP/ICMP에서 PC-A→R1→R2→R3→PC-B 관찰.
- R1/R2/R3: `show ip route`, `show arp`, `show ip interface brief`. 장비에서 `traceroute 192.168.30.20` 또는 PC `tracert` 사용 시 지원과 출력이 다를 수 있음.
- 각 홉의 MAC, IP, TTL 비교. 새 링크로 들어설 때 다음 홉 MAC을 ARP로 해결.

### 기본 경로/LPM 별도 실험
1. 원래 R1 특정 정적 경로를 **유지**한 채, R1에 기본 경로를 추가한다:
```ios
configure terminal
ip route 0.0.0.0 0.0.0.0 10.0.12.2
end
show ip route
```
2. `192.168.30.20`은 /24 특정 경로가 /0보다 우선, 그 외 알려지지 않은 목적지는 기본 경로 대상. **기본 경로가 생겼다고 그 목적지까지 반드시 성공한다는 것은 아니다** (나머지 라우터의 경로 필요).
3. 경로 비교 결과를 확인하고 기본 경로만 원상 복원:
```ios
configure terminal
no ip route 0.0.0.0 0.0.0.0 10.0.12.2
end
```

## 6. 장애 유도·복구
**필수 A — 반환 경로 누락:** 정상 구성 후 R3에서 `no ip route 192.168.10.0 255.255.255.0 10.0.23.1`. PC-A의 ICMP Echo Request가 PC-B에 도착하는지, PC-B Reply가 R3에서 어디서 폐기되는지 Simulation으로 확인. R3의 원래 route 복원 후 Ping 회복.

**필수 B — 잘못된 Next Hop:** 정상 구성 후 R1의 목적지 /24 static route를 제거하고 `ip route 192.168.30.0 255.255.255.0 10.0.12.99`를 추가해 본다. **.99는 R1에 직접 연결된 /30 이웃이 아니므로 IOS가 라우트 설치를 거부하거나 미설치할 수 있다.** `show ip route`로 실제 설치 여부를 확인하고, 반드시 임시 설정을 제거하고 `10.0.12.2`로 복원. 증상은 장비 구현에 따라 다르다.

진단: 링크 → connected routes → 원격 route 존재 → next-hop 유효성 → 역방향 route → 패킷.

## 7. 종료 주관식 2문항
1. 3대의 라우터가 모두 인터페이스 IP를 설정했는데도 양쪽 LAN 사이 Ping이 안 될 수 있는 이유를 설명해 봐.
2. 동일 목적지에 /24 경로와 /0 기본 경로가 모두 일치할 때 어떤 경로가 선택되며, 이것이 Ping 성공을 반드시 보장하지는 않는 이유는?

## 8. 핵심 3가지·후속
- 직접 연결 경로와 원격 정적 경로는 다르다.
- 왕복 경로가 존재해야 통신이 완료된다.
- 기본 경로는 모든 목적지로 통하는 마법의 통로가 아니라 마지막 후보 경로다.

후속: Lab 05 VLAN, 이후 OSPF·BGP, AWS VPC Route Table.

## 9. 실습 진행 기록
- [ ] 주소·토폴로지 구축 및 C 경로 확인
- [ ] 경로 추가 전 실패 관찰
- [ ] S 경로 추가 후 양방향 Ping
- [ ] 홉별 MAC·IP·TTL 관찰
- [ ] 기본 경로/LPM 비교
- [ ] 장애 A/B·복구
- [ ] 주관식 2문항
- 수행일 / 장비 버전 / 관찰 증거: **미실시**

## 10. 질문·학습 메모
| 실제 질문·오개념 | 교정된 이해 | 관찰된 근거 | 다음 복습 |
|---|---|---|---|
| 미실시 | — | — | — |

