# Lab 03 — Pod Multi-Container

> 학습 단계: **기초 개념·실습 과제**

## 강의 없이 시작하기

이 README가 공식 학습·실습 기록입니다. 아래의 개념 → 구성 → 관찰 → 장애/복구 → 정리 절차를 따라 진행합니다. [예전 독립 코스의 실행 자산](../../01-core-objects/01-pod-multicontainer/README.md)은 보충 참고자료이며 별도 중복 이수 대상이 아닙니다.

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

[독립 학습 순서](../../README.md)


## 내부 동작 심화 통합 — 01-pod-creation-pipeline

기존 INT 모듈의 개념·관찰·원인 분석 내용을 이 Lab에 병합했다. 코드 블록에 등장하는 `lab-self-*`는 이전 독립 예제의 실습용 Namespace이며, 현재 Lab의 리소스를 우선 사용하거나 해당 확장 YAML을 적용한 뒤 관찰한다. 별도 INT 진도는 만들지 않는다.

#### 선수 개념과 내부 동작

Pod 생성은 단일 호출이 아니다. kubectl은 API Server에 객체를 제출한다. API Server는 인증·인가·Admission 이후 etcd에 원하는 상태를 저장한다. 독립 Pod라면 Deployment/ReplicaSet 컨트롤러를 거치지 않는다. scheduler는 nodeName이 없는 Pod를 watch하고 Filter/Score 후 Binding한다. 해당 Node의 kubelet이 Pod spec을 수신해 CRI의 RunPodSandbox/CreateContainer/StartContainer 등을 통해 실행한다. CNI는 보통 Sandbox 네트워크 구성에 관여하며 kubelet이 status를 갱신한다. Running과 Ready는 다르다.

#### 시작 전 상태와 예측

1. `kubectl config current-context`, `kubectl version`, `kubectl get nodes -o wide`로 대상 클러스터를 확인한다.
2. [독립 학습](../../README.md)의 01-pods 단계를 완료하고 대상 namespace/객체가 존재하는지 확인한다. 이전 실습에서 cleanup했다면 먼저 다시 생성한다.
3. 명령 실행 전에 예상할 객체 상태, Node 구성, 관련 컴포넌트 및 실패 시 증거를 기록한다.

#### 예시: Pod 생성은 왜 여러 컴포넌트를 거칠까?

가상의 `frontend` Pod를 생성한다고 하자. 처음에는 Pod가 API에 저장되지만 `spec.nodeName`이 없다. **API Server**는 요청 인증·인가·Admission과 저장을 처리하고 컨테이너를 직접 만들지 않는다. **Scheduler**가 조건에 맞는 `worker1`을 선택하여 Binding하면 `spec.nodeName=worker1`이 된다. **worker1의 kubelet**은 API에서 할당된 Pod를 관찰하고 CRI를 통해 Pod Sandbox와 컨테이너 실행을 요청한다. 런타임 및 CNI 설정 후 `status.phase=Running`이 될 수 있지만 readiness가 실패하면 `Ready=False`다.

| 관찰값(예시) | 어디까지 진행됐는가? | 다음 확인 |
|---|---|---|
| `nodeName: <empty>`, `PodScheduled=False` | 아직 배치 전 | Events/스케줄링 조건 |
| `nodeName: worker1`, `ImagePullBackOff` | 배치 완료, 실행 준비 실패 | kubelet/Image Pull Events |
| `Running`, `Ready=False` | 실행 중이지만 요청 받을 준비 미완료 | readiness/컨테이너 로그 |

같은 증상인 `Ready=False`라도 실제 병목 단계는 다를 수 있다.

#### 관찰 명령

아래는 kubeconfig가 준비된 Linux/bash 셸 기준이다. `sudo`가 필요한 명령은 해당 Node의 호스트 셸에서 실행한다. 해당 객체가 없으면 먼저 선수 실습을 수행한다.

```bash
kubectl get nodes -o wide
kubectl -n lab-self-pods get pod pair -o wide
kubectl -n lab-self-pods get pod pair -o jsonpath='{.metadata.uid}{"\n"}{.spec.nodeName}{"\n"}{.status.phase}{"\n"}'
kubectl -n lab-self-pods describe pod pair
kubectl -n lab-self-pods get events --sort-by=.lastTimestamp
```

#### 따라 하기 — 순서와 예상 결과

기존 01-pods를 먼저 apply하고 Ready까지 확인한다. Node 이름을 기록한 후 해당 Node의 호스트 셸에서 sudo crictl pods와 sudo crictl ps로 Pod Sandbox와 컨테이너를 확인한다. kubelet 로그는 sudo journalctl -u kubelet -n 100 --no-pager로 조사한다. crictl의 Pod ID와 Kubernetes Pod UID는 같은 값이 아닐 수 있다.

**관찰 기록:** 실행 전 예상 → 실제 spec/status/Events 또는 Linux 상태 → 예상과 다른 이유. 단순히 명령이 오류 없이 종료됐다는 이유로 정상 동작을 확인했다고 처리하지 않는다.

#### 고장 가설과 복구

이미지가 존재하지 않을 때 Pod는 스케줄되었어도 시작에 실패한다. describe의 Failed/Pulling/BackOff와 containerStatuses[*].state.waiting.reason을 찾아 image pull 문제와 scheduling 문제를 구분한다. 잘못된 이미지는 기존 03 Controller 실습의 실패 사례를 재사용한다.

복구 뒤에는 동일 조건의 조회/요청으로 다시 확인한다. 관찰할 수 없는 구현은 검증 완료로 표시하지 않는다.

#### 다음에 다시 확인하기

설명을 가리고 핵심 질문에 답한 뒤, 위에서 제시한 예상 상태를 자신의 말로 해석한다. 정답 대신 기존 실습의 실제 상태·Events를 근거로 제시한다.

#### 환경 및 정리

이 모듈의 관련 리소스는 기본 단계의 Cleanup 전에 관찰한다. 이전 단계가 정리됐다면 Setup부터 다시 실행한다. 위험한 제어 평면/호스트 변경은 별도 VM에서만 수행한다.

#### 공식 참고

- [이 주제의 공식 Kubernetes 문서](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)
- [Kubernetes 디버깅](https://kubernetes.io/docs/tasks/debug/)

[Kubernetes 공식 커리큘럼](../../README.md)
