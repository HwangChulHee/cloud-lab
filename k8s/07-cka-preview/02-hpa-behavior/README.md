# 02. HPA와 축소 안정화 시간

> 강의 전 예습 · 참고 주제: task-hpa · 환경: 기존 클러스터 + 정상 Metrics Server

기초 연결: [HPA](../../05-advanced/04-hpa/README.md) · [기초 자원 설정](../../01-core-objects/03-node-scheduling-resources/README.md)

## 먼저 이해할 것

HPA의 CPU 사용률은 CPU requests를 기준으로 계산한다. `limits` 대비 비율이 아니다. 안정화 시간은 최근 추천값을 고려해 잦은 축소를 줄이며, 정확히 30초 뒤 Pod를 삭제하는 타이머는 아니다.

## 1. 구축하고 관찰하기

저장소 루트에서 `cd k8s/07-cka-preview/02-hpa-behavior`로 이동한 뒤 실행한다. 명령은 kubectl이 설정된 Linux 셸 기준이다.

```bash
kubectl top nodes
kubectl get apiservice v1beta1.metrics.k8s.io
kubectl apply -f setup.yaml
kubectl -n preview-hpa rollout status deploy/web --timeout=120s
kubectl -n preview-hpa top pods
```

metrics가 없으면 기존 HPA 기초 실습에서 Metrics Server부터 준비한다. APIService가 Available인데도 `<unknown>`이면 Pod metrics가 수집될 때까지 기다리고 HPA Conditions를 확인한다.

## 2. 직접 바꿔보기

CPU 목표 50%, 최소 1개·최대 4개, scaleDown 안정화 시간 30초인 HPA를 만든다. 다음으로 부하를 발생시켜 확장과 축소를 관찰한다.

```bash
kubectl -n preview-hpa run load --image=busybox:1.37 --restart=Never -- \
  sh -c 'while true; do wget -q -O- http://web >/dev/null; done'
kubectl -n preview-hpa get hpa web -w
```

별도 셸에서 `kubectl -n preview-hpa get pods -w`로 Pod 수를 관찰한다. watch는 리소스 종류 하나씩 실행한다. load Pod를 삭제해 축소를 관찰한다. 부하가 부족하면 load Pod를 추가한다. 마지막으로 CPU request와 CPU limit을 모두 지웠을 때 HPA가 무엇을 보고하는지 확인한다. request만 지우고 limit을 남기면 새 Pod의 request가 limit 값으로 자동 설정되므로 누락 장애가 재현되지 않는다. namespace의 LimitRange가 CPU 기본값을 주입하는지도 확인한다.

먼저 예상 결과를 적고 시도한다. 막히면 `get → describe → events → logs`에서 필요한 도구를 고른다. 아래 풀이를 보기 전에 관찰 결과와 추측을 남긴다.

## 3. 검증하기

```bash
kubectl -n preview-hpa describe hpa web
kubectl -n preview-hpa top pods
kubectl -n preview-hpa get hpa web -o yaml
```

목표값, min/max, behavior, metrics와 Conditions를 확인한다. 부하 전후 desired/current replicas가 달라지는지 기록한다.

<details>
<summary>막힐 때 보는 힌트와 예시 풀이</summary>

```bash
kubectl apply -f solution.yaml
kubectl -n preview-hpa delete pod load --ignore-not-found
kubectl -n preview-hpa patch deploy web --type=json \
  -p='[{"op":"remove","path":"/spec/template/spec/containers/0/resources/requests/cpu"},{"op":"remove","path":"/spec/template/spec/containers/0/resources/limits/cpu"}]'
kubectl -n preview-hpa rollout status deploy/web --timeout=120s
kubectl -n preview-hpa get pods -o yaml
kubectl -n preview-hpa describe hpa web
```

새 Pod에서 CPU request가 실제로 없는지 확인한다. HPA가 새 metrics를 수집한 뒤 CPU request 누락을 Conditions/Events에 보고하는지 확인한다. request가 없으면 utilization 계산이 불가능해진다. 복구는 `kubectl apply -f setup.yaml`이다. HPA가 동작하는 동안 Deployment replicas를 반복해서 덮어쓰지 않는다.

</details>

## 4. 정리 및 재실행

```bash
kubectl delete namespace preview-hpa
```

## 강의에서 확인할 질문

- CPU 100m request에 사용량 50m이면 사용률은 얼마인가?
- Metrics 미수집과 CPU request 누락은 어떤 진단 결과로 구분하는가?

[전체 예습 경로](../README.md)
