# Lab 42 — Architecture & Observability Capstone

> 학습 단계: **가이드 축소**

## 강의 없이 시작하기

[독립 학습 가이드](../../08-independent/08-operations/README.md)에서 개념 설명 → 실행 YAML → 예상 결과 → 장애/복구 → 정리를 순서대로 진행한다. 이 문서는 해당 주제의 복습·추가 과제로 사용한다.

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

연계 심화: [계층별 장애 추론](../../09-internals/08-system-failure-analysis/README.md). 이전 독립 경로의 [Ingress/TLS 재현 명령](../../08-independent/08-operations/README.md)은 **기존 참고 자산**으로 남겨 두되 이 Capstone이 공식 완료 기준이다.
