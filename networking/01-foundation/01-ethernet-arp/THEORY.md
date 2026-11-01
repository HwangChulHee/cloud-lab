# THEORY — Ethernet, MAC Learning, ARP, ICMP

## 왜 필요한가?

같은 LAN에서 IP 주소만 안다고 바로 프레임을 전송할 수는 없다. IP 목적지에 전달할 **다음 홉의 링크 계층 주소(MAC)** 를 알아내야 하고, 스위치는 학습한 MAC 주소와 포트를 이용해 프레임을 전달한다.

## 핵심 개념

- **MAC 주소**: 이더넷에서 프레임 송수신에 사용되는 링크 계층 주소.
- **IP 주소**: 네트워크 계층의 논리 주소. 같은 서브넷인지 판단할 때 서브넷 마스크를 사용.
- **ARP**: 동일한 IPv4 브로드캐스트 도메인에서 특정 IPv4 주소에 대응하는 MAC 주소를 알아내는 프로토콜.
- **스위치 MAC 주소 테이블**: 들어오는 프레임의 *출발지 MAC*과 수신 포트를 학습하여, 이미 아는 목적지 MAC이면 해당 포트로 전달.
- **ICMP Echo**: ping이 송신·응답을 확인할 때 쓰는 메시지. TCP/UDP 포트가 있는 프로토콜이 아님.

## 예시

PC-A: 192.168.10.10/24, MAC AA-AA-AA-AA-AA-AA  
PC-B: 192.168.10.20/24, MAC BB-BB-BB-BB-BB-BB (MAC은 설명용 가상값)

1. A가 B가 같은 서브넷에 있는지 판단한다.
2. A의 ARP 캐시에 B 항목이 없으면 브로드캐스트 ARP Request를 보낸다. 목적지 Ethernet MAC은 FF:FF:FF:FF:FF:FF.
3. 스위치는 요청 프레임의 출발지 MAC A를 수신 포트에 매핑하고 브로드캐스트를 다른 포트로 전달한다.
4. B가 자신의 IP에 대한 ARP Request를 받으면 MAC B를 담아 ARP Reply를 보낸다(일반적으로 유니캐스트).
5. A가 B의 MAC을 학습하고 ICMP Echo Request를 Ethernet 목적지 MAC B로 보낸다.
6. 스위치가 B의 MAC과 포트를 알고 있다면 해당 포트로 전달한다. Echo Reply는 반대 경로로 돌아온다.

> 주의: ARP 요청과 응답, MAC 학습의 구체적 순서는 캐시 상태 및 장비의 학습 상태에 따라 일부 달라진다. 첫 ping이 ARP 때문에 실패하거나 지연될 수도 있다.

## 자주 헷갈리는 점

- **스위치가 ARP를 대신 수행하는 것 아님**: 여기서는 PC가 ARP 요청하고 스위치가 프레임을 전달한다.
- **MAC 주소가 IP를 대체하지 않음**: 목적지 네트워크가 다르면 기본 게이트웨이 MAC을 대상으로 프레임을 보낸다(다음 Lab에서 확장).
- **ARP는 IPv4에서 쓰는 방식**: IPv6에서는 주로 Neighbor Discovery를 사용한다.

## 이해 확인 질문
1. A가 B의 IP는 알아도 MAC을 모를 때 어떤 프레임을 보내는가?
2. 스위치가 주소를 학습할 때 출발지 MAC과 목적지 MAC 중 무엇을 보는가?
3. B가 다른 서브넷에 있다면 A가 ARP로 알아내려는 MAC은 무엇인가?

## 심화 연결
VLAN 브로드캐스트 도메인, Inter-VLAN Routing, ARP Spoofing/DAI, IPv6 ND.

## 레퍼런스
- RFC 826 (ARP): https://www.rfc-editor.org/rfc/rfc826
- RFC 792 (ICMP): https://www.rfc-editor.org/rfc/rfc792
