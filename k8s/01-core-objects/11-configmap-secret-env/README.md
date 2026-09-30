# Lab 13 — ConfigMap & Secret Env

> 학습 단계: **기초 개념·실습 과제**

## 목표

설정과 민감 값을 환경변수로 주입하는 흐름을 비교한다.

## 핵심 개념과 오해 방지

ConfigMap의 `data`는 문자열이다. YAML의 true/false나 숫자를 값으로 쓸 때 문자열로 표시한다. Secret의 `data`는 Base64 표현이며 `stringData`에는 문자열을 넣을 수 있다. Base64는 암호화가 아니고, Secret을 읽을 권한이 있는 주체는 원문도 얻을 수 있다. Secret이라고 etcd 저장 암호화가 자동 보장되지는 않는다.

ConfigMap 데이터는 1MiB를 넘길 수 없고 개별 Secret도 1MiB 제한이 있다. 큰 파일이나 로그 저장소로 사용하지 않는다. `--from-file=APP_CONFIG=./config.txt`의 APP_CONFIG는 객체 key다. `env[].name`은 실제 환경변수 이름, keyRef.key는 가져올 key이며 서로 달라도 된다. 파일 확장자가 자동 제거된다고 가정하지 말고 명시적으로 매핑한다. 1.27에서 envFrom의 유효하지 않은 환경변수 key는 건너뛰어질 수 있으므로 Events도 본다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. literal ConfigMap/Secret을 만든다.
2. envFrom/valueFrom으로 Pod에 주입하고 `env`로 확인한다.
3. 값을 변경한 뒤 기존 Pod env가 그대로인지 확인한다.
4. Pod 재생성 후 새 값 반영을 확인한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 존재하지 않는 key를 참조해 Pod 생성 상태/이벤트를 확인한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. Env 주입 시 업데이트 반영 방식과 Secret의 Base64 표현을 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.
