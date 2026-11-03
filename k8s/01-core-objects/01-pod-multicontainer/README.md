# Lab 03 — Pod Multi-Container

> 학습 단계: **기초 개념·실습 과제**

## 강의 없이 시작하기

이 README가 공식 학습·실습 기록입니다. 아래의 개념 → 구성 → 관찰 → 장애/복구 → 정리 절차를 따라 진행합니다. [예전 독립 코스의 실행 자산](../../08-independent/01-pods/README.md)은 보충 참고자료이며 별도 중복 이수 대상이 아닙니다.

## 목표

한 Pod 안의 여러 Container가 네트워크를 공유하는 방식을 확인한다.

## 핵심 개념과 오해 방지

같은 Pod의 컨테이너는 Pod IP와 포트 공간을 공유한다. `containerPort` 숫자를 선언하는 것만으로 포트 충돌이 나는 것은 아니고, 실제 프로세스 둘이 같은 주소/프로토콜/포트에 listen할 때 충돌한다. 파일시스템은 기본적으로 분리되므로 파일 공유에는 volume이 필요하다. 독립 Pod를 삭제하면 Controller가 다시 만들어주지 않으며, 재생성된 Pod IP는 이전과 같을 수도 있어 IP 변경 자체만을 성공 조건으로 삼지 않는다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. 포트 8000/8080 컨테이너를 가진 Pod를 만든다.
2. Pod IP로 각 포트를 호출한다.
3. 컨테이너 내부에서 `localhost`로 다른 컨테이너를 호출한다.
4. Pod 재생성 후 IP 변화를 확인한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 같은 포트를 사용하는 컨테이너 구성으로 충돌을 재현한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. Pod IP, Container port, localhost 관계를 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 확장 실습

- [파일 로그를 Sidecar로 stdout에 보내기](../../07-cka-preview/10-sidecar-logging/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.


## 통합 확장 실습 — 따라 하는 Pod 통합 관찰

이 절은 이전 독립 8단계 과정의 고유 실습·장애 재현을 이 Lab에 합친 것이다. 별도의 8단계 진도를 만들지 않는다. `extended-*.yaml` 자산은 이 Lab에 보존되어 있으며 별도 `lab-self-*` Namespace를 생성하므로 기존 완료 실습을 덮어쓰지 않는다.

#### 따라 하기

```bash
kubectl apply -f k8s/01-core-objects/01-pod-multicontainer/extended-setup.yaml
kubectl -n lab-self-pods wait --for=condition=Ready pod/pair --timeout=120s
kubectl -n lab-self-pods get pod pair -o wide --show-labels
kubectl -n lab-self-pods get pods -l tier=frontend
kubectl -n lab-self-pods exec pair -c observer -- wget -qO- http://127.0.0.1
kubectl -n lab-self-pods exec pair -c observer -- sh -c 'echo shared-ok > /shared/note'
kubectl -n lab-self-pods exec pair -c web -- cat /shared/note
kubectl -n lab-self-pods logs pair -c prepare
kubectl -n lab-self-pods exec pair -c observer -- cat /shared/init
kubectl -n lab-self-pods logs pair -c web --tail=5
kubectl -n lab-self-pods describe pod pair
```

`READY 2/2`, nginx의 환영 HTML, `shared-ok`를 예상한다. observer가 localhost로 web에 접속한 이유와, 다른 Pod에서는 localhost가 다른 대상인 이유를 설명한다. nginx 요청 로그가 stdout에 나타나는 것도 본다. prepare init container가 먼저 성공한 뒤 두 앱 컨테이너가 시작되고 init-ok 파일을 읽는지 확인한다. 일반 init과 계속 실행하는 Sidecar의 종료 조건은 다르다.

#### 변경 → 실패 → 복구

```bash
kubectl -n lab-self-pods label pod pair tier=backend --overwrite
kubectl -n lab-self-pods get pods -l tier=frontend
kubectl -n lab-self-pods get pods -l tier=backend
kubectl -n lab-self-pods label pod pair tier=frontend --overwrite
kubectl -n lab-self-pods exec pair -c observer -- sh -c 'echo private > /tmp/private'
kubectl -n lab-self-pods exec pair -c web -- cat /tmp/private
```

frontend 조회는 비고 backend 조회에 pair가 나타난다. 마지막 cat은 파일 없음으로 실패한다. `/tmp`가 자동 공유되지 않기 때문이다. `get pods`가 전체 Pod를 보여주는지 namespace 없이 실행한 결과와 비교한다.

```bash
kubectl -n lab-self-pods get pod pair -o jsonpath='{.metadata.uid}{"\n"}'
kubectl -n lab-self-pods delete pod pair --wait=true
kubectl -n lab-self-pods get pods
kubectl apply -f k8s/01-core-objects/01-pod-multicontainer/extended-setup.yaml
kubectl -n lab-self-pods wait --for=condition=Ready pod/pair --timeout=120s
kubectl -n lab-self-pods get pod pair -o jsonpath='{.metadata.uid}{"\n"}'
kubectl -n lab-self-pods exec pair -c web -- cat /shared/note
```

Controller가 없는 독립 Pod는 삭제 후 스스로 돌아오지 않는다. 재생성 뒤 UID가 바뀌고 emptyDir 파일이 사라진다. Pod IP가 반드시 달라져야 하는 것은 아니다.

#### 누적 복습 — 다음 단계 전에

앞 단계의 개념을 현재 증상에 다시 연결한다. 문서를 닫고 세 질문에 답하며, 어려운 질문은 실제 spec/status/Events를 근거로 다시 설명한다.

1. Pod 삭제 후 Controller가 없다면 복구되나?
2. Pod IP와 localhost가 다른 이유는?
3. PodScheduled와 Ready는 무엇이 다른가?

관련 내부 심화를 할 경우 이 단계의 **namespace를 정리하기 전에** 진행한다. 개념만 읽을 때는 리소스 재생성을 강제하지 않는다.

#### 완료와 정리

label 변경은 프로세스를 멈추는가? 컨테이너 재시작과 Pod 삭제 중 어느 것이 emptyDir 수명을 끝내는가? 예상과 실제 결과를 기록한다. 파일 없음은 이번 단계의 예상한 실패다.

```bash
kubectl delete namespace lab-self-pods
```

다음: [02 설정 주입](../12-configmap-secret-mount/README.md). 더 연습하려면 [기초 02 관찰](../../00-foundation/02-kubectl-observation-basics/README.md), [Sidecar 로그](../../07-cka-preview/10-sidecar-logging/README.md)를 순서대로 실행한다. Sidecar 예제는 Deployment를 쓰므로 먼저 03의 Controller 설명을 읽어도 된다.

[독립 학습 순서](../../08-independent/README.md)
