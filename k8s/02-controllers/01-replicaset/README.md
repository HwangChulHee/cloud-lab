# Lab 17 — ReplicaSet

> 학습 단계: **중간 가이드**

## 목표

Template, replicas, selector와 desired state를 체감한다.

## Recall

Pod, Label/Selector, desired state의 의미를 먼저 회상한다.

## Build & Observe

1. ReplicaSet으로 Pod를 생성한다.
2. replicas를 1→2→3으로 변경한다.
3. Pod 하나를 수동 삭제해 자동 복구를 확인한다.
4. ReplicaSet selector와 일치하는 독립 Pod를 먼저 만든 뒤, ReplicaSet이 해당 Pod를 관리 대상으로 인식하는지 확인한다.
5. `--cascade=orphan`으로 Controller만 삭제했을 때 Pod가 남는 것을 확인한다.

## Validation Exercise

실행 중인 ReplicaSet의 selector를 억지로 변경하는 실험 대신, 별도 YAML에서 `.spec.selector`와 `.spec.template.metadata.labels`를 불일치시켜 생성해 본다.

- API가 왜 해당 정의를 거부하는지 에러 메시지를 읽는다.
- 정상 YAML과 비교해 어떤 계약이 깨졌는지 찾는다.

## Recover

잘못된 manifest의 selector/template label을 일치시킨 뒤 정상 생성한다.

## 완료 검증

1. ReplicaSet이 replicas 수를 유지하는 과정을 설명한다.
2. selector가 기존 Pod를 관리 대상으로 판단하는 기준임을 설명한다.
3. selector와 template labels가 일치해야 하는 이유를 설명한다.

## Cleanup

이 Lab에서 만든 ReplicaSet과 Pod를 삭제한다. orphan Pod가 남았다면 직접 정리한다.

## 설명하기

> ReplicaSet은 ______와 일치하는 Pod 수를 `replicas` 값에 맞추며, 부족하면 ______을 이용해 새 Pod를 만든다.

## 연결된 CKA 강의 전 예습

- [Helm으로 Argo CD 설치와 템플릿 비교](../../07-cka-preview/13-helm-argocd/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.
