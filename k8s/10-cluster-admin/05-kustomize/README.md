# Kustomize Base·Overlay·patch

> 분류: **CKA 필수** · 선수 학습: [독립 학습](../../08-independent/README.md)의 03-controllers 단계 · 환경: 기존 1.27.2 환경을 우선하고 호스트 변경/설치는 별도 VM만 사용

## Overview — 무엇을 이해해야 하는가

Kustomize는 Kubernetes 리소스의 공통 Base 위에 환경별 변경(overlay)을 선언하는 도구다. 이 단원에서는 실제 컴포넌트의 동작 순서를 학습하고 관찰 증거와 연결한다.

**학습 결과:** Kustomize Base·Overlay·patch의 책임 컴포넌트, 관찰 증거, 실패 조건을 서로 연결해 설명한다.

## 핵심 질문에서 내부 원리까지

**환경별 YAML을 복사하지 않고 관리하려면?**

### 실행 흐름을 따라가기

Kustomize Base는 공통 객체, Overlay는 환경별 변경을 표현한다. kubectl kustomize는 렌더링이고 apply -k는 클러스터 상태 변경이다.

### 예상 상태 해석 예시

dev-web/replicas=2 결과를 얻어도 Base의 replicas=1 파일이 변경됐다는 뜻은 아니다.

> 이 예시는 학습용이며 실제 클러스터 실행 결과가 아니다. 환경·CNI·버전에 따라 출력이 다를 수 있다.

### 개념을 이해했는지 확인하기

- 렌더링과 apply의 차이는?
- 이 과정에서 **API 객체 상태를 만드는 주체**와 **실제 Node에서 실행하는 주체**는 각각 누구인가?
- 비슷한 증상을 유발할 수 있는 다른 원인 하나를 들고 확인할 첫 증거를 설명할 수 있는가?

## 선수 개념과 내부 동작

Kustomize는 Kubernetes 리소스의 공통 Base 위에 환경별 변경(overlay)을 선언하는 도구다. Helm과 달리 템플릿 값 치환을 중심으로 하지 않는다. build/kubectl kustomize는 렌더링 과정이며 실제 클러스터에 적용하지 않는다. Base를 변경하지 않은 채 replicas/image/labels를 환경별로 바꿀 수 있다.

## 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [독립 학습](../../08-independent/README.md)의 03-controllers 단계를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
3. 명령 실행 전에 예상할 객체 상태, Node 구성, 관련 컴포넌트 및 실패 시 증거를 기록한다.

## 관찰 명령

아래는 kubeconfig가 준비된 Linux/bash 셸 기준이다. `sudo`가 필요한 명령은 해당 Node의 호스트 셸에서 실행한다. 해당 객체가 없으면 먼저 선수 실습을 수행한다.

```bash
mkdir -p /tmp/cloud-lab-kustomize/base /tmp/cloud-lab-kustomize/dev
printf 'apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: web\nspec:\n  replicas: 1\n  selector:\n    matchLabels:\n      app: web\n  template:\n    metadata:\n      labels:\n        app: web\n    spec:\n      containers:\n      - name: web\n        image: nginx:1.27-alpine\n' > /tmp/cloud-lab-kustomize/base/deploy.yaml
printf 'resources:\n- deploy.yaml\n' > /tmp/cloud-lab-kustomize/base/kustomization.yaml
printf 'resources:\n- ../base\nnamePrefix: dev-\nreplicas:\n- name: web\n  count: 2\n' > /tmp/cloud-lab-kustomize/dev/kustomization.yaml
kubectl kustomize /tmp/cloud-lab-kustomize/dev
```

## 따라 하기 — 순서와 예상 결과

기존 03단계의 Deployment 구조를 먼저 복습한다. 렌더링 결과에서 name=dev-web/replicas=2를 확인한다. 이어 Base의 replicas=1을 변경하지 않은 상태에서 Overlay 값을 3으로 바꾼 결과를 비교한다. 세번째로 이름이 일치하지 않는 patch를 만들어 렌더 오류를 관찰한 후 수정한다.

**관찰 기록:** 실행 전 예상 → 실제 spec/status/Events 또는 Linux 상태 → 예상과 다른 이유. 단순히 명령이 오류 없이 종료됐다는 이유로 정상 동작을 확인했다고 처리하지 않는다.

## 고장 가설과 복구

오류 재현은 dev의 kustomization.yaml에 `patches:`를 추가해 존재하지 않는 `Deployment/missing`을 대상으로 하는 patch를 지정한 뒤 `kubectl kustomize`의 실패 메시지를 비교하고, 패치를 제거한 후 정상 빌드를 확인한다.

실제 적용을 선택할 때는 namespace를 별도로 만들고 kubectl diff -k와 kubectl apply --dry-run=server -k를 확인한다. 완료 시 /tmp/cloud-lab-kustomize를 정리한다.

복구 뒤에는 동일 조건의 조회/요청으로 다시 확인한다. 관찰할 수 없는 구현은 검증 완료로 표시하지 않는다.

## 다음에 다시 확인하기

설명을 가리고 핵심 질문에 답한 뒤, 위에서 제시한 예상 상태를 자신의 말로 해석한다. 정답 대신 기존 실습의 실제 상태·Events를 근거로 제시한다.

## 환경 및 정리

이 모듈의 관련 리소스는 기본 단계의 Cleanup 전에 관찰한다. 이전 단계가 정리됐다면 Setup부터 다시 실행한다. 위험한 제어 평면/호스트 변경은 별도 VM에서만 수행한다.

## 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[10-cluster-admin 목차](../README.md) · [전체 독립 학습](../../08-independent/README.md)
