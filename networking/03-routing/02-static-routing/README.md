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
### 2-1. 왜 Lab 03은 됐는데 Lab 04에서는 안 될까?
Lab 03의 R1은 왼쪽 LAN과 오른쪽 LAN에 **직접 연결**되어 있었다. 그래서 인터페이스의 IP와 마스크를 설정하고 `up/up`으로 만들면 경로가 자동 생성됐다.

이번에는 라우터 3대가 일렬로 연결된다. R1은 자기 오른쪽에 **R2가 있다**는 것은 알아도, R2 뒤의 R3와 PC-B 네트워크를 처음부터 알지는 못한다. **라우터는 연결된 포트만 보고 인터넷의 모든 네트워크를 알아내지 않는다.**

### 2-2. 꼭 알아야 할 용어를 쉬운 말로
| 용어 | 쉬운 뜻 | 이 Lab의 예 |
|---|---|---|
| 목적지 네트워크 / Prefix | 여러 IP를 묶은 주소 범위 | `192.168.30.0/24` |
| Routing Table | 목적지별로 어디에 넘길지 적은 표 | R1의 `show ip route` |
| C (Connected) | 라우터 포트에 직접 붙어 있는 네트워크 | R1의 `10.0.12.0/30` |
| L (Local) | 라우터 자신의 인터페이스 IP, 보통 /32 | R1의 `10.0.12.1/32` |
| S (Static) | 관리자가 직접 입력한 경로 | `192.168.30.0/24 via 10.0.12.2` |
| Next Hop | **다음 라우터**의 IP. 최종 목적지 IP와 다를 수 있음 | R1에서 R2의 `10.0.12.2` |
| Exit Interface | 패킷이 나갈 포트 | R1 `G0/1` |
| Default Route | 특별히 일치하는 경로가 없을 때 사용하는 마지막 후보 | `0.0.0.0/0` |
| LPM (Longest Prefix Match) | 목적지와 일치하는 경로 중 가장 구체적인 주소 범위를 선택 | /24가 /0보다 우선 |

### 2-3. 라우팅 테이블은 어떻게 만들어질까?
1. **자동(Connected/Local)**: 인터페이스 IP 설정 + 링크 `up/up` → C와 L 경로가 생성된다.
2. **수동(Static)**: 관리자가 `ip route 네트워크주소 서브넷마스크 다음홉`을 입력한다. 이 명령은 다음 홉까지 실제로 왕복 통신이 되는 것까지 보장하지 않는다.
3. **동적 라우팅**: OSPF 등으로 라우터들이 경로를 교환한다. 이 Lab에서는 사용하지 않는다.

명령을 한 단어씩 해석해 보자.

```ios
ip route 192.168.30.0 255.255.255.0 10.0.12.2
```
- `ip route`: IPv4 정적 경로를 설정하겠다.
- `192.168.30.0 255.255.255.0`: 목적지 **192.168.30.0/24 네트워크 전체**에 대해.
- `10.0.12.2`: 패킷을 **다음 라우터 R2**에게 넘기겠다. PC-B의 IP나 MAC이 아니다.

### 2-4. 라우팅 판단과 ARP는 별개의 단계
PC-A `192.168.10.10` → PC-B `192.168.30.20`의 흐름:
1. PC-A는 PC-B가 다른 네트워크라 판단 → 자신의 게이트웨이 R1(`192.168.10.1`) MAC이 필요하다.
2. R1은 목적지 IP `192.168.30.20`으로 **라우팅 테이블을 조회** → R2(`10.0.12.2`)를 Next Hop으로 결정한다.
3. R1은 R2의 MAC을 모르면 **R1의 G0/1 링크에서 `10.0.12.2`에 대해 ARP**한다. PC-B `192.168.30.20`에 대해 ARP하는 게 아니다.
4. R2의 MAC을 알면 새 Ethernet 프레임(`R1 G0/1 MAC → R2 G0/0 MAC`)을 만든다. IP 출발지/목적지(`192.168.10.10 → 192.168.30.20`)는 그대로이며 TTL을 1 줄인다.
5. R2도 다시 자기 라우팅 테이블을 조회한 뒤, 필요하면 `10.0.23.2`의 MAC을 ARP로 해결한다.

**혼동 주의:** 호스트의 ARP 테이블(IP→MAC)과 스위치의 MAC 테이블(MAC→포트)은 다르다. 스위치가 R2의 MAC을 알고 있어도 R1의 ARP 캐시가 비어 있으면 R1은 ARP를 해야 할 수 있다. ARP 브로드캐스트는 해당 링크의 L2 브로드캐스트 도메인에 한정된다.

### 2-5. 패킷은 왕복해야 한다
Ping은 Echo Request(요청)와 Echo Reply(응답) 두 패킷 흐름이 필요하다. R1→R2→R3→PC-B가 잘 되더라도, **R3가 192.168.10.0/24로 돌아가는 경로를 모르면 Reply가 중간에 폐기**될 수 있다. 정적 경로는 한쪽만 설정한다고 다른 쪽이 자동으로 생기지 않는다.

### 2-6. 기본 경로와 Longest Prefix Match
R1의 테이블에 아래 두 개가 있다고 가정:
- `192.168.30.0/24 → 10.0.12.2`
- `0.0.0.0/0 → 10.0.12.2`

`192.168.30.20`은 두 범위에 모두 속하지만 **/24가 더 구체적**이므로 /24 경로가 선택된다. /0은 다른 항목이 일치하지 않을 때 선택된다.

경로가 여럿 있을 때 먼저 **목적지에 일치하는 prefix 중 최장 길이**를 고른다. 같은 prefix에 여러 출처/후보가 있는 경우의 AD·Metric은 별도 단계에서 다룬다. `show ip route`에 경로가 보이는 것과 최종 목적지에서 응답이 오는 것은 다르다.

### 개념 점검 (구축 전에 한 문제씩)
- 왜 R1은 자기 포트를 설정하기만 해서는 PC-B LAN을 알 수 없을까?
- R1이 다음 홉 `10.0.12.2`로 보내려면 ARP Target IP는 무엇일까?
- 요청이 도착했는데 Ping이 타임아웃이라면 어느 방향의 경로를 의심해야 할까?

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
> **대화형 진행 규칙:** 아래는 전체 참고 절차다. 실제 학습에서는 한 번에 명령을 전부 실행시키지 않는다. **장비 1대 구성 → `show` 출력 확인 → 실패 지점 예상 → 다음 명령** 순서로 진행한다. 사용자가 직접 확인하기 전에는 완료 체크 금지.

### 4-1. 배선·IP: 먼저 직접 연결만 구축
1. PC-A, PC-B, 2960 2대, 1941 라우터 3대를 토폴로지대로 배치한다. 링크는 Packet Tracer의 Auto-Connect 사용 가능. 실제 장비 포트 표기를 확인한다.
2. PC-A: `192.168.10.10 / 255.255.255.0 / GW 192.168.10.1`, PC-B: `192.168.30.20 / 255.255.255.0 / GW 192.168.30.1`.
3. 각 라우터에 **인터페이스 IP만 설정**한다. 이 단계에서는 `ip route` 명령을 사용하지 않는다.

**R1**
```ios
enable
configure terminal
hostname R1
interface gigabitEthernet0/0
 description TO_PC_A_LAN
 ip address 192.168.10.1 255.255.255.0
 no shutdown
exit
interface gigabitEthernet0/1
 description TO_R2
 ip address 10.0.12.1 255.255.255.252
 no shutdown
end
show ip interface brief
show ip route
```

**R2**
```ios
enable
configure terminal
hostname R2
interface gigabitEthernet0/0
 description TO_R1
 ip address 10.0.12.2 255.255.255.252
 no shutdown
exit
interface gigabitEthernet0/1
 description TO_R3
 ip address 10.0.23.1 255.255.255.252
 no shutdown
end
show ip interface brief
show ip route
```

**R3**
```ios
enable
configure terminal
hostname R3
interface gigabitEthernet0/0
 description TO_R2
 ip address 10.0.23.2 255.255.255.252
 no shutdown
exit
interface gigabitEthernet0/1
 description TO_PC_B_LAN
 ip address 192.168.30.1 255.255.255.0
 no shutdown
end
show ip interface brief
show ip route
```

4. 세 라우터의 경로 테이블에서 **C와 L만** 확인한다. `up/up`이 아니면 케이블·포트·`no shutdown`을 점검한다.
5. PC-A→자기 게이트웨이, PC-B→자기 게이트웨이 Ping을 각각 확인한다. PC-A→PC-B Ping은 아직 실패할 것으로 예상. 이때 **어느 라우터에서 경로가 없는지** `show ip route`로 먼저 판단한다.

### 4-2. 정적 경로를 '한 개씩' 추가하기
**각 체크포인트의 예상 결과를 먼저 말해 보고, 실제 Simulation/CLI로 확인한 뒤 다음 단계로 넘어간다.**

**체크포인트 A — R1에만 목적지 경로 추가**
```ios
R1# configure terminal
R1(config)# ip route 192.168.30.0 255.255.255.0 10.0.12.2
R1(config)# end
R1# show ip route
```
- 기대: `S 192.168.30.0/24 via 10.0.12.2`가 보이고 PC-A의 Echo Request는 **R2까지** 도달 가능. 하지만 R2는 아직 `192.168.30.0/24`를 모르므로 원격 LAN으로 계속 포워딩하지 못한다.
- 관찰: R1이 R2의 MAC을 알아내려고 `10.0.12.2`로 ARP하는지 확인. **스위치 MAC 학습과 라우터 ARP 캐시를 구분한다.**

**체크포인트 B — R2에 목적지 방향 경로 추가**
```ios
R2# configure terminal
R2(config)# ip route 192.168.30.0 255.255.255.0 10.0.23.2
R2(config)# end
R2# show ip route
```
- 기대: Echo Request가 **PC-B에 도달**할 수 있다. 그러나 PC-B의 Echo Reply는 R3에서 `192.168.10.0/24`의 반환 경로가 없어서 성공하지 못한다.
- PC-A의 Ping 타임아웃만 보지 말고, **PC-B가 Echo Request를 받는지** Simulation으로 분리 관찰한다.

**체크포인트 C — R3에 반환 경로 추가**
```ios
R3# configure terminal
R3(config)# ip route 192.168.10.0 255.255.255.0 10.0.23.1
R3(config)# end
```
- R3가 Echo Reply를 R2로 넘겨도 R2는 아직 LAN10 경로를 모른다. **반환 패킷이 R2에서 멈추는지** 확인.

**체크포인트 D — R2에 마지막 반환 경로 추가**
```ios
R2# configure terminal
R2(config)# ip route 192.168.10.0 255.255.255.0 10.0.12.1
R2(config)# end
```
- 이제 Request와 Reply가 모두 라우팅 가능. PC-A↔PC-B Ping 양방향 성공을 확인한다.
- 각 단계에서 `show ip route`의 변화와 실제 포워딩 결과를 나란히 기록한다.

### 4-3. 상태 저장
- 모든 라우터: `show ip route`, `show ip interface brief`, `show arp` 확인.
- 정상 완료 후 필요하면 `copy running-config startup-config`으로 저장 (Packet Tracer 프로젝트 파일도 별도 저장).

## 5. 검증·내부 동작 관측
### 5-1. 홉마다 무엇이 바뀌는지 비교
- PC-A `ping 192.168.30.20`, PC-B `ping 192.168.10.10`. 처음 몇 패킷은 ARP 처리로 지연될 수 있다.
- Simulation에 ARP·ICMP 필터를 설정한다. PC-A→R1→R2→R3→PC-B의 **한 Echo Request**를 추적한다. 장비 모델에 따라 ARP/ICMP 상세 화면은 다를 수 있다.
- R1, R2, R3의 `Inbound PDU Details` / `Outbound PDU Details`에서 출발지 MAC·목적지 MAC, IP 출발지·목적지, TTL을 비교한다.
- 예상: **IP 출발지/목적지는 유지, Ethernet MAC은 라우터 출력 링크마다 새로 구성, TTL은 라우터 3곳에서 각각 1씩 감소**. 스위치 통과에서는 일반적으로 MAC/TTL이 그대로다.
- 라우터의 `show arp`는 **IP → MAC**, 스위치의 `show mac address-table`은 **MAC → 포트**를 보여준다. ARP는 매 패킷마다 발생하지 않고 캐시가 유효하면 재사용한다.

### 5-2. 기본 경로를 쉬운 예로 확인
**기본 경로 `0.0.0.0/0`(라우터의 목적지 경로)은 PC의 '게이트웨이 설정을 `0.0.0.0`으로 비우는 것'과 완전히 다르다.** Lab 03에서 Packet Tracer PC가 `0.0.0.0`에 대해 ARP를 생성한 관찰을 이 라우터 설정으로 일반화하지 않는다.

1. 모든 정상 정적 경로를 유지하고 R1에 **기본 경로를 추가**한다.
```ios
configure terminal
ip route 0.0.0.0 0.0.0.0 10.0.12.2
end
show ip route
```
2. R1의 `192.168.30.0/24`와 `0.0.0.0/0`를 비교한다. `192.168.30.20`에 일치하는 더 긴 prefix는 /24다. 경로 조회 명령을 지원하는 경우 `show ip route 192.168.30.20`도 확인한다.
3. **검증 가능한 보조 사례:** R1에서 `show ip route 203.0.113.10`으로 매칭 경로를 조회해 보거나(장비 지원 여부 확인), PC-A에서 `ping 203.0.113.10`을 시도한다. R1은 다른 특정 경로가 없으면 기본 경로를 선택하지만, **R2 이후 경로가 없어 Ping은 실패할 수 있다**. 사용자가 출력/Simulation을 확인할 때만 확정한다.
4. **선택 심화:** R1에 `192.168.30.0/25 via 10.0.12.2`를 추가하고 `.20`과 `.200` 목적지에 각각 매칭하는 최장 prefix를 비교한다. /25 경로는 .0~.127에만 일치한다. 같은 next hop이면 전송 결과만으로 선택 차이를 증명할 수 없으므로 **경로 조회 출력 중심**으로 확인한다. 실제 `.200` 호스트는 만들지 않아도 경로 선택 규칙은 설명할 수 있다.
5. 반드시 선택 /25와 기본 경로를 제거하여 원상 복원한다:
```ios
configure terminal
no ip route 192.168.30.0 255.255.255.128 10.0.12.2
no ip route 0.0.0.0 0.0.0.0 10.0.12.2
end
```
선택 /25를 추가하지 않았다면 해당 `no ip route` 줄은 생략한다. 정상 경로와 Ping을 재확인한다.

## 6. 장애 유도·복구
> 정상 구성과 양방향 Ping을 먼저 확인하고, **매 장애마다 증상 → 예상 실패 지점 → `show` 및 Simulation 증거 → 수정 → 재검증** 순서로 진행한다. 이전 장애는 반드시 복구한 후 다음 장애를 시작한다.

### 필수 A — 반환 경로 누락
R3에서 PC-A LAN으로의 정적 경로만 삭제한다.
```ios
configure terminal
no ip route 192.168.10.0 255.255.255.0 10.0.23.1
end
show ip route
```
- PC-A→PC-B Ping은 타임아웃 예상. **Echo Request가 PC-B에 도달한 것**과 **Echo Reply가 R3에서 멈춘 것**을 따로 관찰한다.
- R3에서 `192.168.10.0/24`로 가는 경로가 없음을 확인한다.
- 복구:
```ios
configure terminal
ip route 192.168.10.0 255.255.255.0 10.0.23.1
end
```
- Ping 복구 확인.

### 필수 B — 잘못된 목적지 Prefix
R1의 올바른 `192.168.30.0/24` 경로를 제거하고, 오타가 난 `192.168.31.0/24`를 입력한다. **이전에 추가한 기본 경로는 반드시 제거한 정상 상태에서 시작**한다.
```ios
configure terminal
no ip route 192.168.30.0 255.255.255.0 10.0.12.2
ip route 192.168.31.0 255.255.255.0 10.0.12.2
end
show ip route
```
- `S` 경로가 보이더라도 `192.168.30.20`과는 일치하지 않는다. PC-A→PC-B 요청이 R1에서 더 이상 포워딩되지 않는지 확인한다. **'정적 경로가 존재한다'와 '그 목적지에 매칭된다'는 다르다.**
- 복구:
```ios
configure terminal
no ip route 192.168.31.0 255.255.255.0 10.0.12.2
ip route 192.168.30.0 255.255.255.0 10.0.12.2
end
```
- R1 `show ip route` 및 양방향 Ping 재검증.

### 선택 C — 잘못된 Next Hop
`10.0.12.99`와 같이 직접 연결되지 않은 주소를 Next Hop으로 설정해 보고, 장비의 재귀적 경로 조회/경로 설치 결과를 `show ip route`와 실제 출력으로 검증한다. **IOS/Packet Tracer가 거부·미설치·다른 경로 이용 중 무엇을 보일지는 미리 단정하지 않는다.** 초급 필수 실습에서는 제외한다.

진단 순서: 물리 링크 → `show ip interface brief` → Connected 경로 → 목적지 prefix 매칭 → next hop → ARP → 요청/응답 양쪽 경로.

## 7. 종료 주관식 2문항
> 정답을 미리 공개하지 않는다. **한 번에 한 문제**, 학습자의 서술 답변을 받고 필요한 부분만 피드백한다.

1. R1→R2→R3→PC-B 구성에서 **R1의 C 경로만 있을 때** PC-A→PC-B Ping이 왜 실패하는지 설명하고, R1에 `192.168.30.0/24 via 10.0.12.2`를 추가하면 무슨 일이 달라지는지 말해 봐. 이때 R1이 ARP로 찾을 IP는 무엇일까?
2. 모든 라우터의 경로를 구성한 다음 **R3의 반환 정적 경로만 삭제**했다. PC-A의 Request가 PC-B에 도착하는데 Ping이 실패하는 이유를 패킷 경로로 설명하고, `show ip route`에서 무엇을 확인할지 말해 봐.

(선택 확인) /24 정적 경로와 /0 기본 경로가 동시에 일치할 때 어떤 경로가 선택될까?

## 8. 핵심 3가지·후속
- 직접 연결 경로와 원격 정적 경로는 다르다.
- 왕복 경로가 존재해야 통신이 완료된다.
- 기본 경로는 모든 목적지로 통하는 마법의 통로가 아니라 마지막 후보 경로다.

후속: Lab 05 VLAN, 이후 OSPF·BGP, AWS VPC Route Table.

## 9. 실습 진행 기록
- [ ] 주소·토폴로지 구축 및 C 경로 확인
- [ ] 경로 추가 전 실패 관찰
- [ ] R1 경로만 추가 후 R2에서 멈추는 현상 확인
- [ ] R2 목적지 경로 추가 후 PC-B Request 도착·Reply 실패 관찰
- [ ] R3 반환 경로 추가 후 R2에서 멈추는 현상 확인
- [ ] R2 반환 경로 추가 후 양방향 Ping
- [ ] 홉별 MAC·IP·TTL 및 ARP Next Hop 관찰
- [ ] 기본 경로/LPM 비교 및 설정 복원
- [ ] 장애 A/B·복구
- [ ] 주관식 2문항
- 수행일 / 장비 버전 / 관찰 증거: **미실시**

## 10. 질문·학습 메모
| 실제 질문·오개념 | 교정된 이해 | 관찰된 근거 | 다음 복습 |
|---|---|---|---|
| 미실시 | — | — | — |

