# Lab 07 — Service NodePort

> 학습 단계: **기초 개념·실습 과제**

## 강의 없이 시작하기

[독립 학습 가이드](../../08-independent/04-networking/README.md)에서 개념 설명 → 실행 YAML → 예상 결과 → 장애/복구 → 정리를 순서대로 진행한다. 이 문서는 해당 주제의 복습·추가 과제로 사용한다.

## 목표

Windows Host에서 NodePort를 통해 클러스터 내부 Pod에 접근한다.

## 트래픽 정책과 LoadBalancer 비교 실습

먼저 이 Lab의 기본 과제를 끝낸 뒤 별도 namespace로 비교한다. Pod 한 개를 worker 한 곳에 고정해 `Cluster`와 `Local`의 차이가 드러나게 한다. 저장소 루트의 Linux 셸에서 실행한다.

```bash
kubectl get nodes -L kubernetes.io/hostname -o wide
# 실제 worker의 kubernetes.io/hostname label 값으로 수정한다.
SERVICE_WORKER=REPLACE_WORKER_HOSTNAME
sed "s/REPLACE_WORKER_HOSTNAME/$SERVICE_WORKER/" \
  k8s/01-core-objects/05-service-nodeport/traffic-policy.yaml > /tmp/lab-service-path.yaml
kubectl apply -f /tmp/lab-service-path.yaml
kubectl -n lab-service-path rollout status deploy/web --timeout=120s
kubectl -n lab-service-path get pods -o wide
kubectl -n lab-service-path get svc
kubectl -n lab-service-path get endpointslices -l kubernetes.io/service-name=web-local -o yaml
```

실제 노드 주소와 할당된 nodePort를 기록한다. Windows Host 등 **클러스터 외부**에서 두 worker 각각을 호출한다. Windows PowerShell에서는 `curl.exe --connect-timeout 3 --max-time 5 http://NODE_IP:NODE_PORT`의 주소와 포트를 실제 값으로 바꾼다. 노드 내부에서 자기 Service를 호출한 결과로 외부 트래픽 정책을 판단하지 않는다.

| 대상 | Pod가 있는 worker | Pod가 없는 worker |
|---|---|---|
| web-cluster | Ready backend로 전달 | 다른 노드의 Ready backend로 전달 가능 |
| web-local | 로컬 Ready backend로 전달 | 로컬 backend가 없어 요청 실패 예상 |
| web-lb | 외부 LB 구현이 제공하는 주소로 확인 | 구현 없이 EXTERNAL-IP가 Pending이면 예상한 환경 제약 |

`externalTrafficPolicy: Local`은 외부 트래픽을 로컬 endpoint로 제한하고 노드 사이 전달에 따른 소스 NAT를 피하는 데 사용한다. 클라이언트 앞단 NAT까지 없애는 설정은 아니다. `Cluster`는 원격 노드의 endpoint도 사용할 수 있다. 노드 방화벽, CNI, Service 데이터 평면 문제가 있으면 양쪽 모두 실패할 수 있으므로 Pod Ready와 endpoint부터 확인한다.

LoadBalancer는 Kubernetes 객체만으로 외부 장비를 만드는 기능이 아니다. 별도의 LB 구현과 주소 풀이 필요하다. 구현에 따라 NodePort를 거치거나 Pod로 직접 전달할 수 있다. 여기서는 외부 구현을 설치하지 않고 Pending 상태와 Service 설정을 관찰한다.

Pod를 다른 worker로 옮기려면 원본 YAML의 hostname을 바꿔 apply하고 rollout을 기다린 뒤 같은 표를 다시 채운다. 마지막에 `kubectl delete namespace lab-service-path`와 `rm -f /tmp/lab-service-path.yaml`로 정리한다.

참고: [Service의 외부 트래픽 정책](https://kubernetes.io/docs/concepts/services-networking/service/#traffic-policies).

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. worker1/2에 Pod를 배치하고 NodePort Service를 만든다.
2. Windows에서 `192.168.56.31:<nodePort>`와 `.32`로 호출한다.
3. 반복 호출로 Pod 응답 분산을 확인한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. Pod 하나를 삭제하고 요청 결과 변화를 관찰한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. NodePort → Service → Pod 경로를 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 확장 실습

- [Service와 NodePort 연결 추적](../../07-cka-preview/05-service-nodeport/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.
