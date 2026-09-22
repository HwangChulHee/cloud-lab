# u1. Application Discovery Service / Migration Hub

## AWS Application Discovery Service

Migration 전에 on-premises data center 정보를 수집해 planning을 돕는다.

강의에서 중요하다고 설명하는 정보:

```text
Server Utilization
Dependency Mapping
```

## Agentless Discovery

강의에서 다음을 수집한다고 설명한다.

```text
VM inventory
configuration
CPU / memory / disk usage 같은 performance history
```

## Agent-Based Discovery

더 세밀한 정보를 수집한다.

```text
system configuration
system performance
running processes
network connections between systems
```

## AWS Migration Hub

Discovery Service가 수집한 migration 관련 데이터를 Migration Hub에서 볼 수 있다.

## 기억할 문장

> Application Discovery Service는 무엇을 옮겨야 하고 서로 어떤 dependency가 있는지 파악하고, Migration Hub에서 migration 진행 정보를 모아본다.
