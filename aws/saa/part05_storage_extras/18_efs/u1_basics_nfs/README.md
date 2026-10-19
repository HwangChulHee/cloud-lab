# u1. EFS 기본 구조 / NFS

## 1. EFS란?

EFS는 managed file system이다.

```text
Multiple Linux Clients
        ↓
      NFSv4.1
        ↓
     Amazon EFS
```

강의에서는 Linux 기반 AMI와 호환되며 Windows와는 호환되지 않는다고 설명한다.

## 2. POSIX File System

EFS는 Linux 계열의 표준 file API를 사용하는 POSIX file system으로 설명된다.

즉 애플리케이션 입장에서는 일반 공유 파일 시스템처럼 다룰 수 있다.

## 3. 자동 확장

강의 핵심:

```text
File system grows automatically
→ capacity planning 없음
→ pay-per-use
```

## 4. 동시 접근

강의에서는 수천 개의 concurrent NFS client를 지원하고 petabyte scale까지 자동 확장할 수 있다고 설명한다.

## 기억할 문장

> EFS는 여러 Linux workload가 NFS로 동시에 접근하는 자동 확장형 managed shared file system이다.
