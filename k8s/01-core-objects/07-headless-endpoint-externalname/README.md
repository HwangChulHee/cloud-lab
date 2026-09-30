# Lab 09 — Headless, Endpoint, ExternalName

> 학습 단계: **기초 개념·실습 과제**

## 목표

Service discovery의 세 가지 변형을 비교한다.

## 핵심 개념과 오해 방지

Headless Service(`clusterIP: None`)는 Service 가상 IP 대신 backend 주소를 DNS에 제공한다. 개별 Pod의 안정적인 이름은 hostname/subdomain 또는 StatefulSet의 serviceName 구성과 Ready 조건을 함께 확인한다. 임의 Pod의 metadata.name만으로 모든 Pod별 DNS가 생긴다고 가정하지 않는다.

ExternalName은 외부 이름을 가리키는 DNS CNAME이다. proxy, 포트 변환, HTTP Host 변경, TLS SNI 변경을 수행하지 않는다. DNS 별칭 조회가 성공해도 HTTP 가상 호스트나 인증서 이름 때문에 요청이 실패할 수 있으므로 `nslookup`과 실제 요청을 별도로 검증한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. Headless Service를 만들고 DNS가 Pod IP를 반환하는지 확인한다.
2. selector 기반 Endpoint를 조회한다.
3. selector 없는 Service + 수동 EndpointSlice를 연결한다. discovery.k8s.io/v1, kubernetes.io/service-name 라벨, 고유 endpointslice.kubernetes.io/managed-by 라벨과 실제 backend IP/port를 지정한다. legacy Endpoints는 1.27 비교 관찰에만 사용한다.
4. ExternalName Service로 외부 도메인을 추상화한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 잘못된 Endpoint IP를 넣어 연결 실패를 재현한 뒤 복구한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. ClusterIP/Headless/ExternalName의 결과 차이를 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.
