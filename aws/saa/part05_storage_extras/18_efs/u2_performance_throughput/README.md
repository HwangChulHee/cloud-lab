# u2. EFS Performance / Throughput Modes

강의에서는 Performance Mode와 Throughput Mode를 구분한다.

## Performance Mode

### General Purpose

```text
default
latency-sensitive workload
web server
CMS
```

### Max I/O

```text
higher latency
higher throughput
highly parallel workload
big data / media processing
```

강의에서는 file system 생성 시 Performance Mode를 설정한다고 설명한다.

## Throughput Mode

### Bursting

강의 예시:

```text
1 TB
→ 50 MiB/s
→ burst up to 100 MiB/s
```

### Provisioned

저장 용량과 별개로 원하는 throughput을 지정한다.

```text
예:
1 TB storage
+ 1 GiB/s throughput
```

### Elastic

workload에 따라 throughput을 자동으로 올리고 내린다.

강의에서는 unpredictable workload에 사용한다고 설명한다.

## SAA 판단

```text
latency-sensitive general workload
→ General Purpose

highly parallel throughput workload
→ Max I/O

unpredictable throughput
→ Elastic
```
