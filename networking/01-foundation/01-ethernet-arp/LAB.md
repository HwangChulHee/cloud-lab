# LAB — 두 PC + L2 스위치 실습

## 토폴로지

PC-A (FastEthernet0) — Switch0 (2960) — PC-B (FastEthernet0)

## 주소 설계
| 장비 | 인터페이스 | IPv4 | Subnet Mask | Gateway |
|---|---|---|---|---|
| PC-A | FastEthernet0 | 192.168.10.10 | 255.255.255.0 | 비움 |
| PC-B | FastEthernet0 | 192.168.10.20 | 255.255.255.0 | 비움 |

## 구성 절차
1. Packet Tracer에서 PC 2개(PC-A/PC-B), 2960 스위치 1개를 배치.
2. Copper Straight-Through로 PC-A Fa0 → Switch0 Fa0/1, PC-B Fa0 → Switch0 Fa0/2 연결. 자동 연결도 가능.
3. PC마다 Desktop → IP Configuration에서 표의 IPv4와 마스크 입력.
4. 링크가 활성화됐는지 확인. 초기에는 STP 등의 초기화로 시간이 걸릴 수 있음.

## 통신 검증
1. PC-A Desktop → Command Prompt에서 **ping 192.168.10.20** 실행.
2. 요청과 응답이 성공하는지 확인. 최초 패킷이 실패하면 다시 반복해 상태를 비교.
3. PC-A에서 **arp -a**로 캐시를 확인(지원되는 PT 버전에 따라 출력 형식 차이).
4. Switch0 CLI에서 아래를 실행:

```text
enable
show mac address-table
show interfaces status
```

5. 어느 포트에 어떤 MAC이 학습되었는지 확인. 실제 MAC 값은 기기에서 읽고 기록.

## 프레임 흐름 분석
1. Simulation Mode로 전환하고 ARP와 ICMP 이벤트만 필터링.
2. 필요하면 캐시를 지우거나 새 파일에서 다시 시작하여 최초 ARP 교환을 관찰.
3. PC-A에서 PC-B로 ping을 다시 실행.
4. ARP Request의 목적지 MAC과 ARP Reply의 발신자 IP/MAC을 확인.
5. ICMP Echo Request에서 IP 목적지는 B의 IP이고 Ethernet 목적지는 B의 MAC인지 확인.
6. 스위치에서 MAC 테이블 학습 전후의 전달 차이를 서술.

## 응용
- PC-B를 다른 /24로 변경하되 게이트웨이는 비워두기. 통신 실패를 예상하고 확인.
- 다시 원래 주소로 돌린 뒤 ping 재검증.

## 실습 결과 기록란
- 수행일:
- Packet Tracer 버전:
- PC-A/PC-B 실제 MAC:
- 최초 ping 결과:
- 이후 ping 결과:
- switch MAC 테이블 관측:
- ARP Request/Reply 관측:
- 직접 검증 여부: [ ]
