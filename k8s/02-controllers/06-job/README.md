# Lab 22 — Job

> 학습 단계: **중간 가이드**

## 실습 안내

이 README가 해당 주제의 공식 학습 자료다. **실습 전 상태 확인 → 리소스 구축 → 정상 증거 수집 → 제한된 장애 재현 → 복구 → 정리 → 인출 질문** 순서로 진행한다. 기존 독립 코스는 별도 진도로 계산하지 않는다.

## 목표

완료형 workload의 재시도·병렬성·완료 횟수를 확인한다.

## 핵심 개념과 오해 방지

completions는 성공적으로 완료해야 할 작업 수이고, 실패 재시도 때문에 실제 생성된 Pod 수는 더 많을 수 있다. parallelism은 동시에 실행할 작업 수의 상한이며 항상 그 개수가 Running인 것은 아니다. restartPolicy=OnFailure는 같은 Pod 안의 컨테이너 재시작을, Never는 실패 Pod 이후 새 Pod 재시도를 관찰하기 좋다. backoffLimit와 activeDeadlineSeconds도 함께 본다. 완료한 Pod는 TTL 등 별도 정리 정책이 없으면 남아 있을 수 있다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

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
