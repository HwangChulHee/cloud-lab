# Lab 42 — Architecture & Observability Capstone

> 학습 단계: **가이드 축소**

## 강의 없이 시작하기

이 README가 공식 학습·실습 기록입니다. 아래의 개념 → 구성 → 관찰 → 장애/복구 → 정리 절차를 따라 진행합니다. [예전 독립 코스의 실행 자산](../../05-advanced/03-ingress-canary-tls/README.md)은 보충 참고자료이며 별도 중복 이수 대상이 아닙니다.

## 목표

지금까지 사용한 오브젝트를 실제 Kubernetes 내부 구성요소와 연결해 종합 관찰한다.

## 구성 요소를 하나의 장애 경로로 연결하기

[개념 연결 지도](../../07-cka-preview/CONCEPT_BRIDGE.md)의 Admission·네트워크·로그 경계를 함께 읽는다. 아래 네 경우의 실패 위치와 첫 관찰 대상을 기록한다.

1. RBAC가 요청을 거부해 객체가 생성되지 않음.
2. Quota가 Pod 생성을 거부해 ReplicaSet에 FailedCreate가 남음.
3. Pod는 생성됐지만 scheduler가 조건을 만족하는 노드를 찾지 못함.
4. Pod는 Running이지만 readiness 실패로 Service 외부 요청에 응답하지 않음.

같은 `접속 실패`라도 객체 제어 경로와 앱 트래픽 경로를 구분한다. 컨테이너 로그를 `kubectl logs`로 읽는 것과 노드 수집 에이전트·중앙 저장소로 장기간 보관하는 것도 나눠 설명한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. kube-apiserver, scheduler, controller-manager, etcd, kubelet, containerd, kube-proxy, CoreDNS/CNI를 현재 클러스터에서 찾아낸다.
2. Pod 하나를 생성하며 Events/Pod IP/Node 배치/Service Endpoint를 순서대로 추적한다.
3. `kubectl logs`, `kubectl top`, runtime 로그 위치를 확인한다.
4. Deployment+Service+ConfigMap/Secret+Probe+Ingress/HPA 중 가능한 요소를 조합한 작은 앱 스택을 구성한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 최종 스택에서 selector, readiness, scheduling 중 2개 장애를 연속으로 넣고 원인을 분리해 복구한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. `kubectl apply`부터 실제 Container 실행/네트워크/관측까지 흐름을 한 장으로 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 확장 실습

- [제어 평면 장애를 호스트에서 복구하기](../../07-cka-preview/09-control-plane-recovery/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.


## 종합 장애 과제 — 원인 분리형 진단

이 과제는 기존 개념을 나열하는 복습 대신, **같은 사용자 증상이 다른 계층에서 발생하는 상황**을 구분하는 최종 검증이다. Deployment + Service + ConfigMap + Probe로 최소 앱 스택을 만들고 가능하다면 Ingress/NetworkPolicy를 연결한다.

| 시나리오 | 주입 | 구분해야 할 증거 | 복구 |
|---|---|---|---|
| A. 서비스 이름은 해석되지만 HTTP 실패 | Service selector를 없는 label로 변경 | DNS 정상, EndpointSlice 대상 없음, Pod Ready | selector 원복 후 새 연결 검증 |
| B. Pod Running인데 요청 대상에서 제외 | readiness를 의도적으로 실패시킴 | Pod Running vs Ready, EndpointSlice ready condition | Probe/앱 상태 복구 |
| C. Pod 생성/배치 실패 | Quota 초과 또는 불가능한 nodeAffinity | `FailedCreate` vs `FailedScheduling` | Quota/request/배치 조건 중 실제 원인만 수정 |
| D. Ingress/TLS 실패 (선택) | TLS Secret 이름 불일치 | Ingress 객체/Controller 로그/인증서 검증 | Secret 참조 원복 |

**평가 방법:** 장애 이름을 보지 않고 `kubectl get/describe`, Events, Pod 직접 접근, Service/EndpointSlice, Ingress 순서로 가설과 반증을 기록한다. 복구 전에 다른 원인 하나를 배제할 근거를 명시한다. 장애 전/후 상태, 정확한 변경 사항, 재발 방지 조치를 1페이지 운영 보고서로 정리한다. `curl -k` 성공이나 DNS 응답만으로 HTTPS/애플리케이션 복구를 판정하지 않는다.

연계 심화: [계층별 장애 추론](../../06-architecture/01-architecture-observability-capstone/README.md). 이전 독립 경로의 [Ingress/TLS 재현 명령](../../05-advanced/03-ingress-canary-tls/README.md)은 **기존 참고 자산**으로 남겨 두되 이 Capstone이 공식 완료 기준이다.


## 내부 동작 심화 통합 — 08-system-failure-analysis

이전 INT 단원의 원리와 관찰 내용을 현재 Lab에 통합한다. 아래의 `lab-self-*`은 예전 실습 Namespace이므로 지금 Lab에 생성한 자원을 우선 사용하고, 다른 자원이 필요할 때만 독립된 테스트 Namespace를 생성한다.

### 선수 개념과 내부 동작

HTTP 실패는 DNS, Service/EndpointSlice, kube-proxy/CNI, NetworkPolicy, Ingress Controller, 실제 앱 중 어디서나 시작될 수 있다. 장애를 볼 때 요청 경로를 계층별로 분해한다. API 객체 존재→status/Events→직접 Pod IP→Service DNS/ClusterIP→Ingress 순서로 테스트하면 계층을 좁힐 수 있다. 같은 증상에도 서로 다른 원인이 가능하므로 한번의 성공/실패만으로 결론을 내리지 않는다.

### 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [독립 학습](../../README.md)의 08-operations 단계를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
3. 명령 실행 전에 예상할 객체 상태, Node 구성, 관련 컴포넌트 및 실패 시 증거를 기록한다.

### 관찰 명령

아래는 kubeconfig가 준비된 Linux/bash 셸 기준이다. `sudo`가 필요한 명령은 해당 Node의 호스트 셸에서 실행한다. 해당 객체가 없으면 먼저 선수 실습을 수행한다.

```bash
kubectl get nodes -o wide
kubectl get pods,svc -A
kubectl get endpointslices -A
kubectl get events -A --sort-by=.lastTimestamp
```

### 따라 하기 — 순서와 예상 결과

기존 04-networking, 05-resources-scheduling, 07-security, 08-operations 중 필요한 namespace를 다시 구축한다. 사건 A: selector 오류로 DNS 성공/HTTP 실패. 사건 B: readiness=false로 서비스 대상 제외. 사건 C: RoleBinding 삭제로 403. 각 사건의 예상, 반증 조건, 복구 확인 요청을 기록한다.

**관찰 기록:** 실행 전 예상 → 실제 spec/status/Events 또는 Linux 상태 → 예상과 다른 이유. 단순히 명령이 오류 없이 종료됐다는 이유로 정상 동작을 확인했다고 처리하지 않는다.

### 예시: 같은 HTTP 실패, 서로 다른 두 원인

가상의 client Pod가 `http://web` 호출에 실패했다고 하자. **첫 가설**은 Service selector 불일치다. `nslookup web`은 성공해도 `kubectl get endpointslices -l kubernetes.io/service-name=web`에서 준비된 backend가 없다. **둘째 가설**은 Pod readiness 실패다. EndpointSlice의 주소 또는 ready condition과 Pod Conditions를 비교한다. 두 문제는 사용자 입장에서 비슷하게 보이지만 **원인에 따라 수정하는 리소스가 다르다**.

세 번째 가설로 app이 잘못된 port에서 listen하는 경우를 추가한다. EndpointSlice가 있어도 `wget http://POD_IP:TARGET_PORT`가 실패할 수 있다. 원인을 보기 전에 해결책부터 적용하지 말고 **가설 → 이를 반증할 명령 → 실제 증거 → 최소 수정**을 표로 적는다.

### 난도별 통합 진단

| 단계 | 학습자에게 제공되는 정보 | 완료 기준 |
|---|---|---|
| Level 1 | 원인과 복구 명령 | 원인–결과 설명 |
| Level 2 | 증상과 관련 리소스 | Events/status를 근거로 복구 |
| Level 3 (필수 목표) | 사용자 증상만 | 2개 이상 가설, 반증, 최소 변경, 재검증 |
| Level 4 (선택) | 동시에 발생한 복수 장애 | 장애 우선순위와 독립 원인 구분 |

예시: `http://web` 요청이 실패한다는 증상만 제시한 뒤, selector 불일치와 Pod Ready 실패 중 어느 것인지 처음부터 알려주지 않는다. 증상·가설·진단 명령·복구 후 동일 요청의 결과를 기록한다. 첫 회에는 기존 04·05·07 실습에서 개별 실패를 복습하고 이후 Level 3에서 풀이를 가린다.

### 고장 가설과 복구

사건별 보고 양식: 사용자 증상 / 정상 범위 / 가설 최소 2개 / 첫 진단 명령 / 가설 반증 / 실제 수정 / 동일 요청 재검증 / 재발 방지. CNI 정책 검사는 정책 집행 플러그인이 있을 때만 성공 판정한다.

복구 뒤에는 동일 조건의 조회/요청으로 다시 확인한다. 관찰할 수 없는 구현은 검증 완료로 표시하지 않는다.

### 다음에 다시 확인하기

설명을 가리고 핵심 질문에 답한 뒤, 위에서 제시한 예상 상태를 자신의 말로 해석한다. 정답 대신 기존 실습의 실제 상태·Events를 근거로 제시한다.

### 환경 및 정리

이 모듈의 관련 리소스는 기본 단계의 Cleanup 전에 관찰한다. 이전 단계가 정리됐다면 Setup부터 다시 실행한다. 위험한 제어 평면/호스트 변경은 별도 VM에서만 수행한다.

### 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/tasks/debug/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[09-internals 목차](../README.md) · [전체 독립 학습](../../README.md)
