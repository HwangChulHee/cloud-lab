# u1. Glue ETL / Serverless Data Preparation

Glue는 데이터를 분석하기 좋은 형태로 준비하는 managed ETL service다.

```text
Source
 ↓ Extract
Glue
 ↓ Transform
Target
 ↓ Load
Analytics
```

강의 예:

```text
S3 / RDS
   ↓
Glue ETL
   ↓
Redshift
```

## 왜 Glue인가?

직접 ETL server/cluster를 운영하지 않고 transformation job을 실행할 수 있다.

대표 목적:

```text
format 변환
data cleanse
normalize
schema 변환
analytics용 preprocessing
```

## Serverless

강의에서는 Glue를 fully serverless service로 설명한다.

즉 별도 ETL cluster를 직접 provisioning하는 것이 핵심이 아니다.

## 기억할 문장

> Glue는 여러 source의 데이터를 analytics에 맞게 추출·변환·적재하는 serverless ETL 서비스다.
