# 05. 자원·Probe·스케줄링 실패를 구분하기

## 먼저 이해할 것

requests는 배치 계산, limits는 실행 중 제한에 쓰인다. readiness는 트래픽 수신 가능 여부, liveness는 컨테이너 복구, startup은 기동 완료 여부다. nodeAffinity는 노드 조건, podAntiAffinity는 다른 Pod와 떨어질 범위다. toleration은 노드의 거부 조건을 허용할 뿐 그 노드를 선택하지는 않는다.

## 따라 하기

worker의 실제 hostname label 값을 고른다. 기본 환경은 worker 두 개이며, spread는 서로 다른 노드에 배치돼야 한다.

```bash
kubectl get nodes -L kubernetes.io/hostname
PLACEMENT_WORKER=REPLACE_WORKER_HOSTNAME
sed "s/REPLACE_WORKER_HOSTNAME/$PLACEMENT_WORKER/" k8s/08-independent/05-resources-scheduling/setup.yaml > /tmp/lab-self-placement.yaml
kubectl apply -f /tmp/lab-self-placement.yaml
kubectl -n lab-self-placement rollout status deploy/health --timeout=120s
kubectl -n lab-self-placement rollout status deploy/place --timeout=120s
kubectl -n lab-self-placement rollout status deploy/spread --timeout=120s
kubectl -n lab-self-placement rollout status deploy/near --timeout=120s
kubectl -n lab-self-placement get pods -o wide
kubectl -n lab-self-placement get pod best burst guaranteed -o custom-columns=NAME:.metadata.name,QOS:.status.qosClass
```

BestEffort, Burstable, Guaranteed와 spread의 서로 다른 nodeName을 예상한다. near는 place와 같은 노드에 배치되는 positive affinity를 비교한다. 노드 한 개만 쓸 수 있는 환경에서는 spread 한 개가 Pending인 것이 예상 결과다. 과목 완료를 위해서는 두 worker 환경을 준비하거나 그 환경 제약을 해결한다.

## phase와 표시 상태를 나눠 보기

```bash
kubectl -n lab-self-placement get pod finished crash
kubectl -n lab-self-placement get pod finished crash -o custom-columns=NAME:.metadata.name,PHASE:.status.phase
kubectl -n lab-self-placement logs finished
kubectl -n lab-self-placement describe pod crash
kubectl -n lab-self-placement delete pod crash --wait=true
kubectl -n lab-self-placement run crash --image=busybox:1.37 --restart=Never -- sleep 3600
kubectl -n lab-self-placement wait --for=condition=Ready pod/crash --timeout=120s
```

finished는 Completed 표시와 Succeeded phase, crash는 반복 실패 뒤 CrashLoopBackOff 표시와 컨테이너 waiting reason을 비교한다. CrashLoopBackOff를 별도 Pod phase로 외우지 않는다. 복구한 crash는 새 UID이며 Running이다.

## LimitRange 기본값과 거부 확인

QoS 초기 비교를 먼저 끝내고 다음을 실행한다.

```bash
kubectl apply -f k8s/08-independent/05-resources-scheduling/limits.yaml
kubectl -n lab-self-placement get pod best -o jsonpath='{.status.qosClass}{"\n"}'
kubectl -n lab-self-placement run defaulted --image=busybox:1.37 --restart=Never -- sleep 3600
kubectl -n lab-self-placement get pod defaulted -o yaml
kubectl apply -f k8s/08-independent/05-resources-scheduling/over.yaml
```

기존 best는 BestEffort로 남고 새 defaulted에는 request/limit 기본값이 채워진다. 마지막 Pod는 CPU max 300m을 넘겨 생성이 거부된다. 실제 Pod가 없으므로 scheduler Pending 장애와 다르다. 나머지 단계의 sleep/nginx Pod는 허용 범위 안의 자원을 사용한다.

## Probe 실패와 복구

```bash
HEALTH_POD=$(kubectl -n lab-self-placement get pod -l app=health -o jsonpath='{.items[0].metadata.name}')
kubectl -n lab-self-placement exec "$HEALTH_POD" -- rm /tmp/ready
kubectl -n lab-self-placement wait --for=condition=Ready=false pod/"$HEALTH_POD" --timeout=60s
kubectl -n lab-self-placement get pod "$HEALTH_POD"
kubectl -n lab-self-placement get endpointslices -l kubernetes.io/service-name=health -o yaml
kubectl -n lab-self-placement exec "$HEALTH_POD" -- touch /tmp/ready
kubectl -n lab-self-placement wait --for=condition=Ready pod/"$HEALTH_POD" --timeout=120s
kubectl -n lab-self-placement exec "$HEALTH_POD" -- rm /tmp/live
kubectl -n lab-self-placement get pod "$HEALTH_POD" -w
```

readiness 실패가 반영되면 0/1이 되고 endpoint의 ready=false를 볼 수 있다. 이때 restartCount는 늘지 않는다. liveness 실패 뒤에는 같은 Pod의 restartCount가 늘고 시작 command가 파일을 다시 만들면서 Ready로 돌아온다. watch를 Ctrl+C로 종료한다. UID가 유지되는지도 확인한다.

## 배치 실패와 복구

```bash
kubectl -n lab-self-placement patch deploy place --type=merge -p '{"spec":{"template":{"spec":{"nodeSelector":{"cloud-lab/missing":"true"}}}}}'
kubectl -n lab-self-placement get pods -l app=place
kubectl -n lab-self-placement get events --sort-by=.lastTimestamp
kubectl -n lab-self-placement patch deploy place --type=merge -p '{"spec":{"template":{"spec":{"nodeSelector":null}}}}'
kubectl -n lab-self-placement rollout status deploy/place --timeout=120s
```

일치하는 노드가 없어 새 Pod가 Pending에 남는다. 기존 Pod가 남아 있는 rolling 상태와 독립 Pod Pending을 구분한다. preferred는 우선순위이지 강제 조건이 아니다. [Node Affinity](../../03-pod-deep-dive/05-node-affinity/README.md)와 [Pod Affinity](../../03-pod-deep-dive/06-pod-affinity-antiaffinity/README.md)의 AND/OR·topology 설명을 읽는다.

## taint/toleration 비교

이번 전용 key가 이미 있는 노드에서는 아래 변경을 하지 않는다. 기존 값이 없음을 먼저 확인하고, 학습 worker에서만 실행한다. NoSchedule은 기존 Pod를 퇴거시키지 않으므로 template annotation을 바꿔 새 Pod를 만든다.

```bash
PLACEMENT_NODE=$(kubectl -n lab-self-placement get pod -l app=place -o jsonpath='{.items[0].spec.nodeName}')
kubectl get node "$PLACEMENT_NODE" -o jsonpath='{.spec.taints}{"\n"}'
kubectl taint node "$PLACEMENT_NODE" cloud-lab/self-study=true:NoSchedule
kubectl -n lab-self-placement patch deploy place --type=merge -p '{"spec":{"template":{"metadata":{"annotations":{"study":"taint"}}}}}'
kubectl -n lab-self-placement get pods -l app=place
kubectl -n lab-self-placement get events --sort-by=.lastTimestamp
kubectl -n lab-self-placement patch deploy place --type=merge -p '{"spec":{"template":{"spec":{"tolerations":[{"key":"cloud-lab/self-study","operator":"Equal","value":"true","effect":"NoSchedule"}]}}}}}'
kubectl -n lab-self-placement rollout status deploy/place --timeout=120s
kubectl taint node "$PLACEMENT_NODE" cloud-lab/self-study:NoSchedule-
```

## Quota와 Priority로 확장하기

[11 자원 예산](../../07-cka-preview/11-resource-budget/README.md)을 구축→힌트→복구→정리까지 실행한다. ReplicaSet FailedCreate와 이번 Pending을 비교한다. 이어 [12 PriorityClass](../../07-cka-preview/12-priorityclass/README.md)를 진행한다. 이 두 문서의 풀이를 첫 회에는 참고하고 두 번째에는 닫고 실행한다. 선점 실험은 그 문서의 전용 노드 조건을 따른다.

## 완료와 정리

Ready=false, Pending, OOMKilled, API Forbidden을 같은 문제로 취급하지 않고 첫 확인 대상을 말한다. 실제 OOM/노드 메모리 압박 주입은 이 단계에 필요하지 않다.

```bash
kubectl delete namespace lab-self-placement
rm -f /tmp/lab-self-placement.yaml
```

taint 원복 명령을 먼저 성공시킨다. 다음: [06 영속 저장소](../06-storage/README.md).

[독립 학습 순서](../README.md)
