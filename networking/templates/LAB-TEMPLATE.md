# 단일 README Lab 템플릿

> 각 독립 Lab은 원칙적으로 **README.md 하나**로 구성한다. 이론·설정·검증·장애 분석을 별개 Markdown 파일로 분리하지 않는다. 바이너리 실습 파일(.pkt), 캡처 파일(.pcap), 실제 설정 스크립트는 필요할 때만 추가한다.

```yaml
---
id: NET-SW-004
title: VLAN and Trunk
level: CCNA
pass: A
prerequisites:
  - NET-FD-001
tools:
  - Cisco Packet Tracer
document_status: planned
lab_status: not-tested
---
```

## README.md의 표준 순서

1. **Overview / 학습 목표**: 왜 하는지, 무엇을 확인할지, 도구 및 선수 개념.
2. **실습 전 핵심 개념**: 필요성, 용어, L2/L3 내부 처리, 실제 주소가 포함된 패킷 흐름, 자주 헷갈리는 점, 개념 점검 질문.
3. **Topology & Address Plan**: 인터페이스, 링크, IP/마스크, VLAN, 기대 성공·실패 경로.
4. **Practice**: 재현 가능한 장비별 설정과 각 명령어의 의미.
5. **Verification & Packet Walkthrough**: show 명령·트래픽 확인·Simulation 또는 pcap과 예상 결과.
6. **Troubleshooting**: 장애 삽입 → 증상 → 진단 가설 → 근거 → 수정·재검증.
7. **종료 주관식 퀴즈**: 핵심 원리 2문항, 패킷·장비 내부 동작 2문항, 장애 추론 1문항을 준비한다. LLM은 정답을 미리 보여주지 않고 한 번에 1~2문항씩 출제·채점·재질문한다. 문서에는 질문과 채점 관점만 두고 사용자 실제 답변은 종료 후 학습 기록에 요약한다.
8. **Review & Next**: 핵심 회상 질문, 연계되는 나선형 심화 주제.
9. **Progress & Evidence**: 이론·구축·검증·복구를 분리 체크하고 수행일/버전/실제 출력을 기록.
10. **Learning Notes / 실제 학습 기록**: Lab 종료 후 사용자가 실제 질문한 추가 개념, 처음의 가설, 교정된 이해, 직접 관찰한 증거, 나중에 다시 다룰 주제를 3~8개 내외로 요약. 결과를 추정하거나 실행하지 않은 선택 과제를 완료로 표시하지 않는다.

## 의존성 관리

- **고유 Lab ID는 불변**으로 사용한다. `prerequisites`에는 존재하는 선행 Lab ID만 쓴다.
- 커리큘럼은 학습 순서와 난이도별 재방문 경로를 관리하며, 각 Lab 본문은 그 Lab 수행에 필요한 최소 이론을 자족적으로 설명한다.
- 아직 작성하지 않은 Lab은 링크로 가장하지 말고 **향후 학습 주제**로 표기한다.
- 별도 Markdown 분리는 단일 파일이 과도하게 길거나 여러 독립 Lab이 공유하는 큰 참조 자료가 있을 때만 검토한다.
- 시험 대응표는 확정 Lab ID와 실제 구현 가능성을 기준으로 갱신한다.

## 상태 및 검증 원칙

- `document_status: planned | ready`, `lab_status: not-tested | in-progress | verified-core | verified` (verified-core는 필수 경로만 검증하고 선택 과제가 남은 상태).
- 문서 작성 ≠ 실제 구축 성공 ≠ 검증 완료 ≠ 주관식 퀴즈 완료. 퀴즈는 별도 상태(미실시/진행 중/완료)로 기록한다.
- Packet Tracer의 명령 지원·기능은 장비 모델/버전별로 차이가 있을 수 있다.
- 전용 파일(.pkt, .gns3, .pcap)은 실제 생성·확인한 경우에만 추가한다.
