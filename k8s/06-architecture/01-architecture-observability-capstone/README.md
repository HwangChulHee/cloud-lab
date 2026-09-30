# Lab 42 — Architecture & Observability Capstone

> 학습 단계: **가이드 축소**

## 목표

지금까지 사용한 오브젝트를 실제 Kubernetes 내부 구성요소와 연결해 종합 관찰한다.

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

## 연결된 CKA 강의 전 예습

- [제어 평면 장애를 호스트에서 복구하기](../../07-cka-preview/09-control-plane-recovery/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.
