# Lab 22 — Job

> 학습 단계: **중간 가이드**

## 강의 없이 시작하기

이 README가 이 주제의 **공식 학습·실습 기록**입니다. 아래의 개념 → 구성 → 관찰 → 장애/복구 → 정리 절차를 따라 진행합니다. [이전 독립 코스의 추가 실행 자산](../../02-controllers/08-controller-troubleshooting/README.md)은 고유 예제나 YAML이 필요할 때 참고하며 별도로 중복 완료하지 않습니다.

## 목표

완료형 workload의 재시도·병렬성·완료 횟수를 확인한다.

## 핵심 개념과 오해 방지

completions는 성공적으로 완료해야 할 작업 수이고, 실패 재시도 때문에 실제 생성된 Pod 수는 더 많을 수 있다. parallelism은 동시에 실행할 작업 수의 상한이며 항상 그 개수가 Running인 것은 아니다. restartPolicy=OnFailure는 같은 Pod 안의 컨테이너 재시작을, Never는 실패 Pod 이후 새 Pod 재시도를 관찰하기 좋다. backoffLimit와 activeDeadlineSeconds도 함께 본다. 완료한 Pod는 TTL 등 별도 정리 정책이 없으면 남아 있을 수 있다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. 단일 Job을 실행한다.
2. 서로 다른 completions/parallelism 값을 가진 새 Job을 별도 이름으로 만들어 Pod 실행 패턴을 비교한다.
3. activeDeadlineSeconds를 적용한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 실패 command가 들어 있는 새 Job을 만들어 retry/Failed 상태를 관찰한다. 기존 Job의 Pod template command는 immutable이므로 직접 수정하지 않는다. 복구도 정상 command의 새 Job으로 실행한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. Job의 성공 조건을 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.


## 따라 하기 — Job 성공·실패의 증거

기존의 추상 단계보다 아래 명령을 **공식 실행 순서**로 사용한다. Job은 `spec.template` 변경이 제한되므로 실패 Job을 수정해 복구하지 않고 새로운 정상 Job을 실행한다.

```bash
kubectl apply -f k8s/02-controllers/06-job/job-lab.yaml
kubectl -n lab-job get jobs,pods -w
# watch는 완료/실패를 관찰한 후 Ctrl+C
kubectl -n lab-job wait --for=condition=complete job/batch --timeout=120s
kubectl -n lab-job get job batch -o jsonpath='{.status.succeeded}{" / "}{.spec.completions}{"\n"}'
kubectl -n lab-job get job failing -o yaml
kubectl -n lab-job get pods -l job-name=failing -o wide
kubectl -n lab-job describe job failing
kubectl -n lab-job logs job/batch
```

**예상:** batch는 succeeded=3, parallelism=2 이하로 실행; failing은 재시도 후 Failed condition에 진입한다. Pod 이름과 UID가 여러 번 바뀔 수 있으며 실패 Pod의 종료 코드 1과 Job backoffLimit를 별도로 확인한다.

```bash
kubectl -n lab-job create job recovered --image=busybox:1.37 -- sh -c 'echo recovered'
kubectl -n lab-job wait --for=condition=complete job/recovered --timeout=90s
kubectl -n lab-job get jobs,pods
kubectl delete namespace lab-job
```

**인출:** completions와 parallelism 차이, restartPolicy=Never에서 실패 Pod와 새로운 Pod 관계, `backoffLimit`와 `activeDeadlineSeconds` 차이를 설명한다. 성공/실패/복구와 Namespace 삭제까지 검증해야 완료한다.
