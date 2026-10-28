# Lab 12 — Static PV/PVC

> 학습 단계: **기초 개념·실습 과제**

## 강의 없이 시작하기

[독립 학습 가이드](../../08-independent/06-storage/README.md)에서 개념 설명 → 실행 YAML → 예상 결과 → 장애/복구 → 정리를 순서대로 진행한다. 이 문서는 해당 주제의 복습·추가 과제로 사용한다.

## 목표

Pod → PVC → PV → 실제 저장소 연결을 단계별로 확인한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. 서로 다른 capacity/accessMode의 PV를 만든다.
2. PVC가 어떤 PV와 Bound 되는지 확인한다.
3. PVC를 Pod에 마운트해 파일을 생성한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 기존 Bound PVC는 유지하고, 매칭 가능한 PV가 없는 조건의 새 PVC를 별도 이름으로 만들어 Pending을 재현한다. Bound PVC의 accessModes/storageClassName/volumeName을 제자리에서 바꾸는 실험은 하지 않는다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. PV/PVC 매칭 조건과 local PV의 nodeAffinity를 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 확장 실습

- [Retain PV로 데이터 복구하기](../../07-cka-preview/03-pv-data-recovery/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.

## 실습 완료 기록 (2026-10-28)

- **실습 상태: ✅ 완료**. 대화형 복습은 2문제로 별도 진행한다.
- 초기 `kubectl get pv`, `kubectl get storageclass`: 모두 자원 없음. Namespace `lab-static-pv` 생성.
- Worker 1의 `/var/lib/lab-static-pv` 준비, `lab-local-pv` 생성(1Gi, RWO, Retain, class `lab-static-local`, Local PV nodeAffinity Worker 1). `Available` 확인.
- `lab-local-pvc` 생성(500Mi 요청, volumeName 명시) 후 `lab-local-pv`와 `Bound` 확인. `pv-test-pod`는 nodeName 지정 없이 Worker 1(`20.100.194.93`)에 스케줄링. PVC 마운트 `/data/message.txt`에 `Hello from Local PV` 작성 및 Worker 1 디렉터리에서 동일 내용 확인.
- `oversized-pvc`(2Gi, volumeName 미지정)를 먼저 만들자 `Pending` 발생. `kubectl describe pvc`에서 존재하지 않는 StorageClass `lab-static-local` 관련 `ProvisioningFailed` 이벤트 확인. 기존 PV는 이미 Bound이며 용량도 1Gi라 매칭 대상이 아님.
- Worker 2 `/var/lib/lab-static-pv-2` 준비 및 `lab-local-pv-2` 생성(2Gi, RWO, Retain, 같은 class, nodeAffinity Worker 2). PVC 수정 없이 `oversized-pvc`가 자동 `Bound`됨을 확인. PV 생성 직후 조회에서는 `Available`, 다음 PVC 조회에서는 `Bound`로 관찰.
- `oversized-pvc` 삭제 후 `lab-local-pv-2`의 `Released` 확인. 이후 Pod 삭제 → 첫 PVC 삭제 → PV 둘 다 `Released` 확인 → PV 둘 다 삭제 및 `kubectl get pv` 자원 없음 확인 → Namespace 삭제.
- PV 삭제 후에도 Worker 1의 실제 `message.txt`가 남아 있음을 확인하고 Worker 1/Worker 2의 실습 디렉터리를 직접 삭제. Namespace 삭제 후 NotFound 별도 조회는 실시하지 않음.
- 학습 메모: `Bound`는 실제 볼륨 마운트를 뜻하지 않음. PV/PVC의 클래스 이름 일치는 정적 바인딩에 활용되며 StorageClass 객체 부재는 동적 프로비저닝 실패 이벤트를 유발할 수 있음. Local PV 데이터는 해당 Node에 종속됨.


## 복습 결과 (2026-10-28)

**압축 복습 2/2 정답 — 완료.**

1. **PV/PVC 바인딩과 마운트**: PVC A가 500Mi를 요청해 1Gi PV와 Bound되어도 PV 전체가 해당 PVC에 할당되므로 PVC B가 남은 용량을 별도로 요청해 같은 PV에 Bound될 수 없음을 정확히 설명. Bound 이후 Pod의 볼륨 마운트는 별도 과정임도 설명.
2. **Local PV 스케줄링 충돌과 복구**: PV nodeAffinity=Worker 1, Pod nodeSelector=Worker 2는 충돌해 Pending이 되며 Node 조건을 일치시켜 해결해야 함을 설명. Local PV는 Node 종속적이므로 Worker 1 장애 시 설정만으로 Worker 2에 데이터를 이전할 수 없음을 설명. 실제 디스크가 보존되었다면 별도 복구/복사는 가능함을 보충.

**다음 실습**: [11-configmap-secret-env](../11-configmap-secret-env/README.md).
