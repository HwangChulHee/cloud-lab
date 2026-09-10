# 65. VPN / Direct Connect

이 챕터는 현재 core examples에서 직접 구축하지 않는다. SAA에서 온프레미스와 AWS를 연결하는 선택 기준을 이해하는 것이 목적이다.

## 1. Site-to-Site VPN

인터넷 위에 암호화된 터널을 만들어 온프레미스와 VPC를 연결한다.

```text
On-premises
   ↓
Customer Gateway
   ⇄ IPsec VPN
Virtual Private Gateway / Transit Gateway
   ↓
VPC
```

빠르게 구성할 수 있지만 인터넷 품질의 영향을 받는다.

## 2. Direct Connect

온프레미스와 AWS 사이에 전용 네트워크 연결을 구성한다.

특징:

- 보다 일관된 네트워크 성능이 필요한 경우 고려
- 구축 리드타임이 길 수 있음
- 기본적으로 전용 연결 자체가 암호화를 의미하지는 않음
- 필요하면 VPN과 조합해 암호화를 추가할 수 있음

## 3. 선택 기준

```text
빠르게 사설 연결 필요
→ Site-to-Site VPN

장기적 / 일관된 네트워크 성능 / 대규모 데이터 전송
→ Direct Connect

Direct Connect 장애 대비
→ 별도 DX 또는 Site-to-Site VPN 백업 고려
```

## 4. Transit Gateway와 연결

여러 VPC와 온프레미스 네트워크가 함께 연결될 경우 Transit Gateway가 중앙 허브 역할을 할 수 있다.

## 5. Recall Check

- Site-to-Site VPN과 Direct Connect의 가장 큰 차이는?
- Direct Connect가 자동으로 암호화된 연결을 의미하는가?
- Direct Connect 장애에 대비하는 방법은?
- 여러 VPC와 온프레미스를 함께 연결할 때 어떤 허브 서비스를 고려하는가?

## 6. 완료 기준

- [ ] VPN / Direct Connect 선택 기준을 설명할 수 있다.
- [ ] Direct Connect와 암호화를 별개로 이해한다.
- [ ] 하이브리드 네트워크의 고가용성 기본 아이디어를 설명할 수 있다.
