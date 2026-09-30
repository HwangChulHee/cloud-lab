# Lab 39 — Ingress Routing

> 학습 단계: **가이드 축소**

## 강의 없이 시작하기

[독립 학습 가이드](../../08-independent/08-operations/README.md)에서 개념 설명 → 실행 YAML → 예상 결과 → 장애/복구 → 정리를 순서대로 진행한다. 이 문서는 해당 주제의 복습·추가 과제로 사용한다.

## 목표

Ingress Controller를 통한 path/host routing을 구성한다.

## Recall

Service가 backend Pod를 선택하는 과정과 Ingress object / Ingress Controller의 역할 차이를 먼저 설명한다.

## Build & Observe

1. 실제 설치된 Ingress Controller와 IngressClass를 확인한다. 일반 host/path 실습은 해당 구현을 사용한다. 커뮤니티 ingress-nginx는 2026년 3월 유지보수 종료 대상이므로 신규 설치는 유지보수되는 다른 구현을 사용한다. NGINX Inc.의 구현과 이름만으로 혼동하지 않는다.
2. shopping/customer/order backend와 Service를 준비한다.
3. Path 기반 라우팅을 만든다.
4. Host 기반 라우팅을 추가한다.
5. 요청 URL과 실제 도달 backend를 비교한다.

## Break & Diagnose

Ingress Controller 자체를 제거하는 식의 큰 장애는 만들지 않는다.

1. Ingress rule의 backend Service 이름을 존재하지 않는 이름으로 바꾼다.
2. 또는 path를 의도적으로 잘못 설정해 원하는 backend로 가지 않는 상태를 만든다.
3. Ingress describe, Controller log, Service/Endpoint를 따라가며 원인을 찾는다.

## Recover

잘못된 backend Service 이름/path를 복구하고 같은 요청이 정상 routing되는지 확인한다.

## 완료 검증

1. Ingress object만 존재해도 실제 라우팅을 수행하는 것은 아니라는 점을 설명한다.
2. 요청이 실패할 때 Ingress → Service → Endpoint → Pod 순서로 추적한다.

## Cleanup

Ingress와 이 Lab에서 만든 backend/Service를 삭제한다. 공용 Ingress Controller는 다음 실습에서 사용하므로 유지한다.

## 설명하기

> Ingress는 라우팅 규칙을 선언하고, 실제 규칙을 읽어 트래픽을 처리하는 것은 ______이다.

## 연결된 확장 실습

- [Ingress의 host와 path 라우팅](../../07-cka-preview/06-ingress-routing/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.

- [Ingress에서 Gateway API로 전환](../../07-cka-preview/07-gateway-migration/README.md): 정상 구축부터 변경·진단·복구까지 이어서 연습한다.
