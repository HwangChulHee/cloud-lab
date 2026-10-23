# Lab 11 — Volume hostPath

> 학습 단계: **기초 개념·실습 과제**

## 강의 없이 시작하기

[독립 학습 가이드](../../08-independent/06-storage/README.md)에서 개념 설명 → 실행 YAML → 예상 결과 → 장애/복구 → 정리를 순서대로 진행한다. 이 문서는 해당 주제의 복습·추가 과제로 사용한다.

## 목표

Node 파일시스템과 Pod의 결합을 직접 확인한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. worker1에 두 Pod를 고정하고 같은 hostPath를 마운트한다.
2. Pod A에서 파일 생성 → Pod B → Node에서 확인한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. worker2를 선택하는 새 Pod를 만들어 동일 경로가 같은 데이터가 아님을 확인한다. 기존 Pod의 nodeName/nodeSelector를 수정해 이동시키지 않는다. worker1의 원본 Pod와 파일은 비교가 끝날 때까지 유지한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. hostPath가 Node 종속적인 이유를 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 실습 완료 기록 (2026-10-23)

- **실습 상태: ✅ 완료** (복습 문제 5개는 별도 진행·기록).
- `lab-hostpath` Namespace에 `pod-a`, `pod-b`를 Worker 1에, `pod-c`를 Worker 2에 생성했다. 모두 `/var/lib/lab-hostpath`를 `/data`로 마운트(`DirectoryOrCreate`).
- Pod A에서 `/data/message.txt` 생성 → 같은 Worker 1의 Pod B와 Node 실제 디렉터리에서 내용 일치 확인.
- Worker 2의 Pod C에서 `/data/message.txt`는 `No such file or directory`; `/data`는 비어 있음. 같은 경로 문자열이어도 다른 Node의 독립 파일시스템임을 확인.
- Pod A 삭제 후 같은 YAML로 Worker 1에 재생성: Pod IP가 `20.100.194.90` → `20.100.194.91`로 바뀌었지만 기존 파일 유지 확인.
- 중간 장애 대응: Worker 1이 `NotReady`, Master→Worker 1 통신 불가, Pod Pending 상태였음. VM running, Worker 1의 `eth1` IP 및 kubelet active 확인, Worker 1→Master/Worker 2 ping 성공, 이후 3개 Node Ready 및 Pod A/B Running 확인. 정확한 일시적 장애 원인은 특정하지 않음.
- 정리: `kubectl delete namespace lab-hostpath` 성공, Worker 1/2 각각 `/var/lib/lab-hostpath` 내용 확인 후 삭제. Master에는 해당 경로가 없었으며 Master의 `rm` 실패는 예상 가능한 동작. Namespace 삭제 뒤 `NotFound` 조회 검증은 별도로 진행하지 않았음.
- 결론: `hostPath`의 파일은 Pod가 아니라 **특정 Node의 디스크/경로**에 종속된다. 다른 Node로 데이터가 자동 복제되지 않는다.
