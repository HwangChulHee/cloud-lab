# u1. Amazon Kendra

Amazon Kendra는 **Machine Learning 기반 fully managed document search service**다.

## 검색 대상

강의에서는 다음 document/source를 언급한다.

```text
Text
PDF
HTML
PowerPoint
MS Word
FAQs

Amazon S3
Amazon RDS
Google Drive
Microsoft SharePoint
Microsoft OneDrive
3rd-party / Custom
```

## Natural Language Search

사용자가 자연어 질문을 입력하면 indexed knowledge에서 답을 찾는다.

강의 예:

```text
User:
"Where is the IT support desk?"

Kendra:
"1st floor"
```

## Incremental Learning

사용자 interaction/feedback을 학습해 선호되는 검색 결과를 promote할 수 있다고 설명한다.

또한 다음 기준을 수동 조정할 수 있다.

```text
data importance
freshness
custom tuning
```

## OpenSearch와 구분

```text
OpenSearch
→ general search engine / log / full-text / partial match

Kendra
→ enterprise documents
→ natural language question answering
→ ML-powered relevance
```

## 기억할 문장

> Kendra는 여러 기업 문서를 index하고 자연어 질문으로 답을 찾는 ML-powered document search 서비스다.
