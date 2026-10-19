# u3. Glue Parquet Conversion / Athena Integration

Athena 비용과 성능 최적화에서 Glue가 직접 연결된다.

## 구조

```text
S3 CSV
  ↓
Glue ETL
  ↓
Parquet
  ↓
S3
  ↓
Athena
```

강의는 Athena에서 columnar format인 **Parquet / ORC**를 권장한다.

Glue는 CSV/JSON 같은 원본 데이터를 Parquet 등으로 변환하는 데 사용할 수 있다.

## Event-driven ETL

강의 예:

```text
S3 PUT
  ↓ Event Notification
Lambda 또는 EventBridge
  ↓
Glue ETL Job Trigger
  ↓
Parquet 변환
```

## 왜 중요한가?

```text
Columnar format
→ scan data 감소
→ Athena performance 향상
→ Athena cost 감소
```

## SAA 판단

```text
Athena query 비용 절감
→ Glue로 Parquet/ORC 변환

S3 upload 후 자동 ETL
→ Event + Glue Job
```
