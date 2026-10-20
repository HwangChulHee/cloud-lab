# 계층별 증상·가설·반증·복구

> 분류: **운영 심화** · 선수 학습: [독립 학습](../../08-independent/README.md)의 08-operations 단계 · 환경: 기존 1.27.2 환경을 우선하고 호스트 변경/설치는 별도 VM만 사용

## Overview — 무엇을 이해해야 하는가

HTTP 실패는 DNS, Service/EndpointSlice, kube-proxy/CNI, NetworkPolicy, Ingress Controller, 실제 앱 중 어디서나 시작될 수 있다. 이 단원에서는 실제 컴포넌트의 동작 순서를 학습하고 관찰 증거와 연결한다.

**학습 결과:** 계층별 증상·가설·반증·복구의 책임 컴포넌트, 관찰 증거, 실패 조건을 서로 연결해 설명한다.

## 핵심 질문에서 내부 원리까지

**HTTP 실패 하나에 얼마나 많은 원인이 있을까?**

### 실행 흐름을 따라가기

Pod Ready, 직접 Pod IP, Service EndpointSlice, ClusterIP, DNS, Ingress를 계층별로 점검한다. 가설을 반증할 최소 관찰을 정해 무작정 재시작하지 않는다.

### 예상 상태 해석 예시

DNS가 성공했어도 Service selector 불일치/NetworkPolicy/앱 port 오류로 HTTP가 실패할 수 있다.

> 이 예시는 학습용이며 실제 클러스터 실행 결과가 아니다. 환경·CNI·버전에 따라 출력이 다를 수 있다.

### 개념을 이해했는지 확인하기

- 첫 명령을 고르는 이유를 설명할 수 있는가?
- 이 과정에서 **API 객체 상태를 만드는 주체**와 **실제 Node에서 실행하는 주체**는 각각 누구인가?
- 비슷한 증상을 유발할 수 있는 다른 원인 하나를 들고 확인할 첫 증거를 설명할 수 있는가?

## 선수 개념과 내부 동작

HTTP 실패는 DNS, Service/EndpointSlice, kube-proxy/CNI, NetworkPolicy, Ingress Controller, 실제 앱 중 어디서나 시작될 수 있다. 장애를 볼 때 요청 경로를 계층별로 분해한다. API 객체 존재→status/Events→직접 Pod IP→Service DNS/ClusterIP→Ingress 순서로 테스트하면 계층을 좁힐 수 있다. 같은 증상에도 서로 다른 원인이 가능하므로 한번의 성공/실패만으로 결론을 내리지 않는다.

## 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [독립 학습](../../08-independent/README.md)의 08-operations 단계를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
3. 명령 실행 전에 예상할 객체 상태, Node 구성, 관련 컴포넌트 및 실패 시 증거를 기록한다.

## 관찰 명령

아래는 kubeconfig가 준비된 Linux/bash 셸 기준이다. `sudo`가 필요한 명령은 해당 Node의 호스트 셸에서 실행한다. 해당 객체가 없으면 먼저 선수 실습을 수행한다.

```bash
kubectl get nodes -o wide
kubectl get pods,svc -A
kubectl get endpointslices -A
kubectl get events -A --sort-by=.lastTimestamp
```

## 따라 하기 — 순서와 예상 결과

기존 04-networking, 05-resources-scheduling, 07-security, 08-operations 중 필요한 namespace를 다시 구축한다. 사건 A: selector 오류로 DNS 성공/HTTP 실패. 사건 B: readiness=false로 서비스 대상 제외. 사건 C: RoleBinding 삭제로 403. 각 사건의 예상, 반증 조건, 복구 확인 요청을 기록한다.

**관찰 기록:** 실행 전 예상 → 실제 spec/status/Events 또는 Linux 상태 → 예상과 다른 이유. 단순히 명령이 오류 없이 종료됐다는 이유로 정상 동작을 확인했다고 처리하지 않는다.

## 예시: 같은 HTTP 실패, 서로 다른 두 원인

가상의 client Pod가 `http://web` 호출에 실패했다고 하자. **첫 가설**은 Service selector 불일치다. `nslookup web`은 성공해도 `kubectl get endpointslices -l kubernetes.io/service-name=web`에서 준비된 backend가 없다. **둘째 가설**은 Pod readiness 실패다. EndpointSlice의 주소 또는 ready condition과 Pod Conditions를 비교한다. 두 문제는 사용자 입장에서 비슷하게 보이지만 **원인에 따라 수정하는 리소스가 다르다**.

세 번째 가설로 app이 잘못된 port에서 listen하는 경우를 추가한다. EndpointSlice가 있어도 `wget http://POD_IP:TARGET_PORT`가 실패할 수 있다. 원인을 보기 전에 해결책부터 적용하지 말고 **가설 → 이를 반증할 명령 → 실제 증거 → 최소 수정**을 표로 적는다.

## 난도별 통합 진단

| 단계 | 학습자에게 제공되는 정보 | 완료 기준 |
|---|---|---|
| Level 1 | 원인과 복구 명령 | 원인–결과 설명 |
| Level 2 | 증상과 관련 리소스 | Events/status를 근거로 복구 |
| Level 3 (필수 목표) | 사용자 증상만 | 2개 이상 가설, 반증, 최소 변경, 재검증 |
| Level 4 (선택) | 동시에 발생한 복수 장애 | 장애 우선순위와 독립 원인 구분 |

예시: `http://web` 요청이 실패한다는 증상만 제시한 뒤, selector 불일치와 Pod Ready 실패 중 어느 것인지 처음부터 알려주지 않는다. 증상·가설·진단 명령·복구 후 동일 요청의 결과를 기록한다. 첫 회에는 기존 04·05·07 실습에서 개별 실패를 복습하고 이후 Level 3에서 풀이를 가린다.

## 고장 가설과 복구

사건별 보고 양식: 사용자 증상 / 정상 범위 / 가설 최소 2개 / 첫 진단 명령 / 가설 반증 / 실제 수정 / 동일 요청 재검증 / 재발 방지. CNI 정책 검사는 정책 집행 플러그인이 있을 때만 성공 판정한다.

복구 뒤에는 동일 조건의 조회/요청으로 다시 확인한다. 관찰할 수 없는 구현은 검증 완료로 표시하지 않는다.

## 다음에 다시 확인하기

설명을 가리고 핵심 질문에 답한 뒤, 위에서 제시한 예상 상태를 자신의 말로 해석한다. 정답 대신 기존 실습의 실제 상태·Events를 근거로 제시한다.

## 환경 및 정리

이 모듈의 관련 리소스는 기본 단계의 Cleanup 전에 관찰한다. 이전 단계가 정리됐다면 Setup부터 다시 실행한다. 위험한 제어 평면/호스트 변경은 별도 VM에서만 수행한다.

## 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/tasks/debug/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[09-internals 목차](../README.md) · [전체 독립 학습](../../08-independent/README.md)
