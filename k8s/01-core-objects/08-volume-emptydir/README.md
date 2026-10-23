# Lab 10 — Volume emptyDir

> 학습 단계: **기초 개념·실습 과제**  
> **실습 상태: ✅ 완료 (2026-10-23)**

## 강의 없이 시작하기

[독립 학습 가이드](../../08-independent/01-pods/README.md)에서 개념 설명 → 실행 YAML → 예상 결과 → 장애/복구 → 정리를 순서대로 진행한다. 이 문서는 해당 주제의 복습·추가 과제로 사용한다.

## 목표

Pod 생명주기에 묶인 공유 볼륨을 확인한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. 두 Container가 같은 emptyDir를 서로 다른 mountPath에 마운트한다.
2. Container1에서 파일을 만들고 Container2에서 확인한다.
3. Pod 삭제 후 재생성하여 데이터 소멸을 확인한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 공유 볼륨 없이 같은 경로에 파일을 만들고 서로 보이지 않는 것을 비교한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. emptyDir의 생명주기를 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 확장 실습

- [파일 로그를 Sidecar로 stdout에 보내기](../../07-cka-preview/10-sidecar-logging/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.

## 실습 완료 기록 (2026-10-23)

- [x] `lab-emptydir` namespace 생성 및 Active 확인; 클러스터 3노드 Ready 확인.
- [x] `k8s-worker1`에 `shared-pod`(writer, reader 두 컨테이너) 2/2 Running, Pod IP `20.100.194.87` 확인.
- [x] 하나의 `emptyDir`인 `shared-data`를 writer의 `/data/shared`, reader의 `/shared`로 마운트하고 `message.txt` 내용 `Hello from writer`가 양측에서 읽히는 것 확인.
- [x] writer의 볼륨 외부 `/tmp/private.txt`에 `Private file` 작성 후 reader의 동일 경로에서는 파일이 존재하지 않음을 확인.
- [x] 컨테이너 내부 PID 1에 대한 `kill -9 1` 이후 재시작은 발생하지 않아, Worker 1의 `crictl --runtime-endpoint unix:///run/containerd/containerd.sock stop`으로 writer만 중지. kubelet이 writer를 새 Container ID로 재시작(ATTEMPT 1, Pod `RESTARTS=1`), Pod IP 및 Node 유지 확인.
- [x] writer 컨테이너 재시작 후 두 컨테이너에서 공유 `message.txt` 유지 확인; writer 컨테이너 자체 `/tmp/private.txt`는 사라짐.
- [x] 기존 Pod 삭제 후 동일 YAML로 Worker 1에 재생성(`20.100.194.88`, 2/2 Running); 이전 `message.txt`가 존재하지 않음을 확인.
- [x] `lab-emptydir` namespace 삭제 후 `NotFound`로 정리 완료 검증.

> 핵심 결론: `emptyDir`는 컨테이너 재시작보다 오래 유지되지만 Pod의 생명주기에는 종속된다. 별도 복습 문답은 이후 추가한다.

## 복습 완료 기록 (2026-10-23)

- [x] 문제 1: `emptyDir`는 컨테이너가 아닌 Pod 생명주기에 종속됨을 설명.
- [x] 문제 2: 같은 emptyDir에 대한 서로 다른 mountPath와 컨테이너 자체 `/tmp` 파일 격리를 설명.
- [x] 문제 3: Worker Node 장애 후 다른 Node에 새로 생성된 Pod는 이전 emptyDir 데이터에 접근할 수 없음을 설명.
- [x] 문제 4: 애플리케이션·Sidecar의 공유 emptyDir 마운트 구조를 설명. `volumes`는 Pod spec에 한 번 정의하고 `volumeMounts`는 각 컨테이너에 둔다는 점, 파일보다 디렉터리를 mountPath로 지정하는 것을 보완.
- [x] 문제 5: DB 컨테이너 재시작 시 emptyDir 유지, Pod 삭제·재생성 시 소멸, 영속 데이터에 PV/PVC 사용 필요성을 설명.

**복습 결과: 5/5 정답.** 실습 완료 수치는 변경하지 않음.
