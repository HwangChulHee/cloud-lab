# 02. ConfigMap·Secret을 환경변수와 파일로 주입하기

## 먼저 이해할 것

환경변수는 컨테이너 시작 시 정해지고, 일반 projected volume은 변경이 지연 반영될 수 있다. subPath로 마운트한 파일은 같은 방식으로 갱신되지 않는다. 앱이 파일을 다시 읽는지도 별도 조건이다. Secret의 Base64는 암호화가 아니다. 아래 비밀번호는 학습용 가짜 값이다.

## 따라 하기

```bash
kubectl apply -f k8s/08-independent/02-configuration/setup.yaml
kubectl -n lab-self-config wait --for=condition=Ready pod/config-reader --timeout=120s
kubectl -n lab-self-config exec config-reader -- printenv MODE
kubectl -n lab-self-config exec config-reader -- cat /config/mode /fixed/mode
kubectl -n lab-self-config exec config-reader -- sh -c 'test -s /credentials/password && echo secret-file-present'
```

환경변수와 두 파일 모두 처음에는 `blue`다. Secret 파일이 있는지만 확인하고 원문을 학습 기록에 붙이지 않는다.

## 변경 → 관찰 → 복구

```bash
kubectl -n lab-self-config patch cm settings --type=merge -p '{"data":{"mode":"green"}}'
kubectl -n lab-self-config exec config-reader -- cat /config/mode
kubectl -n lab-self-config exec config-reader -- cat /fixed/mode
kubectl -n lab-self-config exec config-reader -- printenv MODE
```

첫 파일만 시간이 지나 green으로 바뀔 수 있다. 즉시 바뀌지 않으면 잠시 후 다시 조회한다. subPath와 환경변수는 blue로 남는다. 이를 앱 재시작으로 해결하려고 독립 Pod를 삭제한 뒤 **Pod 파일만** 다시 apply한다. setup 전체를 apply하면 ConfigMap도 blue로 복구하므로 비교가 사라진다.

```bash
kubectl -n lab-self-config delete pod config-reader --wait=true
kubectl apply -f k8s/08-independent/02-configuration/pod.yaml
kubectl -n lab-self-config wait --for=condition=Ready pod/config-reader --timeout=120s
kubectl -n lab-self-config exec config-reader -- printenv MODE
kubectl -n lab-self-config exec config-reader -- cat /fixed/mode
kubectl -n lab-self-config patch cm settings --type=merge -p '{"immutable":true}'
kubectl -n lab-self-config patch cm settings --type=merge -p '{"data":{"mode":"red"}}'
```

재생성 뒤 green을 예상하고, 마지막 변경은 immutable이라 거부된다. 이 객체를 원복하려면 삭제 후 새 객체가 필요하다. [TLS 설정 확장](../../07-cka-preview/01-configmap-tls/README.md)은 03의 rollout까지 익힌 뒤 진행한다.

## 누적 복습 — 다음 단계 전에

앞 단계의 개념을 현재 증상에 다시 연결한다. 문서를 닫고 세 질문에 답하며, 어려운 질문은 실제 spec/status/Events를 근거로 다시 설명한다.

1. 환경 변수와 ConfigMap volume 변경이 다르게 보이는 이유는?
2. subPath가 변경 내용을 자동 반영하지 않는 이유는?
3. Secret을 참조한 Pod에 API read 권한이 반드시 필요한가?

관련 내부 심화를 할 경우 이 단계의 **namespace를 정리하기 전에** 진행한다. 개념만 읽을 때는 리소스 재생성을 강제하지 않는다.

## 완료와 정리

환경변수, 일반 mount, subPath의 갱신 차이를 세 줄로 설명한다. Secret을 API로 직접 조회하는 권한과 Pod에 주입하는 경로를 구분한다. 일반 Secret volume/env 주입은 kubelet이 처리하므로 Pod의 ServiceAccount에 secrets get 권한을 추가할 필요가 없다. 반면 같은 namespace에서 Pod를 생성할 수 있는 사용자는 Secret을 마운트해 내용을 읽을 수 있으므로, Secret API 조회 권한만 제한해서 충분하다고 생각하지 않는다. [공식 Secret 설명](https://kubernetes.io/docs/concepts/configuration/secret/)을 참고한다.

```bash
kubectl delete namespace lab-self-config
```

다음: [03 Controller](../03-controllers/README.md).

[독립 학습 순서](../README.md)
