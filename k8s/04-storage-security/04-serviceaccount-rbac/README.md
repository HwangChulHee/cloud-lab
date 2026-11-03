# Lab 36 — ServiceAccount & RBAC

> 학습 단계: **가이드 축소**

## 강의 없이 시작하기

이 README가 공식 학습·실습 기록입니다. 아래의 개념 → 구성 → 관찰 → 장애/복구 → 정리 절차를 따라 진행합니다. [예전 독립 코스의 실행 자산](../../04-storage-security/03-x509-kubeconfig-api/README.md)은 보충 참고자료이며 별도 중복 이수 대상이 아닙니다.

## 목표

인증된 주체에 namespace/cluster 권한을 부여하고 실제 API 허용/거부를 검증한다.

## 핵심 개념과 오해 방지

Role은 namespace에 권한 규칙을 정의하며 RoleBinding은 그 namespace 안에서 규칙을 주체에게 연결한다. ClusterRole을 RoleBinding으로 참조해도 해당 namespace 범위에 적용된다. ClusterRoleBinding은 클러스터 전역에 권한을 부여한다. apiGroups의 core API는 빈 문자열이고 deployments는 apps, jobs는 batch다.

인증 실패(401), 인증됐지만 RBAC 거절(403), Admission 정책에 의한 거절을 구분한다. Quota/LimitRange 거절도 Forbidden일 수 있으므로 상태코드만으로 RBAC 문제라고 단정하지 않는다. 이 실습의 ClusterRole은 pods/services get/list 같은 필요한 권한만 부여하고 `*` 권한을 기본 풀이로 사용하지 않는다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. 실습 namespace에 ServiceAccount를 만들고 `kubectl -n NAMESPACE create token SERVICEACCOUNT_NAME --duration=10m`으로 제한된 수명의 token을 발급한다. 1.24 이후 자동 생성되는 영구 token Secret을 기대하지 않는다. NAMESPACE/SERVICEACCOUNT_NAME은 실습에서 만든 실제 이름으로 바꾼다.
2. Pod get/list만 가능한 Role+RoleBinding을 만든다.
3. Token으로 Pod API 성공, Service API 403을 확인한다.
4. ClusterRole/ClusterRoleBinding으로 범위를 확장해 다시 호출한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. verb/resource 하나를 제거해 403을 재현하고 복구한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. Authentication과 Authorization의 차이를 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 확장 실습

- [Helm으로 Argo CD 설치와 템플릿 비교](../../07-cka-preview/13-helm-argocd/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.


## 독립 심화: RBAC 허용과 Admission 거부 구분

`kubectl auth can-i create pods`의 `yes`는 API 요청의 모든 단계가 성공한다는 뜻이 아니다. RBAC 허용 이후에도 Pod Security Admission(PSA)이나 리소스 정책이 객체를 거부할 수 있다.

- 실습용 Namespace에 PSA `enforce=restricted`를 설정하고 권한이 허용된 주체로 제한 위반 Pod를 **server-side dry-run** 한다.
- `kubectl auth can-i` 출력, API Server의 거부 메시지, Pod가 실제 생성되었는지를 분리해서 기록한다.
- `enforce`/ `warn`/`audit`, `privileged`/`baseline`/`restricted`의 의미와 Linux securityContext(capabilities, seccomp, 권한 상승 금지)의 관계를 설명한다.
- 실패 확인 후 해당 테스트 Namespace를 정리하고 다른 Lab에 PSA 제한을 남기지 않는다.

자세한 예제와 검증 근거는 [Admission과 Pod Security](../../04-storage-security/04-serviceaccount-rbac/README.md)를 참고한다. 이 주제는 기존 SA 토큰과 Role/RoleBinding 실습의 추가 심화이며 별도 기초 필수 Lab으로 중복 산입하지 않는다.


## 내부 동작 심화 통합 — 07-admission-pod-security

이전 INT 단원의 원리와 관찰 내용을 현재 Lab에 통합한다. 아래의 `lab-self-*`은 예전 실습 Namespace이므로 지금 Lab에 생성한 자원을 우선 사용하고, 다른 자원이 필요할 때만 독립된 테스트 Namespace를 생성한다.

### 선수 개념과 내부 동작

API 요청은 인증과 인가 후 Mutating/Validating Admission을 거쳐 저장될 수 있다. RBAC가 허용해도 Admission은 Pod 구성을 거부할 수 있다. Pod Security Admission(PSA)은 namespace의 enforce/audit/warn 레이블로 privileged/baseline/restricted 수준을 적용한다. restricted는 권한 상승 방지, capability, seccomp 등 Pod의 보안 컨텍스트 제약을 요구한다. Pod Security Standards와 Linux UID/capabilities/seccomp는 서로 연결되지만 같은 개념은 아니다.

### 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [독립 학습](../../README.md)의 07-security 단계를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
3. 명령 실행 전에 예상할 객체 상태, Node 구성, 관련 컴포넌트 및 실패 시 증거를 기록한다.

### 예시: 권한이 충분한데 Pod가 거절된다

`lab-int-psa` namespace에 `pod-security.kubernetes.io/enforce=restricted`가 설정돼 있다고 가정한다. 사용자가 `kubectl auth can-i create pods -n lab-int-psa`에서 `yes`를 보더라도 `privileged: true`를 포함한 Pod는 Admission 단계에서 거부될 수 있다.

| 단계 | 질문 | 증거 |
|---|---|---|
| Authentication | 누가 요청했나? | kubeconfig/Token/인증서 |
| Authorization | Pod 생성 권한이 있나? | `kubectl auth can-i` |
| Admission | 요청 Pod가 보안 정책을 충족하나? | `kubectl apply --dry-run=server` 응답 |

[unsafe Pod](./unsafe-pod.yaml)와 [restricted Pod](./restricted-pod.yaml)를 비교하고 `allowPrivilegeEscalation`, `runAsNonRoot`, `capabilities.drop`, `seccompProfile`의 차이를 설명한다. 이미 API에서 거부된 Pod는 kubelet에 배치되지 않는다.

### 관찰 명령

아래는 kubeconfig가 준비된 Linux/bash 셸 기준이다. `sudo`가 필요한 명령은 해당 Node의 호스트 셸에서 실행한다. 해당 객체가 없으면 먼저 선수 실습을 수행한다.

```bash
kubectl create namespace lab-int-psa
kubectl label namespace lab-int-psa pod-security.kubernetes.io/enforce=restricted
kubectl get namespace lab-int-psa --show-labels
kubectl auth can-i create pods -n lab-int-psa
```

### 따라 하기 — 순서와 예상 결과

기존 07-security를 먼저 수행한다. lab-int-psa에 다음 두 Pod manifest를 별도 파일로 작성한다. 첫 번째는 기본 nginx Pod로 restricted 위반을 관찰한다. 두 번째에는 runAsNonRoot:true, allowPrivilegeEscalation:false, capabilities.drop:[ALL], seccompProfile.type:RuntimeDefault를 설정하고 이미지가 비root를 지원하는지 확인한다. 먼저 다음 문서 제공 예제를 사용한다.

```bash
kubectl apply --dry-run=server -f k8s/04-storage-security/04-serviceaccount-rbac/unsafe-pod.yaml
kubectl apply --dry-run=server -f k8s/04-storage-security/04-serviceaccount-rbac/restricted-pod.yaml
```

첫 번째는 Admission 거부, 두 번째는 서버 정책을 충족한다면 dry-run 통과를 예상한다. namespace는 앞 단계에서 만든 `lab-int-psa`를 사용한다. 단, 이미지가 비root 실행을 지원하는지도 실제 이미지 설정과 함께 확인한다. 먼저 --dry-run=server로 양쪽을 비교한 다음 허용되는 Pod만 실제 생성하고 이벤트를 확인한다.

**관찰 기록:** 실행 전 예상 → 실제 spec/status/Events 또는 Linux 상태 → 예상과 다른 이유. 단순히 명령이 오류 없이 종료됐다는 이유로 정상 동작을 확인했다고 처리하지 않는다.

### 고장 가설과 복구

RBAC의 forbidden과 PSA 위반 오류 메시지를 구분한다. restricted 위반 Pod는 API 생성 단계에서 실패하므로 kubelet 로그에 존재하지 않을 수 있다. 실습 후 namespace를 삭제하며 system namespace의 PSA 레이블은 수정하지 않는다.

복구 뒤에는 동일 조건의 조회/요청으로 다시 확인한다. 관찰할 수 없는 구현은 검증 완료로 표시하지 않는다.

### 다음에 다시 확인하기

설명을 가리고 핵심 질문에 답한 뒤, 위에서 제시한 예상 상태를 자신의 말로 해석한다. 정답 대신 기존 실습의 실제 상태·Events를 근거로 제시한다.

### 환경 및 정리

이 모듈의 관련 리소스는 기본 단계의 Cleanup 전에 관찰한다. 이전 단계가 정리됐다면 Setup부터 다시 실행한다. 위험한 제어 평면/호스트 변경은 별도 VM에서만 수행한다.

### 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/concepts/security/pod-security-admission/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[Kubernetes 공식 커리큘럼](../../README.md)
