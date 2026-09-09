# Architecture — Lab 01

구축하기 전에 먼저 작성한다.

## 1. 요구사항 해석

### 핵심 문제

- 

### 반드시 만족해야 하는 요구사항

- 

### 이번 Lab에서 굳이 해결하지 않아도 되는 것

- 

## 2. 내가 제안하는 아키텍처

아래에 직접 그린다.

```text
Client
  |
  ?
```

필요하면 Mermaid를 사용해도 된다.

## 3. 서비스 선택 근거

### Load Balancer

선택:

이유:

대안과 비교:

### EC2 배치

인스턴스 수:

AZ 구성:

이유:

### Health Check

Protocol:

Port:

Path:

이유:

## 4. Security Group 설계

### Load Balancer Security Group

| Direction | Protocol | Port | Source / Destination | 이유 |
|---|---|---:|---|---|
| Inbound |  |  |  |  |
| Outbound |  |  |  |  |

### Application EC2 Security Group

| Direction | Protocol | Port | Source / Destination | 이유 |
|---|---|---:|---|---|
| Inbound |  |  |  |  |
| Outbound |  |  |  |  |

## 5. 장애 실험 예상

### 애플리케이션 프로세스 하나가 죽으면

예상:

근거:

### EC2 한 대가 죽으면

예상:

근거:

### 한 AZ 전체가 장애 나면

예상:

근거:

### Load Balancer 자체 장애는

예상:

근거:

## 6. Trade-off

### Availability

- 

### Security

- 

### Cost

- 

### Operational Complexity

- 

## 7. 구축 후 수정된 생각

실제 실험 이후 처음 설계와 달랐던 부분을 적는다.

- 
