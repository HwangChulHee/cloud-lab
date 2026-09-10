# u7. RDS Proxy & RDS Custom

## 1. RDS Proxy가 왜 필요한가

애플리케이션이 RDS에 접속할 때마다 DB Connection을 만든다.

```text
App Instance A ─┐
App Instance B ─┼→ RDS
App Instance C ─┘
```

사용자가 많아지고 Application Instance도 늘어나면 DB Connection 수가 급격히 증가할 수 있다.

예:

```text
App 1대당 DB Connection 100개
App 20대
→ 최대 2,000 connections
```

DB는 Connection 자체도 메모리와 자원을 사용하기 때문에 연결이 지나치게 많아지면 부담이 커진다.

---

## 2. Connection Pooling이란

매 요청마다 DB Connection을 새로 만들고 끊으면 비효율적이다.

그래서 미리 Connection 여러 개를 만들어두고 재사용하는 것을 **Connection Pooling**이라고 한다.

비유하면:

```text
매번 택시 새로 부르기
vs
회사 셔틀 여러 대를 준비해두고 재사용
```

같은 차이다.

RDS Proxy는 Application과 RDS 사이에서 Connection을 관리하고 재사용하는 계층이다.

```text
Applications
    │
    ▼
RDS Proxy
    │
    ▼
Amazon RDS
```

---

## 3. RDS Proxy의 핵심 역할

RDS Proxy는 여러 Application Connection을 받아 DB 쪽 Connection을 효율적으로 관리한다.

개념적으로:

```text
App connections 1,000개
        ↓
RDS Proxy
        ↓
더 효율적으로 관리되는 DB connections
        ↓
RDS
```

즉 애플리케이션과 DB 사이에 Connection 중간 관리자를 두는 것이다.

---

## 4. 왜 Serverless와 자주 연결되는가

Lambda 같은 환경에서는 짧은 시간에 실행 인스턴스가 많이 늘어날 수 있다.

예:

```text
평소 Lambda 10개 실행
이벤트 급증
→ Lambda 1,000개 동시 실행
```

각 Lambda가 모두 RDS에 직접 Connection을 만들려고 하면 DB가 부담을 받을 수 있다.

```text
Lambda x 1000
    │
    ▼
RDS Proxy
    │
    ▼
RDS
```

처럼 두면 DB Connection 관리가 안정적이 된다.

시험에서:

```text
Lambda가 RDS에 너무 많은 connection을 생성
→ RDS Proxy
```

패턴을 기억하면 좋다.

---

## 5. Failover와 RDS Proxy

RDS Proxy는 DB Failover가 발생했을 때 Application의 연결 복구를 더 수월하게 만드는 데도 도움을 줄 수 있다.

Application이 개별 DB Instance 연결 상태를 직접 다 관리하기보다 Proxy Endpoint를 바라보게 만든다.

```text
Application
   │
   ▼
Proxy Endpoint
   │
   ▼
RDS Primary
```

DB 쪽 변화에 대한 연결 관리 부담을 줄일 수 있다.

---

## 6. Secrets Manager와 연결

RDS Proxy는 DB credential 관리에서 Secrets Manager와 함께 사용되는 경우가 많다.

개념적으로:

```text
Application
    ↓
RDS Proxy
    │
    ├── Secrets Manager
    │      └── DB credential
    ▼
RDS
```

시험에서는 RDS Proxy를 단순한 네트워크 Load Balancer로 이해하면 안 된다.

핵심은:

> **DB Connection Pooling / 관리 계층**

이다.

---

# RDS Custom

## 7. 일반 RDS의 제한

일반 RDS의 장점은 AWS가 OS와 DB 운영의 많은 부분을 관리한다는 것이다.

그 대신 사용자가 기반 OS까지 마음대로 수정하는 자유는 줄어든다.

```text
일반 RDS
AWS 관리 영역
├── OS
├── DB software
├── patch
└── infrastructure
```

대부분의 서비스에는 이게 장점이다.

그런데 오래된 기업 시스템처럼 DB 서버 내부에 특별한 설정이 꼭 필요한 경우가 있을 수 있다.

---

## 8. RDS Custom이란

RDS Custom은 일반 RDS보다 기반 환경을 더 많이 제어하고 커스터마이징할 수 있도록 제공하는 형태다.

강의에서는 Oracle과 SQL Server 같은 workload에서 underlying instance와 OS에 접근하거나 커스터마이징할 필요가 있는 경우를 중심으로 설명한다.

예:

```text
기존 기업 Oracle 시스템
├── 특수 OS 설정 필요
├── DB 서버 내부 Agent 필요
└── 일반 RDS 제약으로 이전 어려움

→ RDS Custom 검토
```

---

## 9. RDS와 RDS Custom 차이

```text
일반 RDS
→ AWS가 많이 관리
→ 운영 편의성 높음
→ OS 직접 제어 제한

RDS Custom
→ 더 많은 OS / DB 환경 제어
→ 특수 요구사항 대응
→ 사용자가 관리해야 할 범위도 증가
```

"Custom이 더 좋은 RDS"라고 보면 안 된다.

대부분의 일반 서비스에서는 관리 부담이 적은 일반 RDS가 더 적절하다.

RDS Custom은 **기반 환경을 건드려야 하는 특별한 요구사항**이 있을 때 선택한다.

---

## SAA 판단

```text
DB Connection이 너무 많아짐
→ RDS Proxy

Lambda가 RDS에 대량으로 Connection 생성
→ RDS Proxy

Connection Pooling / DB 연결 관리
→ RDS Proxy

관리형 DB가 필요함
→ 일반 RDS

Oracle / SQL Server 기반 환경을 직접 커스터마이징해야 함
→ RDS Custom
```

## 10단원 최종 구분

```text
RDS
→ 관리형 관계형 DB

Storage Auto Scaling
→ 저장 공간 자동 확장

Read Replica
→ 읽기 확장

Multi-AZ
→ 고가용성 / 자동 Failover

PITR / Snapshot
→ 데이터 복구

KMS / TLS / SG / Secrets Manager
→ 보안

RDS Proxy
→ DB Connection 관리

RDS Custom
→ 기반 환경 커스터마이징
```
