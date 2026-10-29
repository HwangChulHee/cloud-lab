# Lab 15 — Namespace Isolation

> 학습 단계: **기초 개념·실습 과제**

## 강의 없이 시작하기

[독립 학습 가이드](../../08-independent/01-pods/README.md)에서 개념 설명 → 실행 YAML → 예상 결과 → 장애/복구 → 정리를 순서대로 진행한다. 이 문서는 해당 주제의 복습·추가 과제로 사용한다.

## 목표

Namespace가 이름·Service 선택 범위를 어떻게 나누는지 확인한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. nm-1/nm-2에 같은 이름의 Pod와 Service를 만든다.
2. Service selector가 다른 namespace Pod를 잡지 못하는지 확인한다.
3. Pod IP 직접 통신과 동일 Node hostPath 공유 여부를 비교한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. namespace를 빼먹고 리소스를 생성해 예상하지 않은 위치에 생성되는 상황을 확인한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. Namespace로 격리되는 것과 격리되지 않는 것을 구분한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 확장 실습

- [최소 권한 NetworkPolicy](../../07-cka-preview/08-networkpolicy/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.

## 실습 기록 (2026-10-29)

- Namespace `nm-1`, `nm-2`를 YAML로 생성하여 두 Namespace 모두 `Active`이고 초기 Pod가 없음을 확인.
- 이름과 레이블이 동일한 `web-pod`를 두 Namespace에 생성하여 각각 `Running` 확인. 두 Pod는 k8s-worker1에 배치되었지만 IP는 각각 `20.100.194.100`, `20.100.194.101`.
- `nm-1`에만 `web-service`(ClusterIP `10.111.129.177`, `selector: app=web`)를 생성. EndpointSlice에 `20.100.194.100`만 포함됐고 `nm-2`에는 해당 Service의 EndpointSlice가 없음을 확인.
- `nm-2/web-pod`에서 `http://web-service.nm-1.svc.cluster.local`과 `http://20.100.194.100` 호출 모두 HTTP 200: Namespace만으로 Pod 네트워크 통신은 차단되지 않음.
- `nm-1`, `nm-2` 각각의 `hostpath-pod`를 동일한 `k8s-worker1`의 `/var/lib/lab-namespace-share`에 마운트. `nm-1`에서 쓴 `data.txt`의 `Hello from nm-1`을 `nm-2`에서 확인: Namespace는 동일 Node의 hostPath 파일을 격리하지 않음.
- YAML의 `metadata.namespace`를 생략한 `misplaced-pod`가 컨텍스트 기본 Namespace인 `default`에 생성됨을 확인. `nm-1` 조회는 NotFound, `kubectl get pods -A --field-selector metadata.name=misplaced-pod`로 위치 진단. `kubectl get pod misplaced-pod -A`는 이름 지정과 전체 Namespace 옵션의 충돌로 오류를 내므로 대체 명령 사용.
- **정리 검증:** `default/misplaced-pod` 및 `nm-1`, `nm-2` 삭제. Worker1의 `/var/lib/lab-namespace-share` 삭제 후 `hostPath cleaned` 확인. Namespace 두 개와 잘못 배치한 Pod에 대해 NotFound 확인.
- **범위 참고:** 두 Namespace에서 동일한 이름의 Service를 각각 생성하는 실험은 생략하고, 하나의 Service의 selector/EndpointSlice 범위를 검증했음.
- **복습:** **2/2 완료**. ① Service의 selector는 동일 Namespace의 Pod만 선택하지만 별도 NetworkPolicy 차단이 없으면 다른 Namespace에서도 Service를 호출할 수 있음을 설명. ② Namespace는 Kubernetes 리소스의 논리적 관리 범위만 분리하며, 같은 Worker Node의 동일 hostPath는 Namespace와 관계없이 공유된다는 점을 설명.
