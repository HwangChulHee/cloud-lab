# u5. EBS Volume Types & Multi-Attach

## 지도 확인

EBS는 workload에 따라 Volume Type을 선택한다.

큰 기준은 다음 세 가지다.

```text
Size
Throughput
IOPS
```

---

## Volume Types

### gp2 / gp3 — General Purpose SSD

범용 workload용 SSD다.

- OS boot volume
- 개발/테스트
- 일반적인 application workload

핵심 차이:

```text
gp2
→ 크기와 IOPS가 연결됨

gp3
→ 용량과 IOPS/Throughput을 독립적으로 조정 가능
```

### io1 / io2 Block Express — Provisioned IOPS SSD

높고 일관된 IOPS가 필요한 workload용이다.

대표적으로 중요한 database workload에 사용한다.

```text
mission-critical database
높은 IOPS
낮은 latency
→ io1 / io2
```

### st1 — Throughput Optimized HDD

순차적인 대용량 처리처럼 IOPS보다 throughput이 중요한 workload에 적합하다.

예:

- Big Data
- Data Warehouse
- Log Processing

### sc1 — Cold HDD

접근 빈도가 낮고 비용이 가장 중요한 HDD workload에 사용한다.

`st1`, `sc1`은 boot volume으로 사용할 수 없다.

---

## EBS Multi-Attach

io1/io2 계열에서는 하나의 EBS Volume을 같은 AZ 안의 여러 EC2 인스턴스에 연결하는 Multi-Attach를 사용할 수 있다.

```text
        io2 EBS
       /   |   \
    EC2   EC2   EC2
       same AZ
```

각 인스턴스가 read/write할 수 있기 때문에 애플리케이션과 파일시스템이 동시 쓰기를 안전하게 처리할 수 있어야 한다.

---

## SAA 연결

```text
일반적인 SSD
→ gp3 중심

크기에 따라 IOPS가 같이 증가
→ gp2

용량과 성능을 독립적으로 조정
→ gp3

높고 지속적인 IOPS / database
→ io1 / io2

높은 sequential throughput
→ st1

거의 사용하지 않는 저비용 HDD
→ sc1

여러 EC2가 같은 고성능 EBS를 동시에 사용
→ io1/io2 Multi-Attach + 같은 AZ
```

수치 전체를 외우기보다 어떤 workload가 어떤 타입을 요구하는지 먼저 구분한다.
