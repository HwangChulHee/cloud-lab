# Admission·PSA·SecurityContext

> 분류: **필수 개념** · 선수 학습: [독립 학습](../../08-independent/README.md)의 07-security 단계 · 환경: 기존 1.27.2 환경을 우선하고 호스트 변경/설치는 별도 VM만 사용

## Overview — 무엇을 이해해야 하는가

API 요청은 인증과 인가 후 Mutating/Validating Admission을 거쳐 저장될 수 있다. 이 단원에서는 실제 컴포넌트의 동작 순서를 학습하고 관찰 증거와 연결한다.

**학습 결과:** Admission·PSA·SecurityContext의 책임 컴포넌트, 관찰 증거, 실패 조건을 서로 연결해 설명한다.

## 핵심 질문에서 내부 원리까지

**RBAC 허용인데 Pod 생성이 거부되는 이유는?**

### 실행 흐름을 따라가기

Authentication은 신원, Authorization은 권한, Admission은 객체 보안/변형 정책을 검사한다. PSA는 namespace enforce/warn/audit에 따라 결과가 달라진다.

### 예상 상태 해석 예시

kubectl auth can-i 결과가 yes여도 PodSecurity 위반으로 server dry-run이 거부될 수 있다.

> 이 예시는 학습용이며 실제 클러스터 실행 결과가 아니다. 환경·CNI·버전에 따라 출력이 다를 수 있다.

### 개념을 이해했는지 확인하기

- RBAC 거부와 PSA 거부의 처리 계층은 각각?
- 이 과정에서 **API 객체 상태를 만드는 주체**와 **실제 Node에서 실행하는 주체**는 각각 누구인가?
- 비슷한 증상을 유발할 수 있는 다른 원인 하나를 들고 확인할 첫 증거를 설명할 수 있는가?

## 선수 개념과 내부 동작

API 요청은 인증과 인가 후 Mutating/Validating Admission을 거쳐 저장될 수 있다. RBAC가 허용해도 Admission은 Pod 구성을 거부할 수 있다. Pod Security Admission(PSA)은 namespace의 enforce/audit/warn 레이블로 privileged/baseline/restricted 수준을 적용한다. restricted는 권한 상승 방지, capability, seccomp 등 Pod의 보안 컨텍스트 제약을 요구한다. Pod Security Standards와 Linux UID/capabilities/seccomp는 서로 연결되지만 같은 개념은 아니다.

## 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [독립 학습](../../08-independent/README.md)의 07-security 단계를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
3. 명령 실행 전에 예상할 객체 상태, Node 구성, 관련 컴포넌트 및 실패 시 증거를 기록한다.

### 예시: 권한이 충분한데 Pod가 거절된다

`lab-int-psa` namespace에 `pod-security.kubernetes.io/enforce=restricted`가 설정돼 있다고 가정한다. 사용자가 `kubectl auth can-i create pods -n lab-int-psa`에서 `yes`를 보더라도 `privileged: true`를 포함한 Pod는 Admission 단계에서 거부될 수 있다.

| 단계 | 질문 | 증거 |
|---|---|---|
| Authentication | 누가 요청했나? | kubeconfig/Token/인증서 |
| Authorization | Pod 생성 권한이 있나? | `kubectl auth can-i` |
| Admission | 요청 Pod가 보안 정책을 충족하나? | `kubectl apply --dry-run=server` 응답 |

[unsafe Pod](./unsafe-pod.yaml)와 [restricted Pod](./restricted-pod.yaml)를 비교하고 `allowPrivilegeEscalation`, `runAsNonRoot`, `capabilities.drop`, `seccompProfile`의 차이를 설명한다. 이미 API에서 거부된 Pod는 kubelet에 배치되지 않는다.

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

복구 뒤에는 동일 조건의 조회/요청으로 다시 확인한다. 관찰할 수 없는 구현은 검증 완료로 표시하지 않는다.

## 다음에 다시 확인하기

설명을 가리고 핵심 질문에 답한 뒤, 위에서 제시한 예상 상태를 자신의 말로 해석한다. 정답 대신 기존 실습의 실제 상태·Events를 근거로 제시한다.

## 환경 및 정리

이 모듈의 관련 리소스는 기본 단계의 Cleanup 전에 관찰한다. 이전 단계가 정리됐다면 Setup부터 다시 실행한다. 위험한 제어 평면/호스트 변경은 별도 VM에서만 수행한다.

## 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/concepts/security/pod-security-admission/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[09-internals 목차](../README.md) · [전체 독립 학습](../../08-independent/README.md)
