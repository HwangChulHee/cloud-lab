# 01. Pod를 만들고 상태·네트워크·파일을 관찰하기

## 먼저 이해할 것

Namespace는 이름과 정책의 범위이고, Pod는 함께 배치하는 컨테이너 묶음이다. 같은 Pod는 IP와 포트 공간을 공유한다. 각 컨테이너의 파일시스템은 분리되지만 volume을 같이 마운트하면 그 경로를 공유한다. label은 검색용 표식이고 selector는 그 표식을 고르는 조건이다.

모든 명령은 저장소 루트의 Linux 셸에서 실행한다. 먼저 [시작 준비](../START.md)를 끝낸다. 아래에서 정상 결과가 안 나오면 다음 명령을 계속 붙이지 말고 Events를 확인한다.

## 따라 하기

```bash
kubectl apply -f k8s/08-independent/01-pods/setup.yaml
kubectl -n lab-self-pods wait --for=condition=Ready pod/pair --timeout=120s
kubectl -n lab-self-pods get pod pair -o wide --show-labels
kubectl -n lab-self-pods get pods -l tier=frontend
kubectl -n lab-self-pods exec pair -c observer -- wget -qO- http://127.0.0.1
kubectl -n lab-self-pods exec pair -c observer -- sh -c 'echo shared-ok > /shared/note'
kubectl -n lab-self-pods exec pair -c web -- cat /shared/note
kubectl -n lab-self-pods logs pair -c prepare
kubectl -n lab-self-pods exec pair -c observer -- cat /shared/init
kubectl -n lab-self-pods logs pair -c web --tail=5
kubectl -n lab-self-pods describe pod pair
```

`READY 2/2`, nginx의 환영 HTML, `shared-ok`를 예상한다. observer가 localhost로 web에 접속한 이유와, 다른 Pod에서는 localhost가 다른 대상인 이유를 설명한다. nginx 요청 로그가 stdout에 나타나는 것도 본다. prepare init container가 먼저 성공한 뒤 두 앱 컨테이너가 시작되고 init-ok 파일을 읽는지 확인한다. 일반 init과 계속 실행하는 Sidecar의 종료 조건은 다르다.

## 변경 → 실패 → 복구

```bash
kubectl -n lab-self-pods label pod pair tier=backend --overwrite
kubectl -n lab-self-pods get pods -l tier=frontend
kubectl -n lab-self-pods get pods -l tier=backend
kubectl -n lab-self-pods label pod pair tier=frontend --overwrite
kubectl -n lab-self-pods exec pair -c observer -- sh -c 'echo private > /tmp/private'
kubectl -n lab-self-pods exec pair -c web -- cat /tmp/private
```

frontend 조회는 비고 backend 조회에 pair가 나타난다. 마지막 cat은 파일 없음으로 실패한다. `/tmp`가 자동 공유되지 않기 때문이다. `get pods`가 전체 Pod를 보여주는지 namespace 없이 실행한 결과와 비교한다.

```bash
kubectl -n lab-self-pods get pod pair -o jsonpath='{.metadata.uid}{"\n"}'
kubectl -n lab-self-pods delete pod pair --wait=true
kubectl -n lab-self-pods get pods
kubectl apply -f k8s/08-independent/01-pods/setup.yaml
kubectl -n lab-self-pods wait --for=condition=Ready pod/pair --timeout=120s
kubectl -n lab-self-pods get pod pair -o jsonpath='{.metadata.uid}{"\n"}'
kubectl -n lab-self-pods exec pair -c web -- cat /shared/note
```

Controller가 없는 독립 Pod는 삭제 후 스스로 돌아오지 않는다. 재생성 뒤 UID가 바뀌고 emptyDir 파일이 사라진다. Pod IP가 반드시 달라져야 하는 것은 아니다.

## 완료와 정리

label 변경은 프로세스를 멈추는가? 컨테이너 재시작과 Pod 삭제 중 어느 것이 emptyDir 수명을 끝내는가? 예상과 실제 결과를 기록한다. 파일 없음은 이번 단계의 예상한 실패다.

```bash
kubectl delete namespace lab-self-pods
```

다음: [02 설정 주입](../02-configuration/README.md). 더 연습하려면 [기초 02 관찰](../../00-foundation/02-kubectl-observation-basics/README.md), [Sidecar 로그](../../07-cka-preview/10-sidecar-logging/README.md)를 순서대로 실행한다. Sidecar 예제는 Deployment를 쓰므로 먼저 03의 Controller 설명을 읽어도 된다.

[독립 학습 순서](../README.md)
