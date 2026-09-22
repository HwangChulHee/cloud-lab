# u2. Athena Performance / Cost Optimization

Athena는 scan한 data 양이 성능과 비용에 직접 연결된다.

강의의 최적화 포인트를 그대로 기억한다.

## 1. Columnar Format

```text
Parquet
ORC
```

를 권장한다.

필요한 column만 읽을 수 있어 scan량을 줄인다.

## 2. Glue로 변환

```text
CSV / JSON
   ↓
AWS Glue ETL
   ↓
Parquet / ORC
   ↓
Athena
```

## 3. Compression

압축된 데이터를 사용하면 읽어야 할 byte를 줄일 수 있다.

강의에서 언급:

```text
gzip
bzip2
lz4
snappy
zstd
...
```

## 4. Partition

S3 path를 partition column 기준으로 나눈다.

예:

```text
s3://bucket/flights/
  year=1991/
    month=1/
      day=1/
```

특정 날짜 query 시 관련 partition만 읽을 수 있다.

## 5. Larger Files

강의에서는 너무 많은 작은 파일보다 **128 MB보다 큰 파일**을 권장한다.

작은 파일이 너무 많으면 overhead가 커질 수 있다.

## SAA 판단

```text
Athena 비용 절감
→ Parquet/ORC + Compression + Partition

CSV를 Parquet로 변환
→ Glue ETL
```
