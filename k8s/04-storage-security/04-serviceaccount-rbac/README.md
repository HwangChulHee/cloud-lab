# Lab 36 — ServiceAccount & RBAC

> 학습 단계: **가이드 축소**

## 목표

인증된 주체에 namespace/cluster 권한을 부여하고 실제 API 허용/거부를 검증한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. ServiceAccount와 token을 만든다.
2. Pod get/list만 가능한 Role+RoleBinding을 만든다.
3. Token으로 Pod API 성공, Service API 403을 확인한다.
4. ClusterRole/ClusterRoleBinding으로 범위를 확장해 다시 호출한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod <pod>
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. verb/resource 하나를 제거해 403을 재현하고 복구한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. Authentication과 Authorization의 차이를 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 CKA 강의 전 예습

- [Helm으로 Argo CD 설치와 템플릿 비교](../../07-cka-preview/13-helm-argocd/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.
