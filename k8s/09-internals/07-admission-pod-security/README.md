# Admission·PSA·SecurityContext

> 분류: **필수 개념** · 선수 학습: [독립 학습](../../08-independent/README.md)의 07-security 단계 · 환경: 기존 1.27.2 환경을 우선하고 호스트 변경/설치는 별도 VM만 사용

## Overview — 무엇을 이해해야 하는가

API 요청은 인증과 인가 후 Mutating/Validating Admission을 거쳐 저장될 수 있다. 이 단원은 단순한 명령어 암기가 아니라 Kubernetes API 객체의 변화와 실제 Node/Runtime에서 일어나는 현상을 연결하는 학습이다.

**학습 결과:** Admission·PSA·SecurityContext의 책임 컴포넌트, 관찰 증거, 실패 조건을 서로 연결해 설명한다.

## 선수 개념과 내부 동작

API 요청은 인증과 인가 후 Mutating/Validating Admission을 거쳐 저장될 수 있다. RBAC가 허용해도 Admission은 Pod 구성을 거부할 수 있다. Pod Security Admission(PSA)은 namespace의 enforce/audit/warn 레이블로 privileged/baseline/restricted 수준을 적용한다. restricted는 권한 상승 방지, capability, seccomp 등 Pod의 보안 컨텍스트 제약을 요구한다. Pod Security Standards와 Linux UID/capabilities/seccomp는 서로 연결되지만 같은 개념은 아니다.

## 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [독립 학습](../../08-independent/README.md)의 07-security 단계를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
3. 명령 실행 전에 예상할 객체 상태, Node 구성, 관련 컴포넌트 및 실패 시 증거를 기록한다.

## 관찰 명령

아래는 kubeconfig가 준비된 Linux/bash 셸 기준이다. `sudo`가 필요한 명령은 해당 Node의 호스트 셸에서 실행한다. 해당 객체가 없으면 먼저 선수 실습을 수행한다.

```bash
kubectl create namespace lab-int-psa
kubectl label namespace lab-int-psa pod-security.kubernetes.io/enforce=restricted
kubectl get namespace lab-int-psa --show-labels
kubectl auth can-i create pods -n lab-int-psa
```

## 따라 하기 — 순서와 예상 결과

기존 07-security를 먼저 수행한다. lab-int-psa에 다음 두 Pod manifest를 별도 파일로 작성한다. 첫 번째는 기본 nginx Pod로 restricted 위반을 관찰한다. 두 번째에는 runAsNonRoot:true, allowPrivilegeEscalation:false, capabilities.drop:[ALL], seccompProfile.type:RuntimeDefault를 설정하고 이미지가 비root를 지원하는지 확인한다. 먼저 다음 문서 제공 예제를 사용한다.

```bash
kubectl apply --dry-run=server -f k8s/09-internals/07-admission-pod-security/unsafe-pod.yaml
kubectl apply --dry-run=server -f k8s/09-internals/07-admission-pod-security/restricted-pod.yaml
```

첫 번째는 Admission 거부, 두 번째는 서버 정책을 충족한다면 dry-run 통과를 예상한다. namespace는 앞 단계에서 만든 `lab-int-psa`를 사용한다. 단, 이미지가 비root 실행을 지원하는지도 실제 이미지 설정과 함께 확인한다. 먼저 --dry-run=server로 양쪽을 비교한 다음 허용되는 Pod만 실제 생성하고 이벤트를 확인한다.

**관찰 기록:** 실행 전 예상 → 실제 spec/status/Events 또는 Linux 상태 → 예상과 다른 이유. 단순히 명령이 오류 없이 종료됐다는 이유로 정상 동작을 확인했다고 처리하지 않는다.

## 고장 가설과 복구

RBAC의 forbidden과 PSA 위반 오류 메시지를 구분한다. restricted 위반 Pod는 API 생성 단계에서 실패하므로 kubelet 로그에 존재하지 않을 수 있다. 실습 후 namespace를 삭제하며 system namespace의 PSA 레이블은 수정하지 않는다.

복구 완료 기준은 **동일한 조회나 요청으로 정상 결과를 다시 얻는 것**이다. 관찰할 수 없는 구현(예: CSI driver 미설치, kube-proxy 대체 데이터 평면)은 미검증으로 기록한다.

## 스스로 설명할 문제

1. **Admission·PSA·SecurityContext**이 필요한 이유를 사용자가 겪을 수 있는 실제 문제로 설명할 수 있는가?
2. 이 현상을 만든 API 객체와 실제 실행한 컴포넌트는 각각 무엇인가?
3. 위 예시의 실패 원인과 동일한 외부 증상을 보이는 다른 원인은 무엇이며 첫 번째로 어떤 증거를 확인할 것인가?
4. Pod/Node 또는 Controller를 재시작하지 않고도 진단 가능한 정보는 무엇인가?

## 환경 및 정리

원래 실습 namespace와 공용 애드온은 연결된 기본 단계의 정리 지침을 따른다. Node taint/route/CNI/etcd 및 Kubernetes 패키지 변경은 별도 안전 조건이 명시된 경우에만 수행한다. 실제 VM 실행 여부는 [CHECKPOINTS](../../08-independent/CHECKPOINTS.md)에 별도로 기록한다.

## 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/concepts/security/pod-security-admission/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[09-internals 목차](../README.md) · [전체 독립 학습](../../08-independent/README.md)
