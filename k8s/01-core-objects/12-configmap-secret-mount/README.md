# Lab 14 — ConfigMap & Secret Mount

> 학습 단계: **기초 개념·실습 과제**

## 강의 없이 시작하기

[독립 학습 가이드](../../08-independent/02-configuration/README.md)에서 개념 설명 → 실행 YAML → 예상 결과 → 장애/복구 → 정리를 순서대로 진행한다. 이 문서는 해당 주제의 복습·추가 과제로 사용한다.

## 목표

ConfigMap/Secret을 파일로 마운트하는 방식을 확인한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. 파일 기반 ConfigMap/Secret을 만든다.
2. Pod의 `/mount`에 마운트하고 내용을 확인한다.
3. 일반 volume mount에서 ConfigMap 값을 변경하고 마운트 파일의 지연 갱신을 관찰한다. subPath 방식은 자동 갱신되지 않는다. 파일 갱신과 애플리케이션의 설정 재읽기는 별도로 확인한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 잘못된 key/path 설정으로 원하는 파일이 없는 상태를 만든다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. Env 방식과 Volume Mount 방식의 차이를 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 확장 실습

- [ConfigMap으로 TLS 설정 바꾸기](../../07-cka-preview/01-configmap-tls/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.

## 실습 기록 (2026-10-28)

- **환경:** k8s-master에서 kubectl 실행, k8s-worker1에 두 Pod 스케줄링(Kubernetes v1.27.2).
- **생성:** Namespace `lab-config-mount`; Master VM의 `app.conf`와 `credentials.txt`에서 각각 `app-file-config` ConfigMap과 `app-file-secret` Secret 생성(`kubectl create --from-file`).
- **파일 마운트:** `config-mount-pod`(20.100.194.97)에서 `/etc/app/app.conf`와 `/etc/secret/credentials.txt` 확인. 값은 `APP_MODE=production`, `LOG_LEVEL=info`, 데모 Secret `demo-token-123`.
- **내부 구조:** `app.conf -> ..data/app.conf`; 초기 `..data`가 `..2026_10_28_13_13_19...`를 가리켰고 ConfigMap 갱신 뒤 `..2026_10_28_13_17_02...`로 전환됨을 `ls -la`로 확인.
- **일반 마운트 갱신:** `kubectl edit configmap`으로 `development/debug` 수정 후 Pod 재생성 없이 파일 변경 확인. 다시 `staging/warning`으로 수정한 직후 일시적으로 이전 값이 남았다가 이후 새 값 반영됨.
- **subPath 비교:** 별도 `config-subpath-pod`(20.100.194.98)를 `/tmp/app.conf`에 `subPath: app.conf`로 마운트. ConfigMap을 `staging/warning`으로 수정한 후 일반 마운트는 최신 값, subPath는 `development/debug`으로 유지됨을 확인.
- **이해한 원리:** 두 방식 모두 API 객체 데이터를 kubelet이 Node 측 볼륨으로 제공하지만, 일반 디렉터리 마운트는 `..data` 링크 전환으로 새 파일을 읽는 반면 subPath 파일 바인드 마운트는 처음 연결한 파일에 고정됨. ConfigMap 원본 입력 파일과 Kubernetes 객체, kubelet이 제공하는 볼륨 파일은 구별해야 함.
- **정리:** `kubectl delete namespace lab-config-mount` 후 `kubectl get namespace lab-config-mount`에서 `NotFound` 확인. 로컬 Master VM의 입력·YAML 파일은 자동 삭제되지 않음.
- **미수행 추가 과제:** 존재하지 않는 ConfigMap key/path를 이용한 의도적 마운트 실패와 Events 진단은 별도로 재현하지 않음.
- **복습:** **2/2 완료**. ① `envFrom`은 기존 컨테이너에 변경 내용이 자동 반영되지 않아 Pod 재생성이 필요하고, 일반 ConfigMap 볼륨은 지연 갱신되어 파일을 다시 읽을 때 최신 값 확인 가능. ② `subPath`는 초기 파일 바인드 마운트에 고정되며, 일반 마운트는 kubelet의 `..data` 심볼릭 링크 전환을 따라간다는 원리 설명 완료.
