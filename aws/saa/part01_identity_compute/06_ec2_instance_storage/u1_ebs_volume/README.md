# u1. EBS Volume

## 지도 확인

EC2 인스턴스의 데이터는 인스턴스 자체와 분리해서 생각해야 한다.

```text
EC2
 └─ EBS Volume
```

EBS(Elastic Block Store)는 EC2에 붙여 사용하는 **네트워크 기반 Block Storage**다.

---

## 개념

EBS는 물리적으로 EC2 안에 들어 있는 디스크가 아니라 네트워크를 통해 연결되는 저장장치다.

핵심 특징:

- EC2 실행 중 attach 가능
- 인스턴스와 분리해서 detach / attach 가능
- 데이터를 지속적으로 보관할 수 있음
- 용량과 성능을 미리 provision하고 비용을 지불
- 특정 Availability Zone에 종속

```text
us-east-1a의 EBS
→ us-east-1a의 EC2에는 연결 가능
→ us-east-1b의 EC2에는 바로 연결 불가
```

다른 AZ로 옮기려면 Snapshot을 만든 뒤 대상 AZ에서 새 Volume을 생성한다.

---

## Delete on Termination

EC2를 종료(terminate)할 때 EBS도 같이 삭제할지 결정하는 속성이다.

기본 동작:

```text
Root EBS
→ Delete on Termination = enabled

추가 EBS
→ Delete on Termination = disabled
```

따라서 인스턴스를 삭제한다고 모든 EBS가 항상 같이 삭제되는 것은 아니다.

---

## SAA 연결

```text
EC2와 분리해 유지해야 하는 Block Storage
→ EBS

다른 AZ로 EBS 이동
→ Snapshot → 대상 AZ에서 Volume 생성

EC2 종료 후에도 추가 데이터 디스크를 보존
→ Delete on Termination 설정 확인
```

이번 유닛은 구조와 생명주기 이해가 핵심이므로 별도 유제는 생략한다.
