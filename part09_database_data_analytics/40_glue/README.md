# 40. AWS Glue

AWS Glue는 **fully serverless ETL(Extract, Transform, Load) 서비스**다.

강의에서는 단순 ETL뿐 아니라 Data Catalog / Crawler / Job Bookmark / DataBrew / Studio / Streaming ETL까지 함께 다룬다.

## Units

- [ ] [u1. ETL / Serverless Data Preparation](./u1_etl_serverless/README.md)
- [ ] [u2. Data Catalog / Crawler](./u2_data_catalog_crawler/README.md)
- [ ] [u3. Parquet Conversion / Athena Integration](./u3_parquet_athena_integration/README.md)
- [ ] [u4. Job Bookmark / DataBrew / Studio / Streaming](./u4_bookmark_databrew_streaming/README.md)
- [ ] [u5. SAA Selection](./u5_saa_selection/README.md)

## 기본 구조

```text
S3 / RDS / Other Sources
        ↓ Extract
      Glue ETL
        ↓ Transform
      Clean Data
        ↓ Load
S3 / Redshift / Analytics
```

## 핵심

```text
ETL
Data Discovery
Metadata Catalog
Crawler
Serverless
Analytics preparation
```
