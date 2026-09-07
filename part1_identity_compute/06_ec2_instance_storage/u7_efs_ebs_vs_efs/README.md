# u7. EFS & EBS vs EFS

## 지도 확인

EFS(Elastic File System)는 여러 EC2 인스턴스가 함께 마운트할 수 있는 관리형 네트워크 파일 시스템이다.

```text
EC2 ─┐
EC2 ─┼─ EFS
EC2 ─┘
```

---

## EFS 개념

EFS는 NFS 기반의 POSIX 파일 시스템이다.

핵심 특징:

- 여러 EC2에서 동시에 mount 가능
- Multi-AZ 환경에서 사용 가능
- Linux 기반 EC2와 사용
- Security Group으로 접근 제어
- 용량이 자동으로 확장
- 사용량 기반 과금
- KMS 기반 at-rest encryption 지원

대표 사용 사례:

- content management
- web serving
- data sharing
- 여러 서버가 같은 파일을 공유해야 하는 경우

---

## Performance / Throughput

강의에서는 EFS의 성능 설정을 다음처럼 구분한다.

### Performance Mode

```text
General Purpose
→ 일반적인 latency-sensitive workload

Max I/O
→ 더 높은 병렬 처리량이 필요한 workload
```

### Throughput Mode

```text
Bursting
Provisioned
Elastic
```

특히 workload가 불규칙할 때 Elastic throughput을 선택할 수 있다.

---

## Storage Classes

```text
Standard
→ 자주 접근

Infrequent Access (EFS-IA)
→ 덜 자주 접근

Archive
→ 매우 드물게 접근
```

Lifecycle policy로 파일을 저렴한 tier로 이동할 수 있다.

가용성 기준으로는 Multi-AZ Standard와 One Zone 계열을 구분한다.

---

## EBS vs EFS

```text
EBS
→ Block Storage
→ 기본적으로 한 EC2에 연결
→ 특정 AZ에 종속
→ 용량/IOPS를 provision

EFS
→ File Storage
→ 여러 EC2가 공유
→ Multi-AZ
→ 자동 확장
```

EBS Multi-Attach라는 예외가 있지만 일반적인 SAA 선택 문제에서는 '한 서버용 block storage인가, 여러 서버가 공유할 file system인가'를 먼저 본다.

---

## SAA 연결

```text
한 EC2의 영속적인 Block Storage
→ EBS

여러 EC2가 같은 Linux 파일을 공유
→ EFS

Multi-AZ 공유 파일 시스템
→ EFS

다른 AZ로 EBS 이동
→ Snapshot으로 복원
```

이 유닛까지 보면 EC2 Instance Storage의 큰 선택 지도는 다음과 같다.

```text
영속 Block Storage → EBS
고성능 임시 Local Storage → Instance Store
여러 EC2 공유 File System → EFS
EC2 실행 이미지 → AMI
EBS 백업/이동 → Snapshot
```
