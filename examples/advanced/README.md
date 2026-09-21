# AWS Optional / Advanced Examples

이 디렉터리는 `examples/01~16`의 필수 Guided 흐름을 깨지 않고, 특정 AWS 기능을 더 깊게 확인하기 위한 **선택 심화 실습**을 모은다.

핵심 과정의 목적은 그대로 유지한다.

```text
examples/01~16
→ 핵심 웹 인프라 반복 구축 / 관측 / 장애 / 복구
→ portfolio/
```

Advanced Example은 필요한 주제를 골라 수행한다. 번호는 핵심 과정과 별도로 `A01`, `A02`처럼 관리한다.

## 현재 실습

| # | Example | 핵심 질문 | 권장 시점 |
|---|---|---|---|
| A01 | [PrivateLink Service Access](./01-privatelink-service-access/README.md) | VPC 전체를 연결하지 않고 특정 서비스만 private하게 노출하려면? | Part 12의 VPC Endpoint/PrivateLink 학습 후, 또는 Example 06 이후 |

## 공통 원칙

- Console 중심으로 구축하고 CLI로 상태를 검증한다.
- Terraform/IaC는 억지로 추가하지 않는다.
- 핵심 개념을 보여주는 최소 구성만 사용한다.
- 비용이 발생하는 NLB, Interface Endpoint 같은 리소스는 실습 직후 정리한다.
- `Project=cloud-lab`, `Stage=examples-advanced`, `Example=A01` 형식으로 가능한 리소스에 태그한다.
- 삭제 후 [Advanced CLI Verification](./CLI_VERIFICATION.md)으로 잔존 리소스를 확인한다.


## CLI 원칙

Advanced Example도 중앙 CLI 문서만 보고 실행하지 않는다. 각 실습 README 하단의 **로컬 CLI 검증 가이드**에서 명령과 출력 필드의 의미를 함께 학습한다.

`examples/advanced/CLI_VERIFICATION.md`는 여러 Advanced 실습을 한 번에 비교하거나 삭제 후 잔존 리소스를 통합 점검하는 참고 문서로 유지한다.
