# Lab 08 — Service DNS

> 학습 단계: **기초 개념·실습 과제**  
> **실습 상태: ✅ 완료 (2026-10-22)**

## 강의 없이 시작하기

[독립 학습 가이드](../../08-independent/04-networking/README.md)에서 개념 설명 → 실행 YAML → 예상 결과 → 장애/복구 → 정리를 순서대로 진행한다. 이 문서는 해당 주제의 복습·추가 과제로 사용한다.

## 목표

CoreDNS를 통해 Service 이름이 어떻게 발견되는지 확인한다.

## Recall

시작 전에 이 실습에서 재사용되는 이전 개념을 말로 설명한다. 막히면 바로 수정하지 말고 `get → describe → events` 순서로 확인한다.

## Build & Observe

1. request Pod를 만들고 `nslookup <service>`를 실행한다.
2. short name과 `<service>.<namespace>.svc.cluster.local`을 비교한다.
3. DNS 이름으로 HTTP 요청한다.

필요에 따라 다음 명령을 사용한다.

```bash
kubectl get pods -o wide
kubectl get all
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
```

## Break & Diagnose

1. 다른 namespace에서 short name만 사용해 실패시키고 namespace-qualified name으로 복구한다.

1. 예상 상태와 실제 상태를 비교한다.
2. Conditions / Events를 확인한다.
3. Service 관련이면 selector와 Endpoint를 본다.
4. Container 관련이면 logs와 restartCount를 본다.
5. Scheduling 관련이면 Node label, requests, affinity, taint를 본다.

## Recover

원인을 찾은 뒤 **최소 변경**으로 정상 상태로 되돌리고, 복구 전/후 출력 차이를 기록한다.

## 완료 검증

1. 같은/다른 namespace에서 필요한 DNS 이름 차이를 설명한다.

## Cleanup

이 Lab에서 만든 리소스만 삭제한다. Node label/taint, Namespace, StorageClass처럼 다음 실습에 영향을 줄 수 있는 설정은 반드시 원복한다.

## 설명하기

> 이 실습에서 정상 상태를 결정한 핵심 조건은 ______였고, 실패했을 때 가장 먼저 확인할 것은 ______이다.

## 연결된 확장 실습

- [Ingress의 host와 path 라우팅](../../07-cka-preview/06-ingress-routing/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.

## 실습 완료 기록 (2026-10-22)

- [x] `lab-dns`, `lab-dns-client` Namespace 생성 및 Active 확인.
- [x] `k8s-worker1 (192.168.56.31)`의 Nginx `web` Pod (`20.100.194.82:80`) Running/Ready 확인.
- [x] `web-svc` ClusterIP `10.106.76.229:80` 및 EndpointSlice의 `20.100.194.82:80` 확인.
- [x] 동일 Namespace `lab-dns`의 BusyBox Client에서 `nslookup web-svc` 실행: FQDN `web-svc.lab-dns.svc.cluster.local`이 `10.106.76.229`로 해석됨. 검색 도메인 후보에 대한 NXDOMAIN도 출력되어 BusyBox `nslookup` 종료 코드 1 발생했으나 유효한 DNS 응답 확인.
- [x] 루트 점을 포함한 절대 이름 `web-svc.lab-dns.svc.cluster.local.` 조회 성공 및 `wget http://web-svc`로 Nginx HTML 응답 확인.
- [x] 별도 `lab-dns-client` Namespace의 BusyBox Client에서 `/etc/resolv.conf`의 `search lab-dns-client.svc.cluster.local svc.cluster.local cluster.local`, `nameserver 10.96.0.10`, `options ndots:5` 확인.
- [x] 다른 Namespace에서 `wget http://web-svc`는 `bad address`로 실패, `wget http://web-svc.lab-dns`는 정상 HTML 응답. Namespace별 DNS 검색 도메인 영향 확인.
- [x] `lab-dns`, `lab-dns-client` Namespace 삭제 후 둘 다 `NotFound` 확인.

> CoreDNS의 이름 해석과 Service의 HTTP 데이터 경로는 별개다. 이 기록은 기초 Service DNS Lab 완료를 뜻하며 별도 심화/CKA 확장 완료를 뜻하지 않는다.

## 복습 완료 기록 (2026-10-22)

- [x] 문제 1: CoreDNS는 DNS 이름 해석을 담당하며 HTTP 데이터 경로에는 직접 관여하지 않음을 설명.
- [x] 문제 2: Namespace별 `/etc/resolv.conf`의 search domain 및 짧은 이름/qualified name 차이를 설명.
- [x] 문제 3: DNS 성공 후 HTTP 실패 원인으로 애플리케이션 장애와 Node 네트워크 장애를 제시.
- [x] 문제 4: `10.96.0.10`은 CoreDNS Pod IP가 아닌 kube-dns Service의 ClusterIP이며 Pod 재생성과 독립적임을 설명.
- [x] 문제 5: CoreDNS 전체 장애 시 캐시 없는 DNS 이름 조회는 실패하지만, 내부 정상 Service ClusterIP 직접 요청은 성공할 수 있음을 설명.

**복습 결과: 5/5 정답.** 기존 실습 완료 수치는 변경하지 않음.
