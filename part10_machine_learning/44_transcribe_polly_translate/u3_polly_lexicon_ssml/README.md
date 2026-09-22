# u3. Polly Lexicon / SSML

Polly는 발음과 말하기 스타일을 조정할 수 있다.

## Pronunciation Lexicon

단어의 발음을 직접 지정한다.

강의 예:

```text
St3ph4ne
→ "Stephane"

AWS
→ "Amazon Web Services"
```

Lexicon을 업로드한 뒤 `SynthesizeSpeech`에서 사용할 수 있다.

## SSML

Speech Synthesis Markup Language.

강의에서 가능한 customization:

```text
특정 단어/문구 강조
phonetic pronunciation
breathing sounds
whispering
Newscaster speaking style
```

## 기억할 문장

> Polly의 발음 사전은 Lexicon, 말하기 표현/스타일 제어는 SSML로 연결한다.
