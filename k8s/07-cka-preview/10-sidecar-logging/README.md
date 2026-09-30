# 10. 파일 로그를 Sidecar로 stdout에 보내기

> 독립 실행 가능한 확장 실습 · 참고 주제: task-sidecar · 환경: 기존 클러스터

기초 연결: [멀티 컨테이너 Pod](../../01-core-objects/01-pod-multicontainer/README.md) · [emptyDir](../../01-core-objects/08-volume-emptydir/README.md)

[독립 과정에서의 위치](../../08-independent/03-controllers/README.md). 처음에는 예시 풀이를 참고해 구축하고, 두 번째에는 요구사항만 보고 실행한다. 강의 수강은 선행 조건이 아니다.

## 먼저 이해할 것

kubectl logs는 컨테이너 stdout/stderr를 보여준다. 애플리케이션이 파일로만 쓰는 로그는 자동으로 나타나지 않는다. 같은 Pod의 두 컨테이너가 emptyDir를 공유하고 Sidecar가 파일을 tail해 stdout으로 내보내게 한다. 기존 1.27에서도 가능한 일반 containers 방식이다.

## 1. 구축하고 관찰하기

저장소 루트에서 `cd k8s/07-cka-preview/10-sidecar-logging`로 이동한 뒤 실행한다. 명령은 kubectl이 설정된 Linux 셸 기준이다.

```bash
kubectl apply -f setup.yaml
kubectl -n preview-logging rollout status deploy/legacy --timeout=120s
kubectl -n preview-logging exec deploy/legacy -- cat /var/log/legacy.log
kubectl -n preview-logging logs deploy/legacy
```

파일에는 로그가 있지만 kubectl logs에는 날짜 출력이 없는 차이를 확인한다.

## 2. 직접 바꿔보기

1. 기존 메인 컨테이너의 실행 명령은 유지한다.
2. 공유 emptyDir와 양쪽 `/var/log` 마운트를 추가한다.
3. Sidecar가 파일을 따라가 stdout에 출력하게 한다.
4. Sidecar의 mountPath만 틀리게 바꿔 파일 공유 실패를 진단한다.

먼저 예상 결과를 적고 시도한다. 막히면 `get → describe → events → logs`에서 필요한 도구를 고른다. 아래 풀이를 보기 전에 관찰 결과와 추측을 남긴다.

## 3. 검증하기

```bash
kubectl -n preview-logging rollout status deploy/legacy --timeout=120s
kubectl -n preview-logging logs deploy/legacy -c sidecar --tail=5
kubectl -n preview-logging exec deploy/legacy -c legacy -- tail /var/log/legacy.log
```

두 컨테이너에서 같은 날짜 로그를 확인한다. Pod 재생성 후 emptyDir 내용이 새로 시작하는 것도 확인한다.

<details>
<summary>막힐 때 보는 힌트와 예시 풀이</summary>

```bash
kubectl apply -f solution.yaml
kubectl -n preview-logging rollout status deploy/legacy --timeout=120s
```

메인과 Sidecar 시작 순서는 보장되지 않으므로 파일이 생성될 때까지 기다리는 짧은 루프를 넣었다. emptyDir는 컨테이너 재시작에는 유지되지만 Pod 삭제에는 유지되지 않는다.

</details>

## 4. 정리 및 재실행

```bash
kubectl delete namespace preview-logging
```

## 스스로 설명할 질문

- 같은 Pod라고 파일시스템까지 자동 공유되는가?
- 로그 보존이 필요하면 emptyDir 외에 어떤 요소가 필요한가?

[전체 확장 경로](../README.md)
