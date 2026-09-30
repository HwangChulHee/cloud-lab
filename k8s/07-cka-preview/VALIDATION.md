# 예습 자료 검증 기록

작성 시점: 2026-09-30. 이 기록은 자료의 정적 검증과 Helm 렌더링 결과이며 실제 사용자 클러스터에서 모든 실습을 실행한 기록은 아니다.

## 2026-09-30 독립 과정 재검증

실제 명령 순서와 성공/실패 판정 조건을 다시 읽고 다음을 수정했다.

- Pod 삭제 후 generation이 그대로인 Controller의 rollout status만으로 복구를 판정하던 부분: Deployment는 새 Pod 두 개의 Ready를 watch로 확인하고, StatefulSet은 새 UID와 Ready를 함께 기다린다.
- readiness 파일을 바로 복구해 실패 관찰을 건너뛸 수 있던 부분: Ready=false 대기를 추가했다.
- Blue/Green 전환과 Service 장애를 전파 전에 원복할 수 있던 부분: 응답 비교/실패 관찰 후 다음 블록으로 넘어가도록 분리했다.
- CronJob 자동 실행을 확인하기 전에 suspend하던 순서: 자동 Job을 먼저 확인한다. 수동 생성 Job도 ownerReference가 clock일 수 있어 이름으로 함께 구분한다.
- Secret API 권한과 kubelet의 volume/env 주입 경로를 구분하고, TLS 인증서 이름 불일치와 Controller의 Secret 참조 오류를 별도로 확인하도록 했다.
- 초보자가 selector/label 관계를 직접 읽을 수 있게 생성된 YAML anchor/alias를 풀었다. 변경된 YAML 7개 파일은 이전 commit과 파싱된 객체가 동일함을 확인했다.

이번에 실행한 검사:

- check_materials.py: 78개 문서 상대 링크, 190개 bash 블록 문법, 138개 YAML 객체와 커리큘럼 연결 검사 통과.
- wait_for_pod.py: 가짜 kubectl 응답으로 이전 Ready Pod → 일시적 부재 → 새 NotReady Pod → 새 Ready Pod, 최초 생성, 삭제 중 Pod, Forbidden 즉시 실패, timeout의 5개 시나리오 통과. 실제 클러스터 실행 결과는 아니다.
- OpenSSL: 문서와 같은 SAN 인증서를 실제 생성해 study.local 검증 성공과 wrong.local hostname mismatch 실패를 확인했다.
- Python 문법과 git diff --check 통과.

이번 환경에는 기존 kubeconform 실행 파일이 없고 release 다운로드가 timeout으로 실패해 스키마 검사는 재실행하지 못했다. 아래 이전 검사의 136 Valid/2 Skipped 기록과 구분한다. 이번 변경에서 Kubernetes YAML 객체의 값/구조는 바뀌지 않았고 파싱 동등성 및 기존 정적 검사를 확인했다. VM/실제 클러스터에서 전체 과정을 실행한 검증도 포함하지 않는다.

## 2026-09-30 독립 학습 커리큘럼 보강

[독립 과정](../08-independent/README.md)을 기본 진입점으로 추가했다. 새 가이드 14개, YAML 파일 15개/객체 73개, 42개 기초와 16개 확장의 연결 데이터를 추가했다. 강의 수강은 선행 조건에서 제거하고 8단계 순서와 별도 플랫폼 경로, 애드온 준비, 정상/실패/복구/정리 기준을 제공했다.

- 전체 Markdown 78개 상대 링크와 bash 185개 블록의 `bash -n` 검사 통과.
- 전체 YAML 138개 객체 파싱, namespace, Pod/Deployment/ReplicaSet/DaemonSet/StatefulSet/Job/CronJob selector 및 volume 연결 검사 통과.
- curriculum.json의 42개 기초·16개 확장 연결 누락/중복과 8단계 선행 순서 검사 통과.
- kubeconform 0.6.7, Kubernetes 1.27.2 + Gateway/CRD catalog: YAML 48개 파일, 136개 객체 Valid, Invalid/Errors 0, 기존 학습용 CRD/인스턴스 2개 Skipped.
- `git diff --check`: 통과.

curriculum.json은 Kubernetes 객체가 아닌 학습 경로 메타데이터이므로 kubeconform에서 파일명으로 제외하고 check_materials.py에서 구조/연결을 검사한다. over.yaml은 LimitRange 거절을 관찰하기 위한 의도적인 실패 입력이며, API schema가 유효하다는 사실이 Admission 통과를 의미하지 않는다.

공식 Metrics Server 호환표, Local Path 설치/제약, Traefik Ingress 설정, kubeadm 설치와 NGF 호환표를 대조했다. 신규 Gateway 준비는 공식 표의 NGF 2.3.0 / Gateway API 1.4.1 조합으로 정리했다. Local Path v0.0.37 공식 설치 manifest에 default StorageClass annotation이 없음을 확인했다.

이 검사에는 VM 생성/OS 패키지 설치, 이미지 pull, 애드온 실행, 실제 TLS/HPA/정책/저장소 복구를 포함하지 않는다. 이번 커리큘럼 변경에서 Helm을 다시 렌더링하지도 않았다. 사용자 클러스터의 실행 완료는 CHECKPOINTS에 별도로 기록한다.

## 2026-09-30 두 자료의 내용 대조 후 보강

[내용 대조 기록](../CONTENT_REVIEW.md)에 입문·CKA 주제의 연결, 원본의 단순화/오타와 남은 실습 범위를 기록했다. 개념 설명 보강과 NodePort 외부 트래픽 정책 비교 YAML을 추가했다.

- `check_materials.py`: 전체 64개 문서 상대 링크, bash 132개 블록 문법 검사 통과. 기초의 추가 YAML까지 포함해 65개 객체 파싱·namespace·Deployment 연결 검사 통과.
- kubeconform 0.6.7, Kubernetes 1.27.2 + Gateway/CRD catalog: 33개 YAML 파일, 63개 객체 Valid, Invalid/Errors 0. 기존 학습용 CRD/인스턴스 2개는 외부 스키마가 없어 Skipped.
- `git diff --check`: 통과.

NodePort의 외부 호출, HPA 계산에 대응하는 실제 확장, scheduler 진단은 사용자 클러스터에서 실행하지 않았다. 이번 검사는 정적 자료 검사이며 Helm을 다시 렌더링하지 않았다. 1.34 전용 설정의 실제 허용 여부와 애드온 동작은 해당 환경에서 별도로 확인한다.

## 2026-09-30 재검토와 수정

기초 42개와 예습 16개 문서의 작업 순서·변경 가능 필드·검증 조건을 다시 검토했다. 아래는 이번 수정 후 실행한 검사이며, 아래쪽 최초 작성 기록의 Helm 렌더링을 이번에 다시 실행했다는 뜻은 아니다.

| 발견한 문제 | 수정 |
|---|---|
| HPA CPU request만 삭제하면 limit에서 request 자동 주입 | request/limit 함께 제거, rollout 후 실제 Pod 확인 |
| 여러 종류를 한 번에 watch하는 명령 | HPA와 Pod watch를 별도 셸로 분리 |
| NetworkPolicy의 other가 송신에서 막혀 광범위 수신 허용도 정답처럼 보임 | 검증용 두 클라이언트의 제한된 egress 허용, 수신 정책만 바꾸는 양성/음성 비교 추가 |
| PV 기본 파일이 재생성돼도 복구 성공으로 오인 가능 | 장애 전에 고유 문구를 저장하고 복구 후 정확히 비교, Pod 삭제 대기 추가 |
| Pod 자원·배치, PVC class, Job command 제자리 변경 가정 | Pod/PVC/Job 재생성 또는 새 객체 비교 방법 명시 |
| Certificate kind가 API group 사이에서 모호함 | explain에 group이 붙은 리소스 이름과 api-version 모두 지정 |
| Ingress canary annotation을 구현 공통 기능처럼 사용 | ingress-nginx 전용임을 표시하고 일반 Ingress/신규 환경과 구분 |
| Ready=false 주소가 EndpointSlice에서 완전히 사라진다고 가정 | ready condition과 실제 Service 전달 대상 구분 |
| 일반 ConfigMap mount와 subPath 갱신 혼동 가능 | 지연 갱신·subPath·앱 재읽기를 분리 |
| 기본 사용자의 admin.conf 읽기 권한과 bash placeholder 오류 | 소유자/600 권한의 kubeconfig 준비, 셸에서 유효한 placeholder 표기 |
| StatefulSet 삭제 후 PVC와 SA token 발급 방식 안내 부족 | PVC 별도 정리, 제한된 수명 TokenRequest 사용 |

이번 검사 결과:

- `check_materials.py`: k8s 전체 63개 문서의 상대 링크와 bash 130개 블록 검사 통과. 예습 YAML 60개 객체의 파싱·namespace·Deployment 연결 검사 통과.
- kubeconform 0.6.7, Kubernetes 1.27.2 + Gateway/CRD catalog 스키마: 32개 YAML 파일, 58개 객체 Valid, Invalid/Errors 0. 학습용 CRD/인스턴스 2개는 외부 스키마가 없어 Skipped이며 YAML 파싱만 확인했다.
- `git diff --check`: 통과.

실제 사용자 Vagrant 클러스터에는 접속하지 않았다. HPA 확장, CNI 정책 전파/집행, PV 파일 보존과 Gateway/TLS 응답은 각 문서의 실제 검증 단계로 확인해야 한다. 기초 문서 상당수는 과제 개요이며 모든 폴더에 실행용 YAML을 갖춘 상태는 아니다. 기초 02는 독립 관찰 Pod 생성부터 삭제까지 실행 명령을 추가했고, 다른 기초는 연결된 예습과 함께 사용한다.

수정 근거: [CPU limit에서 request 기본값 설정](https://kubernetes.io/docs/tasks/configure-pod-container/assign-cpu-resource/), [Pod 변경](https://kubernetes.io/docs/concepts/workloads/pods/), [NetworkPolicy 허용 합집합](https://kubernetes.io/docs/concepts/services-networking/network-policies/), [PV 회수](https://kubernetes.io/docs/concepts/storage/persistent-volumes/), [Ingress NGINX 유지보수 종료](https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/).

## 최초 작성 때 완료한 검사

| 검사 | 결과 |
|---|---|
| 실습 구성 | 16개 주요 실습, 각 실습의 구축·과제·검증·힌트·정리·질문 확인 |
| Markdown 상대 링크 | k8s 전체의 로컬 링크 대상 존재 확인 |
| bash 코드 블록 | 86개 명령 블록의 `bash -n` 검사 통과 |
| YAML 파싱과 기본 연결 | 60개 객체 파싱, preview namespace, Deployment selector, volumeMount/volume 연결 확인 |
| Kubernetes/Gateway API 스키마 | 58개 통과, invalid/error 0, 학습용 CRD 정의/인스턴스 2개는 외부 스키마 부재로 제외 |
| Argo CD chart 8.6.4 | Helm 3.16.4로 Kubernetes 1.34 대상으로 실제 렌더링 |
| chart CRD 분리 | crds.install=true에서 CRD 3개 추출, false에서 CRD 0개 확인 |
| CRD 제외 chart 리소스 | Kubernetes 1.34 스키마로 50개 통과 |
| git diff | 공백 오류 없음 |

## 재확인 명령

저장소 루트에서 PyYAML과 kubeconform을 준비한 뒤 실행한다.

```bash
python3 k8s/07-cka-preview/check_materials.py
kubeconform -strict -summary -kubernetes-version 1.27.2 \
  -schema-location default \
  -schema-location 'https://raw.githubusercontent.com/datreeio/CRDs-catalog/main/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json' \
  -ignore-missing-schemas -ignore-filename-pattern 'curriculum\.json$' k8s
git diff --check
```

Placeholder를 실제 환경 값으로 바꾼 뒤에는 server-side dry-run도 수행할 수 있다. custom resource는 CRD가 먼저 설치돼 있어야 한다.

```bash
kubectl apply --dry-run=server -f 해당파일.yaml
```

정적 검사는 이미지 다운로드, 실제 CNI 정책 집행, 노드 자원 여유, Controller의 route 처리, 런타임 설치를 보장하지 않는다. 각 실습 문서의 실제 요청·상태·복구 검증을 수행한 후에 학습 완료로 표시한다.
