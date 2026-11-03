# Lab 37 — Dashboard Auth & kubeconfig Contexts

> 학습 단계: **가이드 축소**

## 강의 없이 시작하기

이 README가 공식 학습·실습 기록입니다. 아래의 개념 → 구성 → 관찰 → 장애/복구 → 정리 절차를 따라 진행합니다. [예전 독립 코스의 실행 자산](../../08-independent/07-security/README.md)은 보충 참고자료이며 별도 중복 이수 대상이 아닙니다.

## 목표

ServiceAccount token 인증과 kubeconfig context 사용 흐름을 정리한다. 독립 과정에서는 API의 허용/거부를 직접 확인하고, Dashboard 로그인은 이미 UI가 설치된 경우의 선택 과제로 진행한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. Dashboard ServiceAccount/RoleBinding/Token 관계를 확인한다.
2. UI가 이미 설치됐다면 Token으로 로그인한다. 미설치 환경은 독립 가이드의 curl/kubectl 권한 비교로 본 단계를 진행한다.
3. 현재 kubeconfig의 context를 조회하고 이름을 명확히 정리한다.
4. 선택 과제로 두 번째 클러스터 kubeconfig 병합 절차를 문서화한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 권한이 제한된 ServiceAccount Token으로 Dashboard에서 보이는 범위를 비교한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. Token, kubeconfig, context가 각각 무엇을 선택/인증하는지 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.
