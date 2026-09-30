# 03. 원하는 상태·배포 전략·완료 작업을 구분하기

## 먼저 이해할 것

ReplicaSet은 개수를 맞추고, Deployment는 ReplicaSet을 교체해 배포한다. DaemonSet은 대상 노드마다 실행하며, Job은 성공 횟수를 채우고 CronJob은 일정에 맞춰 Job을 만든다. 같은 재시작 기능으로 묶지 않는다. YAML의 spec은 원하는 상태, status는 관측된 상태다.

## 따라 하기: 소유권과 복구

```bash
kubectl apply -f k8s/08-independent/03-controllers/setup.yaml
kubectl -n lab-self-control rollout status deploy/web --timeout=120s
kubectl -n lab-self-control get deploy,rs,pods,ds,job,cronjob
CONTROL_POD=$(kubectl -n lab-self-control get pod -l app=web -o jsonpath='{.items[0].metadata.name}')
kubectl -n lab-self-control get pod "$CONTROL_POD" -o jsonpath='{.metadata.ownerReferences}{"\n"}'
kubectl -n lab-self-control delete pod "$CONTROL_POD" --wait=true
kubectl -n lab-self-control get pods -l app=web --watch
```

Pod 소유자는 ReplicaSet이며 Deployment까지 연결된다. watch에서 삭제한 이름이 아닌 새 이름의 Pod가 생기고, 삭제 중인 Pod를 제외해 두 개 모두 1/1 Ready인지 확인한 뒤 Ctrl+C로 종료한다. 이 삭제는 Deployment template을 변경하지 않으므로 rollout status만으로 새 Pod 준비 완료를 판단하지 않는다.

## 변경 → 실패 → 복구: 롤링과 Recreate

```bash
kubectl -n lab-self-control set image deploy/web web=nginx:1.28-alpine-missing
kubectl -n lab-self-control get pods -l app=web
kubectl -n lab-self-control get events --sort-by=.lastTimestamp
kubectl -n lab-self-control rollout status deploy/web --timeout=30s
kubectl -n lab-self-control rollout history deploy/web
kubectl -n lab-self-control rollout undo deploy/web
kubectl -n lab-self-control rollout status deploy/web --timeout=120s
kubectl -n lab-self-control patch deploy web --type=merge -p '{"spec":{"strategy":{"type":"Recreate","rollingUpdate":null}}}'
kubectl -n lab-self-control set image deploy/web web=nginx:1.27-alpine
kubectl -n lab-self-control rollout status deploy/web --timeout=120s
```

존재하지 않는 태그는 ImagePullBackOff가 예상된다. rollout status의 timeout도 예상한 실패다. rolling은 이전 Pod가 남을 수 있고 Recreate는 먼저 이전 Pod를 내린다. 별도 셸의 `kubectl -n lab-self-control get pods -w`로 비교하고 Ctrl+C로 종료한다. template을 변경하는 이유와 Ready가 가용성에 필요한 이유를 설명한다.

## Blue/Green: 트래픽 대상 변경

```bash
kubectl -n lab-self-control rollout status deploy/blue --timeout=120s
kubectl -n lab-self-control rollout status deploy/green --timeout=120s
kubectl -n lab-self-control run client --image=busybox:1.37 --restart=Never -- sleep 3600
kubectl -n lab-self-control wait --for=condition=Ready pod/client --timeout=120s
wait_color() {
  local expected="$1" attempt body
  for attempt in $(seq 1 30); do
    body=$(kubectl -n lab-self-control exec client -- wget -T 2 -qO- http://color) || body=""
    if [ "$body" = "$expected" ]; then printf '%s\n' "$body"; return 0; fi
    sleep 2
  done
  echo "color 응답이 $expected 로 바뀌지 않았습니다. EndpointSlice/Pod를 확인하세요." >&2
  return 1
}
wait_color blue
kubectl -n lab-self-control patch svc color --type=merge -p '{"spec":{"selector":{"app":"green"}}}'
wait_color green
```

green을 출력한 것을 확인한 뒤에만 blue로 복구한다. timeout이면 먼저 `kubectl -n lab-self-control get endpointslices -l kubernetes.io/service-name=color -o yaml`로 전달 대상을 확인한다.

```bash
kubectl -n lab-self-control patch svc color --type=merge -p '{"spec":{"selector":{"app":"blue"}}}'
wait_color blue
unset -f wait_color
```

blue → green → blue가 각각 새 연결에서 관찰된다. 반영 지연 시 EndpointSlice가 바뀌었는지 확인하고 재요청한다. 두 Deployment가 살아 있고 Service selector만 바뀐 것이다.

## DaemonSet·Job·CronJob 관찰

```bash
kubectl -n lab-self-control get ds agent -o wide
kubectl -n lab-self-control get pods -l app=agent -o wide
kubectl -n lab-self-control wait --for=condition=Complete job/batch --timeout=120s
kubectl -n lab-self-control get job batch
kubectl -n lab-self-control create job manual-clock --from=cronjob/clock
kubectl -n lab-self-control wait --for=condition=Complete job/manual-clock --timeout=120s
kubectl -n lab-self-control logs job/manual-clock
kubectl -n lab-self-control get jobs -o 'custom-columns=NAME:.metadata.name,OWNER:.metadata.ownerReferences[0].name' --watch
```

Job COMPLETIONS는 3/3이다. DaemonSet DESIRED는 보통 worker 2개이며 실제 taint/배치 조건에 따라 달라진다. watch에서 NAME이 clock-숫자 형태이고 OWNER가 clock인 자동 Job을 확인할 때까지 기다린다(분 경계와 Controller 처리 시간이 필요하다). manual-clock도 OWNER가 clock일 수 있으므로 그 행을 제외한다. manual-clock의 성공만으로 예약 실행을 확인했다고 판단하지 않는다. 자동 Job을 확인한 뒤 Ctrl+C로 watch를 종료하고 다음을 실행한다.

```bash
kubectl -n lab-self-control patch cronjob clock --type=merge -p '{"spec":{"suspend":true}}'
```

suspend는 이미 시작한 Job을 중단하지 않는다.

## 완료와 정리

독립 Pod와 Deployment의 삭제 후 차이, rollback이 ConfigMap/DB까지 되돌리지 않는 이유, Job 성공 수와 총 Pod 수의 차이를 설명한다.

```bash
kubectl delete namespace lab-self-control
```

다음: [04 Service/DNS](../04-networking/README.md).

[독립 학습 순서](../README.md)
