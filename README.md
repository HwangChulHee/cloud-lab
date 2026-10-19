# cloud-lab

클라우드·인프라 기술을 개념부터 직접 구축, 검증, 장애 진단, 복구까지 학습하는 저장소입니다.

AWS SAA-C03은 **2026-10-19 합격 완료**했습니다. 기존 강의별 학습 기록과 체크 상태는 보존하며, 이후에는 실습 및 기술면접 역량 강화에 집중합니다.

## 학습 영역

| 영역 | 내용 |
| --- | --- |
| [AWS](./aws/README.md) | [SAA 학습 기록](./aws/saa/README.md) · [AWS Labs](./aws/labs/README.md) |
| [Kubernetes](./k8s/README.md) | 기초, CKA 예습, 독립 실습, 장애 진단 |
| [Technical Interview](./interview/README.md) | Linux, Networking, AWS, Docker, K8s, Terraform, CI/CD, Monitoring, Troubleshooting |

## 학습 흐름

```text
개념 이해 → 직접 구축 → 결과 관측 → 장애 재현 → 원인 분석 → 복구 → 설명하기
```

각 기술의 커리큘럼과 완료 체크는 해당 디렉터리에서 관리합니다. 애플리케이션 포트폴리오와 Spring 학습 프로젝트는 이 저장소에 포함하지 않고 별도 저장소에서 진행합니다.

## 저장소 구조

```text
aws/
  saa/      SAA 강의 이론 / 선택 기준 / 완료 기록 (part00~14)
  labs/     AWS 01~16 기본 실습 + advanced 실습
k8s/        Kubernetes 기초 + CKA + 독립 실습
interview/  클라우드 / DevOps 기술면접 대비
```
