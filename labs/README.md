# AWS Scenario Labs

SAA 객관식 문제풀이와 별개로, **상황을 보고 직접 아키텍처를 설계하고 구축하는 연습**을 한다.

이 단계는 `examples/`의 Guided Example을 따라 구축하며 기본 구조와 콘솔 사용에 익숙해진 뒤 진행한다.

> 먼저 따라 만들어보고 싶다면 [AWS Guided Examples](../examples/README.md)부터 진행한다.

정답 아키텍처를 먼저 보지 않는다.

> 상황 이해 → 요구사항 분해 → 설계 → 구축 → 검증 → 장애 실험 → 회고

## 진행 방식

각 Lab은 다음 순서로 진행한다.

1. `README.md`의 상황과 요구사항만 읽는다.
2. `architecture.md`에 먼저 자신의 설계를 작성한다.
3. AWS Console 또는 IaC로 직접 구축한다.
4. 검증 항목을 수행한다.
5. 실패/장애 상황을 일부러 만들어본다.
6. `postmortem.md`에 결과와 개선점을 정리한다.

처음에는 Console 중심으로 진행하고, SAA 취득 후 Terraform으로 다시 구현해도 된다.

## 규칙

- AWS 서비스를 많이 쓰는 것이 목표가 아니다.
- 요구사항을 만족하는 **가장 단순한 구조**부터 생각한다.
- 서비스 선택에는 항상 이유를 적는다.
- 가용성, 비용, 보안, 운영 복잡도의 trade-off를 기록한다.
- 구축 후 반드시 실제 요청/장애 테스트로 검증한다.
- 리소스 삭제 및 비용 확인까지 Lab의 일부로 본다.

## Labs

- [ ] [01. 웹 서버 1대가 죽어도 살아있는 서비스](./01-high-availability-web/README.md)
- [ ] 02. 트래픽 폭증에 자동 대응하는 서비스
- [ ] 03. DB 읽기 부하가 급증한 서비스
- [ ] 04. Public / Private 계층 분리와 보안
- [ ] 05. 외부 업체의 고정 IP Whitelist 요구 대응
- [ ] 06. Availability Zone 장애 대응
- [ ] 07. 다중 서버 환경의 로그인 세션 문제
- [ ] 08. 비용 최적화 시나리오
- [ ] 09. 비동기 주문 처리와 장애 격리
- [ ] 10. 최종 Architecture Challenge

## 공통 산출물

```text
labs/<lab-name>/
├── README.md          # 문제 및 요구사항
├── architecture.md    # 내가 설계한 구조와 선택 근거
└── postmortem.md      # 구축/장애 실험 결과와 회고
```

Terraform을 사용하는 단계에서는 각 Lab에 `terraform/`을 추가한다.
