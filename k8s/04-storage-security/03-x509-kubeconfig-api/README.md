# Lab 35 — X509, kubeconfig & API

> 학습 단계: **가이드 축소**

## 강의 없이 시작하기

이 README가 공식 학습·실습 기록입니다. 아래의 개념 → 구성 → 관찰 → 장애/복구 → 정리 절차를 따라 진행합니다. [예전 독립 코스의 실행 자산](../../08-independent/07-security/README.md)은 보충 참고자료이며 별도 중복 이수 대상이 아닙니다.

## 목표

kubectl 뒤의 인증서 기반 API 접근을 직접 확인한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. `/etc/kubernetes/admin.conf`의 cluster/user/context 구조를 확인한다.
2. client certificate/key를 추출해 API Server `/api/v1/nodes`를 HTTPS로 호출한다.
3. `kubectl proxy` 방식과 직접 6443 접근을 비교한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 잘못된/없는 인증 정보로 API 호출해 인증 실패를 확인한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. kubectl이 어떤 인증 정보로 API Server에 접근하는지 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 확장 실습

- [CRD 조회와 kubectl explain 문서 추출](../../07-cka-preview/16-crd-discovery/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.


## 독립 심화: 인증서와 토큰으로 API 직접 요청

관리자 kubeconfig의 현재 API server와 CA, **테스트 전용** 클라이언트 인증서를 사용해 `curl --cacert ... --cert ... --key ... "$API_SERVER/api/v1/nodes"` 요청을 검증한다. 이는 관리자 권한이므로 개인 키·토큰·`kubectl config view --raw` 출력은 절대 커밋하지 않는다.

그다음 제한된 ServiceAccount에 대해 `kubectl create token <sa> -n <namespace> --duration=10m`으로 짧은 유효기간의 토큰을 발급하고 `Authorization: Bearer`를 사용해 허용된 Pod 목록 요청과 금지된 Secret 목록 요청의 HTTP 상태를 비교한다. 인증(Authentication), 인가(Authorization), Admission 거절을 구분하며 **403만 보고 인증 실패로 단정하지 않는다**.

파일 격리는 `umask 077`, `mktemp -d`로 수행하고 종료 시 키·토큰 파일을 제거한다. 실행 명령 예제: [x509/RBAC 직접 요청](../../08-independent/07-security/README.md). 기존 전역 kubeconfig를 덮어쓰지 말고 별도의 임시 `--kubeconfig` 파일로 context 변화를 확인한다.
