# u5. S3 Encryption — SSE-S3 / SSE-KMS / SSE-C / Client-Side

S3 암호화는 크게 **서버 측 암호화(Server-Side Encryption)** 와 **클라이언트 측 암호화(Client-Side Encryption)** 로 나눈다.

```text
Server-Side Encryption
→ S3에 도착한 뒤 AWS 쪽에서 암호화

Client-Side Encryption
→ 애플리케이션이 업로드 전에 암호화
```

## 1. SSE-S3

SSE-S3는 S3가 소유하고 관리하는 키로 객체를 암호화한다.

```text
User → S3 → S3 managed key로 암호화 → 저장
```

키 관리가 가장 단순하고, 강의 기준으로 새 객체는 기본적으로 서버 측 암호화가 적용된다.

## 2. SSE-KMS

SSE-KMS는 AWS KMS의 Key를 이용한다.

장점은 단순 암호화를 넘어 키 권한을 세밀하게 제어하고 CloudTrail 등을 통해 키 사용을 감사할 수 있다는 점이다.

```text
User
 ↓ upload
S3
 ↓ GenerateDataKey
KMS
 ↓
암호화된 Object 저장
```

다운로드 시에는 KMS `Decrypt` 호출이 연결된다. 따라서 매우 많은 요청이 발생하면 KMS API quota도 고려해야 한다.

예:

```text
금융 문서 저장
+ 누가 어떤 Key를 사용했는지 감사 필요
→ SSE-KMS
```

## 3. SSE-C

SSE-C는 **Customer-Provided Key**, 즉 고객이 암호화 키를 직접 제공한다.

```text
Client가 Key 제공
→ S3가 그 Key로 암호화/복호화
→ S3는 Key 자체를 저장하지 않음
```

키 관리 책임이 사용자 쪽에 더 크다. HTTPS를 통해 키를 안전하게 전달해야 한다.

## 4. Client-Side Encryption

애플리케이션이 S3에 보내기 전에 데이터를 암호화한다.

```text
Plaintext
 ↓ client가 암호화
Ciphertext
 ↓ upload
S3
```

S3는 이미 암호화된 데이터를 저장할 뿐이다.

## SAA 판단

```text
가장 단순, AWS가 키까지 관리
→ SSE-S3

KMS 권한 제어 / 감사 / 키 정책 필요
→ SSE-KMS

고객이 직접 Key를 제공하고 관리
→ SSE-C

AWS에 보내기 전에 자체 암호화
→ Client-Side Encryption
```

시험에서는 "누가 키를 관리하는가"와 "KMS 기능이 필요한가"를 기준으로 구분하면 된다.
