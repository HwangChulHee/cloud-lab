# 63. VPC Peering / Transit Gateway

이 챕터는 현재 core examples의 직접 실습 대상은 아니지만, 네트워크 구조를 확장할 때 필요한 SAA 핵심 선택 기준을 정리한다.

## 1. VPC Peering

두 VPC를 사설 네트워크로 직접 연결한다.

```text
VPC-A ← Peering → VPC-B
```

핵심:

- 서로 겹치지 않는 CIDR이 필요하다.
- route table에 상대 VPC CIDR을 peering connection으로 보내는 route가 필요하다.
- transitive routing을 제공하지 않는다.

예:

```text
A ↔ B
B ↔ C
```

라고 해서 A가 자동으로 C에 통신할 수 있는 것은 아니다.

## 2. Transit Gateway

많은 VPC와 온프레미스 연결을 허브-앤-스포크 형태로 묶을 때 사용한다.

```text
        VPC-A
          |
VPC-B — TGW — VPC-C
          |
      On-premises
```

여러 개의 개별 peering을 복잡하게 관리하는 대신 중앙 연결 허브 역할을 한다.

## 3. 선택 기준

```text
VPC 두 개를 단순 연결
→ VPC Peering

많은 VPC / 여러 계정 / VPN / Direct Connect를 중앙 연결
→ Transit Gateway
```

## 4. 실습과의 연결

현재 `examples/01~16`에서는 직접 구축하지 않는다. 다만 59~62에서 배운 CIDR과 route table 개념이 그대로 확장된다.

## 5. Recall Check

- VPC Peering이 transitive하지 않다는 의미는?
- Peering을 만들고도 route table 변경이 필요한 이유는?
- 수십 개 VPC를 연결할 때 Transit Gateway가 유리한 이유는?
- CIDR overlap이 왜 네트워크 연결 설계를 어렵게 하는가?

## 6. 완료 기준

- [ ] VPC Peering과 Transit Gateway의 선택 기준을 설명할 수 있다.
- [ ] Peering에 route table 설정이 필요한 이유를 이해한다.
- [ ] transitive routing 개념을 설명할 수 있다.
