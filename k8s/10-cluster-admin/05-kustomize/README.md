# ADM-05 Kustomize 기본과 Overlay

> 분류: **CKA 필수** · 연결/선행: **03 완료 후** · [기본 학습](../../08-independent/README.md) · [환경 기준](../../07-cka-preview/ENVIRONMENT.md)

## Overview — 왜 배우는가?

Base와 Overlay로 동일 애플리케이션의 환경 차이를 표현한다. 기존의 관련 실습과 연결해, 객체 조회에 그치지 않고 **컴포넌트의 판단 → Linux/Runtime의 실행 → 상태·로그·이벤트 증거**를 이어서 설명한다.

## 선수 지식과 동작 원리

kubectl kustomize로 replicas=2와 namePrefix를 검증하고 base를 변경하지 않고 overlay의 결과만 달라지는지 비교한다.

## 예측 후 관찰

실행 전에 (1) 예상 상태, (2) 이 상태를 책임지는 컴포넌트, (3) 검증할 증거를 먼저 적는다. 아래 명령은 Linux/bash 셸에서 실행한다. 리소스가 이미 만들어져 있어야 하는 명령은 연결된 이전 단계를 먼저 수행한다.

```bash
mkdir -p /tmp/cloud-lab-kustomize/base /tmp/cloud-lab-kustomize/dev
printf 'apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: web\nspec:\n  replicas: 1\n  selector:\n    matchLabels:\n      app: web\n  template:\n    metadata:\n      labels:\n        app: web\n    spec:\n      containers:\n      - name: web\n        image: nginx:1.27-alpine\n' > /tmp/cloud-lab-kustomize/base/deploy.yaml
printf 'resources:\n- deploy.yaml\n' > /tmp/cloud-lab-kustomize/base/kustomization.yaml
printf 'resources:\n- ../base\nnamePrefix: dev-\nreplicas:\n- name: web\n  count: 2\n' > /tmp/cloud-lab-kustomize/dev/kustomization.yaml
kubectl kustomize /tmp/cloud-lab-kustomize/dev
```

출력이 비어 있거나 오류가 나면 도구 부재·리소스 미준비·실제 장애를 구분한다. 비어 있는 값이나 실패를 정상 동작의 증거로 사용하지 않는다.

## 장애 가설 → 증거 → 복구

overlay에서 존재하지 않는 리소스 이름을 참조하는 잘못된 patch를 추가해 빌드 오류를 기록한 뒤 복구한다.

가설과 관찰 결과가 일치하는지 기록하고, 최소한의 변경으로 복구한 뒤 **처음과 같은 명령/요청**으로 성공을 확인한다. 이 문서는 안전한 관찰 순서가 기본이며, 위험한 장애 주입은 명시한 별도 VM에서만 수행한다.

## 환경 제약 및 정리

이 실습은 /tmp 아래 임시 파일을 생성하며 마지막에 rm -rf /tmp/cloud-lab-kustomize로 정리한다. 실제 적용 전 kubectl apply --dry-run=server -k 를 사용한다.

- Kubernetes 1.27.2에서 실제 실행한 내용과 최신 버전의 공식 설명을 구분한다.
- 이 문서 작성만으로 사용자 VM 실행 완료를 뜻하지 않는다.
- 실습 완료 기록: [CHECKPOINTS](../../08-independent/CHECKPOINTS.md).

## 설명 질문

1. 이 상태는 어떤 컴포넌트가 만들거나 갱신하는가?
2. 정상과 장애를 구분하는 가장 작은 증거는 무엇인가?
3. 같은 증상이 다른 계층에서도 발생할 수 있다면 어떻게 반증할까?

## 공식 문서

- [Kubernetes Architecture](https://kubernetes.io/docs/concepts/architecture/)
- [Service virtual IP](https://kubernetes.io/docs/reference/networking/virtual-ips/)
- [kubeadm upgrade](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)

[모듈 목차](../README.md) · [독립 학습](../../08-independent/README.md)
