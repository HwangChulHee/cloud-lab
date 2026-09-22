# u2. Textract Forms / Tables / Structured Data

강의가 Textract에서 특별히 강조하는 부분은 **forms와 tables**다.

예를 들어 문서에서:

```text
Document ID
Name
SEX
DOB
...
```

같은 field를 추출해 분석 결과로 만들 수 있다.

## 구조

```text
Invoice / Form / Table
        ↓
     Textract
        ↓
Key-Value / Table Data
        ↓
Application Processing
```

따라서 document processing automation에 적합하다.

## 기억할 문장

> Textract는 문서를 "이미지"로만 보는 것이 아니라 form/table 구조까지 추출하는 document AI 서비스다.
