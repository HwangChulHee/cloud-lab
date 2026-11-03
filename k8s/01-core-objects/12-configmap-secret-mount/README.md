# Lab 14 — ConfigMap & Secret Mount

> 학습 단계: **기초 개념·실습 과제**

## 강의 없이 시작하기

이 README가 공식 학습·실습 기록입니다. 아래의 개념 → 구성 → 관찰 → 장애/복구 → 정리 절차를 따라 진행합니다. [예전 독립 코스의 실행 자산](../../01-core-objects/12-configmap-secret-mount/README.md)은 보충 참고자료이며 별도 중복 이수 대상이 아닙니다.

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


## 독립 심화: ConfigMap 변경 전파, subPath, immutable

기존 환경변수/파일 마운트 실습 후 아래를 **추가 실습**으로 진행한다. 기존 완료 기록은 변경하지 않는다.

- 동일한 ConfigMap 키 `mode: blue`를 `env.valueFrom.configMapKeyRef`, 일반 ConfigMap volume, `subPath` 파일로 각각 주입한 실습 Pod를 생성한다.
- `kubectl patch configmap settings --type=merge -p '{"data":{"mode":"green"}}'`로 값을 변경한다. 일반 volume은 지연 후 바뀔 수 있지만 **환경변수와 subPath 마운트는 자동 반영되지 않는다**.
- Pod만 재생성해 신규 환경변수·subPath 값이 green인지 비교한다. ConfigMap 정의까지 재적용해 blue로 되돌리지 않도록 주의한다.
- `kubectl patch configmap settings --type=merge -p '{"immutable":true}'` 후 data 수정이 거부되는지 확인한다. immutable 객체의 data를 수정하려면 삭제·재생성이 필요하다.
- Secret은 Base64가 암호화가 아니며, Pod의 ServiceAccount에 Secret API `get` 권한이 없어도 kubelet이 참조된 Secret을 volume/env로 주입할 수 있다는 점을 설명한다.

실행용 참고 YAML은 이전 실습 자산 [configuration setup](../../01-core-objects/12-configmap-secret-mount/extended-setup.yaml), [configuration pod](../../01-core-objects/12-configmap-secret-mount/extended-pod.yaml)에 보존한다. 사용할 때는 `lab-self-config` namespace를 먼저 확인하고 다른 Lab의 리소스와 겹치지 않게 실행한다. 이 과제의 결과는 본 Lab의 확장 기록으로만 남긴다.


## 통합 확장 실습 — 환경변수·파일·subPath 비교

이 절은 이전 독립 8단계 과정의 고유 실습·장애 재현을 이 Lab에 합친 것이다. 별도의 8단계 진도를 만들지 않는다. `extended-*.yaml` 자산은 이 Lab에 보존되어 있으며 별도 `lab-self-*` Namespace를 생성하므로 기존 완료 실습을 덮어쓰지 않는다.

#### 따라 하기

```bash
kubectl apply -f k8s/01-core-objects/12-configmap-secret-mount/extended-setup.yaml
kubectl -n lab-self-config wait --for=condition=Ready pod/config-reader --timeout=120s
kubectl -n lab-self-config exec config-reader -- printenv MODE
kubectl -n lab-self-config exec config-reader -- cat /config/mode /fixed/mode
kubectl -n lab-self-config exec config-reader -- sh -c 'test -s /credentials/password && echo secret-file-present'
```

환경변수와 두 파일 모두 처음에는 `blue`다. Secret 파일이 있는지만 확인하고 원문을 학습 기록에 붙이지 않는다.

#### 변경 → 관찰 → 복구

```bash
kubectl -n lab-self-config patch cm settings --type=merge -p '{"data":{"mode":"green"}}'
kubectl -n lab-self-config exec config-reader -- cat /config/mode
kubectl -n lab-self-config exec config-reader -- cat /fixed/mode
kubectl -n lab-self-config exec config-reader -- printenv MODE
```

첫 파일만 시간이 지나 green으로 바뀔 수 있다. 즉시 바뀌지 않으면 잠시 후 다시 조회한다. subPath와 환경변수는 blue로 남는다. 이를 앱 재시작으로 해결하려고 독립 Pod를 삭제한 뒤 **Pod 파일만** 다시 apply한다. setup 전체를 apply하면 ConfigMap도 blue로 복구하므로 비교가 사라진다.

```bash
kubectl -n lab-self-config delete pod config-reader --wait=true
kubectl apply -f k8s/01-core-objects/12-configmap-secret-mount/extended-pod.yaml
kubectl -n lab-self-config wait --for=condition=Ready pod/config-reader --timeout=120s
kubectl -n lab-self-config exec config-reader -- printenv MODE
kubectl -n lab-self-config exec config-reader -- cat /fixed/mode
kubectl -n lab-self-config patch cm settings --type=merge -p '{"immutable":true}'
kubectl -n lab-self-config patch cm settings --type=merge -p '{"data":{"mode":"red"}}'
```

재생성 뒤 green을 예상하고, 마지막 변경은 immutable이라 거부된다. 이 객체를 원복하려면 삭제 후 새 객체가 필요하다. [TLS 설정 확장](../../07-cka-preview/01-configmap-tls/README.md)은 03의 rollout까지 익힌 뒤 진행한다.

#### 누적 복습 — 다음 단계 전에

앞 단계의 개념을 현재 증상에 다시 연결한다. 문서를 닫고 세 질문에 답하며, 어려운 질문은 실제 spec/status/Events를 근거로 다시 설명한다.

1. 환경 변수와 ConfigMap volume 변경이 다르게 보이는 이유는?
2. subPath가 변경 내용을 자동 반영하지 않는 이유는?
3. Secret을 참조한 Pod에 API read 권한이 반드시 필요한가?

관련 내부 심화를 할 경우 이 단계의 **namespace를 정리하기 전에** 진행한다. 개념만 읽을 때는 리소스 재생성을 강제하지 않는다.

#### 완료와 정리

환경변수, 일반 mount, subPath의 갱신 차이를 세 줄로 설명한다. Secret을 API로 직접 조회하는 권한과 Pod에 주입하는 경로를 구분한다. 일반 Secret volume/env 주입은 kubelet이 처리하므로 Pod의 ServiceAccount에 secrets get 권한을 추가할 필요가 없다. 반면 같은 namespace에서 Pod를 생성할 수 있는 사용자는 Secret을 마운트해 내용을 읽을 수 있으므로, Secret API 조회 권한만 제한해서 충분하다고 생각하지 않는다. [공식 Secret 설명](https://kubernetes.io/docs/concepts/configuration/secret/)을 참고한다.

```bash
kubectl delete namespace lab-self-config
```

다음: [03 Controller](../../02-controllers/08-controller-troubleshooting/README.md).

[독립 학습 순서](../../README.md)
