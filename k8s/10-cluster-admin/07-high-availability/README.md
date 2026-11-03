# HA API 엔드포인트·etcd quorum

> 분류: **CKA 필수 개념·선택 구축** · 선수 학습: [ADM-01 클러스터 구축](../01-kubeadm-bootstrap/README.md), [ADM-02 etcd](../02-etcd-backup-restore/README.md) · 환경: 기존 클러스터는 읽기 관찰만, 실제 HA 구성·장애 주입은 별도 VM

## Overview — 무엇을 이해해야 하는가

Control Plane HA는 API Server 다중화뿐 아니라 안정된 controlPlaneEndpoint(LB)와 etcd의 quorum을 함께 고려해야 한다. 이 단원에서는 실제 컴포넌트의 동작 순서를 학습하고 관찰 증거와 연결한다.

**학습 결과:** HA API 엔드포인트·etcd quorum의 책임 컴포넌트, 관찰 증거, 실패 조건을 서로 연결해 설명한다.

## 핵심 질문에서 내부 원리까지

**Control Plane이 두 대면 곧 HA인가?**

### 실행 흐름을 따라가기

API LoadBalancer의 접근성, 여러 API Server, etcd의 다수결 quorum을 구별해야 한다. stacked/external etcd는 장애 도메인이 다르다.

### 예상 상태 해석 예시

3-member etcd는 한 대 실패 시 2개 quorum이 있지만 두 대 실패 시 쓰기 불가능하다.

> 이 예시는 학습용이며 실제 클러스터 실행 결과가 아니다. 환경·CNI·버전에 따라 출력이 다를 수 있다.

### 개념을 이해했는지 확인하기

- API LB 장애와 etcd quorum 장애는 어떻게 다른가?
- 이 과정에서 **API 객체 상태를 만드는 주체**와 **실제 Node에서 실행하는 주체**는 각각 누구인가?
- 비슷한 증상을 유발할 수 있는 다른 원인 하나를 들고 확인할 첫 증거를 설명할 수 있는가?

## 선수 개념과 내부 동작

Control Plane HA는 API Server 다중화뿐 아니라 안정된 controlPlaneEndpoint(LB)와 etcd의 quorum을 함께 고려해야 한다. stacked etcd는 Control Plane 노드에 멤버가 있고 external etcd는 분리된 etcd 멤버를 사용한다. etcd의 다수결 quorum을 잃으면 새 상태 변경이 중단될 수 있다. 단일 Control Plane에 Worker만 여러 대 있다고 HA가 되는 것은 아니다.

## 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [독립 학습](../../README.md)에서 [ADM-01](../01-kubeadm-bootstrap/README.md)과 [ADM-02](../02-etcd-backup-restore/README.md)를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
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

복구 뒤에는 동일 조건의 조회/요청으로 다시 확인한다. 관찰할 수 없는 구현은 검증 완료로 표시하지 않는다.

## 다음에 다시 확인하기

설명을 가리고 핵심 질문에 답한 뒤, 위에서 제시한 예상 상태를 자신의 말로 해석한다. 정답 대신 기존 실습의 실제 상태·Events를 근거로 제시한다.

## 환경 및 정리

이 모듈의 관련 리소스는 기본 단계의 Cleanup 전에 관찰한다. 이전 단계가 정리됐다면 Setup부터 다시 실행한다. 위험한 제어 평면/호스트 변경은 별도 VM에서만 수행한다.

## 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[10-cluster-admin 목차](../README.md) · [전체 독립 학습](../../README.md)


## HA 설계 검증 — quorum과 API 가용성

**실습 목표:** 단순히 Control Plane Pod 3개를 만드는 것이 아니라 **API 진입점(LB)과 etcd 데이터 정족수**가 서로 다른 책임을 지닌다는 것을 설명한다.

| 구성 | etcd 과반수 | 허용 가능한 etcd 노드 장애 | API 서버 가용성의 전제 |
|---|---:|---:|---|
| etcd 멤버 1개 | 1 | 0 | 해당 VM이 죽으면 단일 장애점 |
| etcd 멤버 3개 | 2 | 1 | LB가 살아 있는 API Server로 연결 |
| etcd 멤버 5개 | 3 | 2 | LB, 네트워크와 API 서버 상태 별도 확인 |

**주의:** etcd 2개만으로 구성하면 quorum=2여서 1대 장애를 견디지 못한다. API Server가 여러 개라고 해서 etcd HA가 자동으로 달성되지 않는다. 별도 LB가 모든 API Server와 연결 가능한지 확인하고, LB 자신의 SPOF도 설계에서 검토한다.

### 사전 관찰 — 기존 클러스터에서 안전하게 수행

```bash
kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}{"\n"}'
kubectl get nodes -o wide
kubectl -n kube-system get pods -l component=kube-apiserver -o wide
kubectl -n kube-system get pods -l component=etcd -o wide
kubectl get --raw=/readyz
```

Static Pod의 label은 설치 형태에 따라 다를 수 있으므로 `kubectl -n kube-system get pods`로 실제 목록을 함께 확인한다. 여기서는 **읽기만** 하고 Control Plane을 중단하지 않는다.

### 별도 HA VM 선택 과제

1. [공식 kubeadm HA](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/)의 stacked-etcd 또는 external-etcd 토폴로지 중 하나를 선택한다.
2. 3개 Control Plane과 하나 이상의 API LB를 설계하고 LB health check·DNS·고정 진입점을 정의한다.
3. 버전 호환 kubeadm, CRI, CNI를 설치하고 `kubeadm init --control-plane-endpoint`와 `kubeadm join --control-plane`을 사용해 별도 VM을 구성한다. **실제 토큰·인증서 키는 공개하지 않는다.**
4. 한 Control Plane의 장애를 **폐기 가능한 VM**에서만 재현하고, API 요청과 etcd quorum/멤버 상태를 각각 검증한다.
5. 장애 복구 뒤 `kubectl get nodes`, API `/readyz`, 테스트 Deployment/Service 요청까지 확인한다.

**완료 기준:** 개념 경로에서는 HA 설계도·SPOF·quorum 계산과 사고 시나리오를 설명하면 된다. 선택 구축 경로는 실제 VM과 LB/etcd 상태를 증거로 남겼을 때만 별도로 완료 표시한다. 3개의 Control Plane 실습을 기존 1+2 Vagrant 클러스터에서 진행하지 않는다.
