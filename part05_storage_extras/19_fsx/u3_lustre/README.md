# u3. FSx for Lustre

Lustre는 **large-scale computing용 parallel distributed file system**이다.

강의 use case:

```text
Machine Learning
High Performance Computing
Video Processing
Financial Modeling
Electronic Design Automation
```

## Performance 감각

강의에서는 매우 높은 throughput/IOPS와 sub-millisecond latency를 강조한다.

## Storage Options

```text
SSD
→ low latency
→ IOPS-intensive
→ small/random file operations

HDD
→ throughput-intensive
→ large/sequential file operations
```

## S3 Integration

강의 핵심:

```text
FSx for Lustre
→ S3 data를 file system처럼 읽기
→ computation output을 다시 S3로 쓰기
```

## Deployment Options

### Scratch

```text
temporary
replication 없음
file server failure 시 persistence 보장 안 됨
high burst
short-term processing
cost optimization
```

### Persistent

```text
long-term storage
same AZ 내 replication
failed file server 교체
sensitive / long-term workload
```

## SAA 판단

```text
HPC / ML + high performance shared filesystem
→ FSx for Lustre

S3와 seamless integration + compute
→ FSx for Lustre
```
