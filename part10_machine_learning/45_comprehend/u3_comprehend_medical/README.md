# u3. Amazon Comprehend Medical

Comprehend Medical은 **unstructured clinical text**에서 의료 관련 정보를 추출한다.

강의 예:

```text
Physician notes
Discharge summaries
Test results
Case notes
```

## PHI Detection

`DetectPHI` API를 이용해 Protected Health Information(PHI)을 탐지할 수 있다.

## 연결 패턴

강의에서는 다음 조합을 언급한다.

```text
S3 Documents
→ Comprehend Medical

Kinesis Data Firehose real-time data
→ Comprehend Medical

Patient Narratives
→ Transcribe
→ Text
→ Comprehend Medical
```

## 기억할 문장

> 의료 임상 텍스트에서 entity/PHI 같은 정보를 NLP로 뽑아야 하면 Comprehend Medical이다.
