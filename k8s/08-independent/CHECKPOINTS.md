# 단계별 완료 기준 — 실행·진단·설명을 따로 확인하기

처음에는 YAML과 풀이를 참고해 실행한다. 두 번째에는 풀이를 닫고 같은 요구사항을 재현한다. 명령어를 외워 타이핑하는 것이 목표는 아니다. 문서 검색은 허용하며, 왜 그 변경을 했는지 설명한다. 강의 수강이나 단순 읽기를 실행 완료로 체크하지 않는다.

| 단계 | 정상 증거 | 실패를 구분할 증거 | 넘어갈 조건 |
|---|---|---|---|
| 01 Pod | 2/2 Ready, localhost HTML, 공유 파일 | /tmp 파일 없음, Pod 삭제 뒤 자동 생성 없음 | Pod/컨테이너/volume/label의 차이 설명 |
| 02 설정 | env·일반 mount·subPath 초기 값 | 변경 후 서로 다른 값, immutable 거절 | 왜 Pod 재생성이 필요한 경우가 있는지 설명 |
| 03 Controller | replicas 복구, Job 3/3, blue/green 전환 | 잘못된 이미지 Events/rollout timeout | 컨테이너 restart와 Controller 재생성 구분 |
| 04 네트워크 | ClusterIP/DNS/수동 endpoint 응답 | DNS 성공 + HTTP 실패, endpoint 없음 | 외부 Cluster/Local 결과를 backend 노드와 연결 |
| 05 자원·배치 | QoS 3종, readiness/liveness 결과, 두 노드 분리 | Pending vs FailedCreate, taint 조건 | request/limit와 상태별 첫 관찰 대상 설명, taint 원복 |
| 06 저장소 | 고유 문구 보존, 두 StatefulSet PVC Bound | PVC Pending과 Pod mount 실패 구분 | Retain/Delete와 emptyDir/PVC 수명 설명 |
| 07 인증·권한 | 인증서 API NodeList, SA 200/403 | binding 삭제 후 권한 거부 | cluster/user/context/RBAC 분리, 임시 인증 파일 제거 |
| 08 운영 | HTTP/TLS/HPA 관찰, 통합 사례 복구 | selector·Probe·이미지·Quota·RBAC·TLS 차이 | 두 사례는 풀이 없이, 세 번째는 직접 예상/검증 |

각 단계에 연결된 확장 실습은 그 문서의 완료 기준까지 확인한다. HPA가 확장될 부하를 충분히 주지 못했거나 NetworkPolicy CNI가 집행하지 않으면 그 **실습만 보류**로 표시한다. 환경 제약을 성공으로 대신하지 않는다. 다음 주제를 읽고 준비하는 것은 계속할 수 있다.

## 기록 양식

```text
단계/실습:
context / Kubernetes 버전 / namespace:
정상 상태 증거:
변경한 필드와 예상:
실제 status / Events / 로그 / 응답:
실패가 발생한 단계(API/배치/실행/트래픽):
복구에 필요한 최소 변경:
복구 뒤 같은 검증의 결과:
파일/PV/taint/애드온 원복 여부:
내 말로 설명한 원인:
두 번째 실행에서 참고한 문서:
완료 / 보류와 이유:
```

## 예상 실패를 성공으로 오인하지 않기

- 문서가 의도적으로 실패를 만들었다면 오류 메시지를 남긴다. 그 명령의 실패는 실습 실패가 아니다.
- Ready 대기/rollout이 timeout이면 정상 준비가 완료되지 않은 상태다. 다음 단계 명령을 무조건 이어 실행하지 않는다.
- 외부 LB Pending은 구현 미설치 확인이고 외부 LB 라우팅을 검증한 기록은 아니다.
- StatefulSet 데이터 비교는 파일 존재뿐 아니라 **원래 고유 문구**가 같은지 본다.
- TLS는 신뢰할 인증서와 이름 검증을 함께 확인한다. curl -k만으로 완료하지 않는다.
- 새 설치/제어 평면 장애 주입은 별도 VM에서 진행하고 스냅샷 복구까지 독립적으로 기록한다.

[독립 학습 순서](./README.md)
