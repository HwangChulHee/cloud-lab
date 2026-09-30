# Lab 01 — Cluster Verification

> 학습 단계: **상세 가이드**

## 목표

현재 3노드 클러스터 구조와 시스템 Pod를 확인하고 기준 상태를 기록한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. `kubectl get nodes -o wide`로 master/worker1/worker2를 확인한다.
2. `kubectl get pods -A -o wide`로 kube-system 구성요소를 확인한다.
3. 각 노드의 IP, Kubernetes 버전, container runtime을 기록한다.
4. `kubectl describe node`로 Conditions와 Allocatable/Allocated Resources를 확인한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get nodes -o wide
kubectl get pods -A -o wide
kubectl describe node <node>
kubectl get events -A --sort-by=.lastTimestamp
```

## Compare & Diagnose

이 첫 실습에서는 클러스터를 일부러 중단시키지 않는다. 대신 정상 상태의 기준선을 만든다.

1. master와 worker의 Roles 차이를 확인한다.
2. kube-system Pod가 어느 Node에 배치돼 있는지 비교한다.
3. Node Conditions에서 Ready/MemoryPressure/DiskPressure/PIDPressure를 확인한다.

## 완료 검증

1. 3개 Node가 모두 `Ready`인지 확인한다.
2. 현재 클러스터의 기준 상태를 설명할 수 있다.

## Cleanup

생성한 리소스가 없으므로 별도 삭제는 없다.

## 설명하기

> Node가 정상이라고 판단할 때 확인할 상태는 ______이고, 시스템 Pod는 ______ namespace에서 확인한다.

## 연결된 CKA 강의 전 예습

- [제어 평면 장애를 호스트에서 복구하기](../../07-cka-preview/09-control-plane-recovery/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.

- [CNI 설치와 NetworkPolicy 집행 확인](../../07-cka-preview/14-cni-install/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.

- [CRI와 Linux 네트워크 매개변수 준비](../../07-cka-preview/15-cri-linux-preparation/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.
