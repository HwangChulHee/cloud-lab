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

## 완료와 정리

환경변수, 일반 mount, subPath의 갱신 차이를 세 줄로 설명한다. Secret 읽기 권한이 왜 필요한지도 설명한다.

```bash
kubectl delete namespace lab-self-config
```

다음: [03 Controller](../03-controllers/README.md).

[독립 학습 순서](../README.md)
