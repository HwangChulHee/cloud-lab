# u2. Redshift Loading / Spectrum

## 1. 대량 Insert

강의는 Redshift에 작은 insert를 계속 보내는 것보다 **batch / large insert**가 훨씬 낫다고 강조한다.

대표 적재:

```text
S3
 ↓ COPY
Redshift
```

또는:

```text
Kinesis Data Firehose
 ↓
S3 staging / copy
 ↓
Redshift
```

## 2. COPY Command

S3의 대량 데이터를 Redshift로 적재할 때 대표적으로 COPY를 사용한다.

```sql
COPY table
FROM 's3://bucket/path'
IAM_ROLE '...';
```

핵심은 개별 row insert보다 bulk loading이 자연스럽다는 점이다.

## 3. Enhanced VPC Routing

강의는 Redshift와 외부 data source 사이 traffic을 VPC 경로로 제어하는 Enhanced VPC Routing을 보여준다.

## 4. Redshift Spectrum

Redshift Spectrum은 **S3에 있는 데이터를 Redshift cluster로 적재하지 않고 query**하게 한다.

```text
Redshift Cluster
      ↓ query
Redshift Spectrum
      ↓
S3
```

강의 핵심:

```text
S3 data를 external table처럼 query
Redshift cluster는 query 시작에 필요
Spectrum nodes가 분산 처리
```

## 기억할 문장

> Redshift는 data warehouse 자체에 대량 적재할 수도 있고, Spectrum으로 S3 데이터를 직접 분석할 수도 있다.
