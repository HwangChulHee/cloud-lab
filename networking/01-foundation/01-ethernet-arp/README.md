# Lab 01 — 두 PC 간 Ethernet 통신과 ARP

- **수준:** CCNA 기초 (Pass A)
- **도구:** Cisco Packet Tracer
- **선수 지식:** 이더넷의 역할, IPv4 주소/서브넷의 기초 (이 Lab에서 간략히 복습)
- **목표:** 같은 서브넷의 PC 두 대가 스위치를 통해 통신할 때 MAC 학습·ARP·ICMP의 관계를 관찰한다.
- **상태:** 문서 작성 완료 / 실습 직접 검증 미완료 / .pkt 미첨부

## 읽고 실습할 순서
1. [THEORY.md](./THEORY.md): 이더넷 프레임, MAC, ARP, MAC 테이블, Ping
2. [LAB.md](./LAB.md): 두 PC와 스위치 구성 및 Simulation Mode 분석
3. [TROUBLESHOOTING.md](./TROUBLESHOOTING.md): 잘못된 IP/서브넷 설정을 진단

## 완료 체크
- [ ] 핵심 이론 질문을 말로 설명
- [ ] PC-A → PC-B Ping 성공
- [ ] ARP 요청/응답과 MAC 학습 관측
- [ ] 잘못된 설정을 만들고 복구
- [ ] 관측한 결과를 README에 기록

**다음 연결:** 서브넷/기본 게이트웨이 → VLAN → 인터 VLAN 라우팅으로 확장.
