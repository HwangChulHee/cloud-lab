# u3. Lambda Limits / Memory / Timeout / Storage

강의 기준으로 Lambda의 대표 제한을 이해한다.

## Execution

```text
Memory
→ 128 MB ~ 10 GB

Maximum Execution Time
→ 900 seconds = 15 minutes

Environment Variables
→ 4 KB

/tmp temporary disk
→ 512 MB ~ 10 GB
```

## Memory와 CPU

강의에서 중요한 포인트:

```text
Lambda memory 증가
→ CPU 성능 증가
→ network 성능도 함께 증가
```

즉 memory 설정은 단순 RAM 크기만 바꾸는 것이 아니다.

## Deployment Size

강의에서는 deployment package 제한도 설명한다.

```text
compressed .zip
→ 50 MB

uncompressed code + dependencies
→ 250 MB
```

## /tmp

Function container 안의 `/tmp`는 일시적인 파일 작업에 사용할 수 있다.

예:

```text
S3 file download
→ /tmp에서 변환
→ S3 upload
```

하지만 persistent storage처럼 생각하면 안 된다.

## SAA 판단

```text
15분 초과하는 장시간 작업
→ Lambda 적합성 낮음

많은 dependency / arbitrary runtime
→ ECS/Fargate 또는 Batch 고려

짧은 event processing
→ Lambda
```
