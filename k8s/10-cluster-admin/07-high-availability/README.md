# HA API 엔드포인트·etcd quorum

> 분류: **CKA 필수 개념·선택 구축** · 선수 학습: [독립 학습](../../08-independent/README.md)의 ADM-01, ADM-02 단계 · 환경: 기존 1.27.2 환경을 우선하고 호스트 변경/설치는 별도 VM만 사용

## Overview — 무엇을 이해해야 하는가

Control Plane HA는 API Server 다중화뿐 아니라 안정된 controlPlaneEndpoint(LB)와 etcd의 quorum을 함께 고려해야 한다. 이 단원은 단순한 명령어 암기가 아니라 Kubernetes API 객체의 변화와 실제 Node/Runtime에서 일어나는 현상을 연결하는 학습이다.

**학습 결과:** HA API 엔드포인트·etcd quorum의 책임 컴포넌트, 관찰 증거, 실패 조건을 서로 연결해 설명한다.

## 선수 개념과 내부 동작

Control Plane HA는 API Server 다중화뿐 아니라 안정된 controlPlaneEndpoint(LB)와 etcd의 quorum을 함께 고려해야 한다. stacked etcd는 Control Plane 노드에 멤버가 있고 external etcd는 분리된 etcd 멤버를 사용한다. etcd의 다수결 quorum을 잃으면 새 상태 변경이 중단될 수 있다. 단일 Control Plane에 Worker만 여러 대 있다고 HA가 되는 것은 아니다.

## 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [독립 학습](../../08-independent/README.md)의 ADM-01, ADM-02 단계를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
3. 명령 실행 전에 예상할 객체 상태, Node 구성, 관련 컴포넌트 및 실패 시 증거를 기록한다.

## 관찰 명령

아래는 kubeconfig가 준비된 Linux/bash 셸 기준이다. `sudo`가 필요한 명령은 해당 Node의 호스트 셸에서 실행한다. 해당 객체가 없으면 먼저 선수 실습을 수행한다.

```bash
kubectl get nodes -o wide
kubectl -n kube-system get pods -l component=kube-apiserver -o wide
kubectl -n kube-system get pods -l component=etcd -o wide
```

## 따라 하기 — 순서와 예상 결과

기존 1+2 노드 토폴로지를 그리고 API 서버/etcd의 SPOF를 표시한다. 다음으로 3 Control Plane + LB + Worker 구성에서 한 Control Plane을 정지했을 때 예상 API 접근과 etcd quorum을 각각 계산한다. 자원 여유가 있을 때만 Kubernetes 공식 kubeadm HA 절차에 따라 별도 VM에 실제 다중 Control Plane을 구축한다.

**관찰 기록:** 실행 전 예상 → 실제 spec/status/Events 또는 Linux 상태 → 예상과 다른 이유. 단순히 명령이 오류 없이 종료됐다는 이유로 정상 동작을 확인했다고 처리하지 않는다.

## 고장 가설과 복구

정상 HA의 증거는 2대가 더 존재한다는 사실이 아니라 LB endpoint 접근, 다수 API Server Ready, etcd quorum 유지, 제어 평면 1대 중단 후 API 갱신 성공이다. 2/3 etcd가 중단되면 다수결이 없어 신규 쓰기가 불가능함을 설명한다.

복구 완료 기준은 **동일한 조회나 요청으로 정상 결과를 다시 얻는 것**이다. 관찰할 수 없는 구현(예: CSI driver 미설치, kube-proxy 대체 데이터 평면)은 미검증으로 기록한다.

## 스스로 설명할 문제

1. **HA API 엔드포인트·etcd quorum**이 필요한 이유를 사용자가 겪을 수 있는 실제 문제로 설명할 수 있는가?
2. 이 현상을 만든 API 객체와 실제 실행한 컴포넌트는 각각 무엇인가?
3. 위 예시의 실패 원인과 동일한 외부 증상을 보이는 다른 원인은 무엇이며 첫 번째로 어떤 증거를 확인할 것인가?
4. Pod/Node 또는 Controller를 재시작하지 않고도 진단 가능한 정보는 무엇인가?

## 환경 및 정리

원래 실습 namespace와 공용 애드온은 연결된 기본 단계의 정리 지침을 따른다. Node taint/route/CNI/etcd 및 Kubernetes 패키지 변경은 별도 안전 조건이 명시된 경우에만 수행한다. 실제 VM 실행 여부는 [CHECKPOINTS](../../08-independent/CHECKPOINTS.md)에 별도로 기록한다.

## 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[10-cluster-admin 목차](../README.md) · [전체 독립 학습](../../08-independent/README.md)
