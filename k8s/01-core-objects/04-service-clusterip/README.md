# Lab 06 — Service ClusterIP

> 학습 단계: **기초 개념·실습 과제**  
> **실습 상태: ✅ 완료 (2026-10-22)**

## 강의 없이 시작하기

[독립 학습 가이드](../../08-independent/04-networking/README.md)에서 개념 설명 → 실행 YAML → 예상 결과 → 장애/복구 → 정리를 순서대로 진행한다. 이 문서는 해당 주제의 복습·추가 과제로 사용한다.

## 목표

휘발성 Pod IP 대신 Service의 고정 진입점을 사용하는 이유를 확인한다.

## 핵심 개념과 오해 방지

ClusterIP는 Service 객체가 유지되는 동안 안정적인 가상 IP다. Service를 삭제하고 다시 만들면 IP가 달라질 수 있다. API Server나 Service 객체가 HTTP 요청을 직접 중계하는 것은 아니며, kube-proxy 또는 대체 데이터 평면이 EndpointSlice의 backend로 전달한다. 요청마다 정확한 균등 분산을 보장하지 않고, 연결 재사용과 sessionAffinity도 결과에 영향을 준다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. Pod와 ClusterIP Service를 만든다.
2. Service IP:port로 호출한다.
3. Pod를 교체한 뒤 Service IP가 유지되는지 확인한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. selector를 깨뜨려 Service는 존재하지만 요청이 실패하는 상태를 만든다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. `kubectl get svc,endpoints`로 정상 연결을 검증한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 실습 완료 기록 (2026-10-22)

- [x] `lab-clusterip` namespace 및 `web-1`, `web-2` Nginx Pod 생성. 두 Pod가 서로 다른 worker에서 Ready.
- [x] `web-svc` ClusterIP `10.97.180.115:80` 및 두 backend EndpointSlice 확인.
- [x] `kube-proxy` 설정 `mode: ""` 확인, 해당 v1.27 환경의 iptables NAT 규칙(`KUBE-SVC`, `KUBE-SEP`, DNAT) 관찰.
- [x] 임시 BusyBox HTTP client로 ClusterIP 요청, Nginx HTML 수신.
- [x] `web-1` 삭제 시 Service IP 유지 및 Endpoint 감소 확인. 재생성 후 Pod IP `20.100.194.76` → `20.100.194.78`, EndpointSlice 갱신 확인.
- [x] Service selector를 `app=nonexistent`로 변경해 Endpoint가 비는 현상과 `Connection refused` 확인.
- [x] selector를 `app=web`으로 복구해 두 Endpoint 및 HTTP 응답 재확인.
- [x] namespace 삭제 후 `NotFound` 확인; 실습 리소스 정리 완료.

> 기록된 IP와 출력은 당시 실습 환경의 관측값이며 이후 재실행 시 달라질 수 있다. 본 기록은 이 기초 Lab 완료 증거이며 별도의 `08-independent` 통합 단계나 `09-internals`/`10-cluster-admin` 수행 완료를 의미하지 않는다.
