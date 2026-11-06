# SmileShark 고객 사례 전수 분석 — 17건 (2026-11-06)

> 출처: 스마일샤크 공식 블로그 [Case Study 1페이지](https://www.smileshark.kr/blog/categories/case-study), [2페이지](https://www.smileshark.kr/blog/categories/case-study/page/2). 두 페이지에 노출된 글 **12 + 5 = 17건**을 게시 순서대로 각각 기록. 단순 목록 요약이 아닌 문제→접근→성과→인프라 학습 포인트를 정리했다. 기사 본문을 복제하지 않고 사실을 재구성한 학습 노트이며, 성과 숫자는 모두 **고객/스마일샤크가 공개한 주장**으로 독립 검증하지 않았다.
>
> 판독 주의: **[공개]** 기사에서 확인된 내용 / **[해석]** 이를 바탕으로 학습·포트폴리오에 적용하는 제안 / **[미공개]** 실제 AWS 계정, 전체 아키텍처, 인스턴스 개수, 실측 로그, 통계 조건 등이 기사에 없는 경우. 일부 기사 아키텍처 이미지는 스스로 '실제 아키텍처와 다름'이라고 명시한다. 따라서 그림만으로 실제 배포 토폴로지를 확정하지 않는다.

## 빠른 인덱스

| # | 사례 | 유형 | 핵심 서비스/키워드 | 인프라 연구 적합성 |
| --- | --- | --- | --- | --- |
| 01 | 호각 | 실시간 미디어·운영 | EKS, ALB/NLB, LB controller, DB CPU, 5xx, GPU 검토 | 매우 높음 |
| 02 | 잇그린 | 현대화·MSP | EC2→일부 ECS Fargate, ALB, VPN, Aurora Serverless | 매우 높음 |
| 03 | 클로봇 | AI PoC | Bedrock, SageMaker, Lambda, OpenSearch, VLM/RAG | 중간 (AI 인프라) |
| 04 | 매경AX | AI 서버리스 워크플로 | Step Functions, AI 오디오 자동화 | 높음 (워크플로 운영) |
| 05 | 엠블록컴퍼니 | AI 자동화 | Bedrock, Google Sheets, 뉴스 API | 낮음~중간 |
| 06 | 블링스 | AI SaaS·기술지원 | LLM/임베딩 벤치마크, 보안·설계 검토 | 중간 |
| 07 | 퀀팃 | 배치·컴퓨팅 | ECS, ECR, CodeBuild, Step Functions, CPU/GPU 모델 | 매우 높음 |
| 08 | 국내 A 법무법인 | 검색·서버리스 | RAG, OpenSearch, S3/CloudFront, API Gateway/Lambda | 중간~높음 |
| 09 | 맑은소프트 | LMS·트래픽 폭증 | MySQL read bottleneck, DynamoDB, Redis, Auto Scaling | **매우 높음** |
| 10 | 그레이박스 | CRM·비용/DB | Lambda→일부 ECS Fargate, RDS→Aurora, CloudFront | 매우 높음 |
| 11 | 하이퍼세일즈 | 데이터 파이프라인 | MSK, 야간 데이터 처리, CloudFront | 높음 |
| 12 | 데일리샷 | 커머스·FinOps | CloudFront 전송비 최적화, 운영 지원 | 높음 |
| 13 | 아정네트웍스 | CRM·배포 자동화 | Bitbucket→AWS Code 시리즈→ECS | 매우 높음 |
| 14 | 해피문데이 | 아키텍처 선택·FinOps | EKS PoC 후 ECS 선택, CloudFront/EBS 최적화 | 매우 높음 |
| 15 | 트라이본즈 | 쇼핑몰 장애·CloudOps | 변칙적 장애 조사, 연속성 확보 | 잠재적으로 높음; 원문 404 |
| 16 | 이누씨 | 온프렘→SaaS | ELB, Multi-AZ, VPC subnet, ECS, managed DB/cache | 매우 높음 |
| 17 | 오픈서베이 | IDC→AWS 마이그레이션 | EKS, EC2 autoscaling, Spot, 데이터 무결성 | 매우 높음 |

## 1페이지 (12건)

### 01. 호각 — 스포츠 OTT 포착
- **원문:** https://www.smileshark.kr/post/hogak-pochak-sports-ott-aws-msp-case
- **문제 [공개]:** 라이브·VOD를 동시에 제공하는 스포츠 미디어에서 DB 부하, 특정 시점 5xx, 간헐적인 NLB 대상 그룹 health check 이상, 통합되지 않은 로드밸런서 관리가 발생. 일정 기반 트래픽 급증과 이후 AI 영상 분석 수요까지 고려해야 했음.
- **적용/지원 [공개]:** EKS 운영/네트워크 검토, ALB/NLB와 AWS Load Balancer Controller의 권한 문제 점검, 로그 기반 5xx 분석, EKS 접근 제어/HTTPS 표준화 및 LB 선언적 관리 제안. CloudFront, S3, 미디어 인코딩, VPN, GPU/EC2/SageMaker 등은 **검토/가이드**된 영역도 있으므로 모두 구현 완료로 단정하지 않음.
- **성과 [공개 주장]:** DB CPU 사용률 약 16% 수준, 2026년 3월 기준 5xx·디스커넥션 문제 해소, NLB target health 정상화. GPU Auto Scaling은 향후 검토 대상.
- **인프라 학습 [해석]:** health check/target registration/IAM 권한 장애 재현→원인 분석 Runbook; DB 관측; 시즌성 트래픽 선제 증설; CPU·GPU 비용별 배치 vs 상시 운영.
- **미공개:** 정확한 EKS 노드 수·GPU 실제 배포·트래픽·비용/성과 측정법.

### 02. 잇그린 — 리턴잇 다회용기/인벤토리
- **원문:** https://www.smileshark.kr/post/aws-case-study-itgreen-msp
- **문제 [공개]:** EC2 위의 주문·반납에 RFID 기반 재고 추적, 세척/가맹 운영이 추가되며 도메인 복잡도가 높아짐. 개발팀의 인프라 설계/유지 부담.
- **적용 [공개]:** 위험이 높은 기존 주문/반납은 EC2 유지, 신규 인벤토리만 ECS/Fargate로 점진적 전환. Public/Private subnet, 외부 ALB, 내부 VPN 접근, Aurora Serverless 사용. 월간 비용·성능·보안 운영 보고.
- **성과 [공개 주장]:** 인프라 설계에 투입되는 리소스 약 70% 감소; 컨테이너 기반 확장·배포 용이. 이는 **AWS 요금 70% 절감**이 아님.
- **인프라 학습 [해석]:** 전면 재작성보다 도메인별 단계적 마이그레이션. EC2/ECS 혼용, 사설망 보호, 전후 인력 소요/운영 복잡도 평가.
- **미공개:** 정확한 Fargate Task/DB 용량 및 트래픽.

### 03. 클로봇 — 현장 유충 위험 탐지 로봇 AI PoC
- **원문:** https://www.smileshark.kr/post/aws-case-study-clobot-ai-poc
- **문제 [공개]:** 일반 객체 인식만으로 유충 위험 환경의 상황적 의미/지침 적합성을 판별하기 어려움. 신속한 모델 비교와 저비용 실험 필요.
- **적용 [공개]:** Amazon Bedrock, Lambda, OpenSearch Serverless, SageMaker를 단위별 시험; VLM+RAG/지식기반 결합, LangChain/LangGraph 흐름, Streamlit 검증. SageMaker JumpStart 활용 비교.
- **성과 [공개 주장]:** 모델/서비스 비교 기간 단축, 유충 위험 판정 PoC 및 방역 가이드 자동 점검 가능성 확인. 운영 서비스의 실전 정확도·트래픽 수치는 미공개.
- **인프라 학습 [해석]:** 별도 GPU 구매 없이 관리형 AI PoC, 추론 경로 지연·비용 비교, 모델·데이터/프롬프트 추적.
- **미공개:** 실서비스 배포 여부와 GPU 인스턴스 수.

### 04. 매경AX — AI 팟캐스트 'MAI 모닝 브리핑'
- **원문:** https://www.smileshark.kr/post/aws-case-study-mkax-ai-podcast-automation-1
- **문제 [공개]:** 인간이 제작하던 대화형 뉴스 오디오가 제작 기간 2~3일·큰 인력 부담을 요구; 뉴스 정확성과 환각 방지 필요.
- **적용 [공개]:** EC2/상시 서버 접근 대신 서버리스 구조 제안, AWS Step Functions로 독립 가능한 각 단계 오케스트레이션. 팩트 추출→문체/대본 변환→검증의 단계화, 음성 생성(ElevenLabs), 음성 후처리.
- **성과 [공개 주장]:** 매일 07:00 자동 발행, 인력 관여를 최종 검수 중심으로 축소, 약 90% 인력 리소스 절감 주장.
- **인프라 학습 [해석]:** 주기성 batch를 항상 켜 둔 서버 대신 Step Functions·서버리스로 모델링하고 실패 단계 재시도·알림·비용 기록.
- **미공개:** 정확한 Step Functions state machine 및 각 Lambda 서비스 경계.

### 05. 엠블록컴퍼니 — 뉴스레터 제작 자동화
- **원문:** https://www.smileshark.kr/post/aws-case-study-mblock-ai-newsletter
- **문제 [공개]:** 기사 날짜/출처/관련성 판별, 톤 일관성, 작업 이력 재현이 일반 대화형 AI에서 어려움.
- **적용 [공개]:** 네이버 뉴스/Google APIs, Bedrock, Google Sheets를 연결. 약 100개 뉴스 수집·평가(100점 기준), 관련 기사 보강, 사람의 체크박스 승인 후 여러 문체 생성; 초기 Slack 방식에서 Sheets로 전환.
- **성과 [공개 주장]:** 편집 소요 3.5시간→40분, 약 81% 단축. 이 수치는 **인프라 처리량**이 아닌 편집 업무 시간.
- **인프라 학습 [해석]:** 사람 승인 단계 포함 자동화, 입력·생성 결과의 감사 추적과 재처리/idempotency, 관리형 API 비용 측정.
- **미공개:** 내부 배포 토폴로지·서비스별 비용.

### 06. 블링스 — 맞춤형 AI 챗봇
- **원문:** https://www.smileshark.kr/post/blynx-aws-case-study
- **문제 [공개]:** SI에서 글로벌 B2C AI 챗봇 SaaS로 피벗, 미숙한 신기술 스택을 빠르게 습득해야 했고 안전한 AWS 인프라 검토·지원 필요.
- **지원 [공개]:** LLM/임베딩 벤치마크 정보, AWS 인프라·보안 검토, AWS 파트너 기술 지원과 크레딧 프로그램 연계. 구체적인 고객의 실배포 아키텍처를 단정할 정보는 부족.
- **성과 [공개 주장]:** 약 3개월 베타 출시, 서비스 시작 후 약 한 달에 챗봇 약 300개 생성.
- **인프라 학습 [해석]:** 인프라/보안 설계 검토 체크리스트, 임베딩/추론 서비스 비교 성능보고.
- **미공개:** 모델 서빙 위치, GPU 여부, 클러스터 크기.

### 07. 퀀팃 — 금융 모델 파이프라인
- **원문:** https://www.smileshark.kr/post/aws-case-study-quantit
- **문제 [공개]:** 사무실 물리 PC 기반 배치에서 장애·환경 종속성. 오전 6시 데이터 유입부터 9시 장 개시 전까지 모델 연산을 완료해야 하는 마감 시한.
- **적용 [공개]:** EC2에 직접 구성한 환경에서 ECS 컨테이너 워크로드로 전환, Step Functions로 데이터 읽기→CodeBuild→ECR 이미지→CPU/GPU 모델 실행 흐름 자동화. 시간대별 컴퓨팅 사용 조정.
- **성과 [공개 주장]:** 모델러별 파이썬/라이브러리 환경 독립, 워크플로 가시성, 시간대별 리소스 효율. 정량 비용 절감액은 미공개.
- **인프라 학습 [해석]:** 이 사례는 GPU/AI 인프라 방향과도 연결됨. 시간 제한 batch 스케줄, 실패 복구/재처리, EC2/컨테이너/GPU의 실행시간·비용 비교.
- **미공개:** GPU 배포 방식과 실행량 수치.

### 08. 국내 A 법무법인 — 문서 검색/AI 업무 지원
- **원문:** https://www.smileshark.kr/post/aws-case-study-a-korean-law-firm
- **문제 [공개]:** 문서/검색 데이터와 증가하는 큐레이션·문의 트래픽, 대량 PDF 처리 및 AI 업무 지원.
- **적용 [공개]:** RAG/LLM, LangChain-OpenSearch 검색 가이드, OpenSearch 벡터 인덱스, S3+CloudFront, Lambda/API Gateway, DynamoDB 및 Auto Scaling 관련 아키텍처.
- **성과 [공개 주장]:** 페이지 로딩 약 40% 개선, 검색/데이터 처리 약 60% 향상. 각 개선율의 부하 조건과 기간은 미공개.
- **인프라 학습 [해석]:** 문서 ingest·벡터 검색 파이프라인, cache/CDN과 serverless 분리, 관측 가능한 요청 지연 경로.
- **주의:** 공개 구성도는 실제 아키텍처와 다를 수 있다고 명시.

### 09. 맑은소프트 — LMS 수강신청/학습 플랫폼 (**현 프로젝트와 직접 연결**)
- **원문:** https://www.smileshark.kr/post/aws-case-study-malgnsoft
- **문제 [공개]:** 수강신청 시기와 글로벌 사용으로 요청 급증; MySQL 읽기 집중으로 병목 및 장애. 공공 LMS 보안 요구와 비용도 관리 필요.
- **적용 [공개]:** AWS Auto Scaling, **일부 읽기 데이터를 DynamoDB로 이전**, Redis 캐시(학습 상태/강의 목록 등 반복 조회), CloudFront 글로벌 캐시.
- **성과 [공개 주장]:** 처리 속도 2배, 현재 초당 수천 건 데이터 처리 가능, 클라우드 비용 약 30% 절감, 해외 콘텐츠 접근 속도 약 50% 개선. 어떤 API가 '수천 건'인지, 동시 신청 commit/s인지 **불명**.
- **인프라 학습 [해석]:** 현재 course-registration-infra와 비교해 **조회/신청을 구분**. read-heavy 워크로드에서 SQL 병목을 먼저 계측→캐시/읽기모델 분리 유무 A/B; 캐시 무효화/정원 표시에 일관성 설계. Redis·DynamoDB를 결과 없이 도입하지 말 것.
- **미공개:** 실제 수강신청 DB 트랜잭션 잠금/대기열 여부와 정확한 트래픽.

### 10. 그레이박스 — 노티플라이 CRM
- **원문:** https://www.smileshark.kr/post/aws-case-study-greybox-notifly
- **문제 [공개]:** 실시간 메시징/데이터 처리 증가로 Glue/Lambda 비용 상승, Lambda→PostgreSQL 연결 문제, 멀티테넌트 확장.
- **적용 [공개]:** 일부 Lambda를 ECS Fargate로 전환, RDS에서 Aurora 전환, CloudFront, Glue/RI 최적화 제안.
- **성과 [공개 주장]:** Glue 비용 약 20% 감소, Lambda 관련 비용 약 15% 감소, 기사에서 99.99% 안정성을 표기. Aurora 제품의 SLA·내구성 수치와 고객 서비스의 실제 관측 가용성을 혼동하지 말 것.
- **인프라 학습 [해석]:** Lambda vs Fargate 비용 손익분기점, DB connection burst와 pool 관리, multi-tenant 운영 지표.
- **미공개:** 실제 인프라 사양, 보정된 월 비용 분모 및 가용성 측정 근거.

### 11. 하이퍼세일즈 — B2B 기업 데이터 플랫폼
- **원문:** https://www.smileshark.kr/post/aws-case-study-hypersales
- **문제 [공개]:** 50만 건 이상 기업 데이터의 대량/주기적 갱신 작업을 사용자 영향이 적은 새벽에 완료해야 함.
- **적용 [공개]:** AWS MSK를 통한 데이터 파이프라인 개선, CloudFront와 비용 최적화.
- **성과 [공개 주장]:** 데이터 업데이트 속도 약 50% 향상, 인프라 운영 비용 약 30% 절감.
- **인프라 학습 [해석]:** Kafka/MSK의 처리량, consumer lag, 재처리, 장애 복구, batch deadline과 오프피크 증설 실험.
- **미공개:** partition/replica/retention 설정, 정확한 이벤트 수.

### 12. 데일리샷 — 커머스 운영·CloudFront
- **원문:** https://www.smileshark.kr/post/aws-case-study-dailyshot
- **문제 [공개]:** 빠른 성장 대비 인프라 전문 인력 부족, 트래픽 증가 및 이미지 전송 비용.
- **적용 [공개]:** AWS 테크 서포트와 운영 컨설팅, CloudFront 비용·캐싱/전송 최적화.
- **성과 [공개 주장]:** 전체 클라우드 인프라 비용 40% 이상 감소, 이미지 전송 비용 70% 이상 감소. **서로 범위가 다른 두 수치**.
- **인프라 학습 [해석]:** CDN cache hit, origin traffic, egress 비용/성능 계산, 월별 Cost Explorer 보고서.
- **미공개:** 정확한 캐시 정책·비용 계약 조건.

## 2페이지 (5건)

### 13. 아정네트웍스 — CRM/CRMS
- **원문:** https://www.smileshark.kr/post/aws-case-study-ajungnetworks-cicd-buildup
- **문제 [공개]:** 성장하는 고객·CS/CX 업무용 자체 CRM을 빠르게 개발·배포해야 하는데 인프라 설계와 CI/CD 통합 역량 부족.
- **적용 [공개]:** 기존 Bitbucket을 유지하면서 AWS Code 시리즈 빌드/파이프라인을 통해 컨테이너 이미지 생성 후 ECS 서비스에 배포.
- **성과 [공개 주장]:** 반복 배포/테스트 자동화와 컨테이너 기반 워크로드 구축. 정량적인 배포 시간·장애 감소 수치 미공개.
- **인프라 학습 [해석]:** Git/CodePipeline/CodeBuild/ECR/ECS 배포, rollback, 실패 알림과 배포 상태 측정.
- **미공개:** 배포 정책(blue/green 여부), 정확한 클러스터 크기.

### 14. 해피문데이 — 앱·이커머스 비용/아키텍처
- **원문:** https://www.smileshark.kr/post/aws-case-study-happymoonday-cloudfront
- **문제 [공개]:** 앱·커머스 성장으로 DB/서버 확장, 콘텐츠 전송 규모 증가 및 비용 부담.
- **적용 [공개]:** PoC 크레딧으로 **EKS 고도화를 테스트한 뒤 최종 ECS 선택**. CloudFront 비용 최적화, DB minor upgrade 및 EBS 세대 조정; 2주 내 최적화 보고서 제공.
- **성과 [공개 주장]:** 비슷한 트래픽 조건에서 CloudFront 비용 약 65% 절감.
- **인프라 학습 [해석]:** Kubernetes를 무조건 채택하지 않고 ECS/EKS 복잡도·운영비용·요건 비교. FinOps 보고와 워크로드별 선택 기준.
- **미공개:** EKS/ECS 비교 실측 지표나 구체적인 테스트 비용.

### 15. 트라이본즈 — 쇼핑몰 CloudOps
- **원문(현재 404):** https://www.smileshark.kr/post/aws-case-study-tribons-cloudops-1
- **확인 상태:** **분류 목록에 게시물은 있으나 직접 원문 접근 404.** 아래는 [Case Study 2페이지](https://www.smileshark.kr/blog/categories/case-study/page/2)의 카드 문구만으로 확인 가능한 내용.
- **문제 [목록 공개]:** 쇼핑몰에서 변칙적으로 발생하는 서비스 장애와 연속 운영의 어려움.
- **적용 [목록 공개]:** 스마일샤크 CloudOps 서비스 및 인프라 안정화 지원으로 소개.
- **성과/기술:** 서비스 중단 없이 운영한다는 방향의 소개 외 구체적인 구성 요소, 성과 수치, 장애 원인 **검증 불가**. 다른 사례의 AWS 구성을 이곳에 전용해서 적지 않음.
- **인프라 학습 [해석]:** 사유별 장애 유형 표준 분류, 인시던트 분석, 알람→Runbook→복구→재발 방지 훈련이 적합.

### 16. 이누씨 — B2B 미디어 CMS의 SaaS 전환
- **원문:** https://www.smileshark.kr/post/case-study-inuc
- **문제 [공개]:** 온프레미스 CMS를 B2B SaaS로 전환하며 빠른 개발·확장 및 서비스 연속성 필요.
- **적용 [공개]:** ELB, 2개 이상 AZ, Public/Private subnet, ECS/Docker, Auto Scaling, ElastiCache/Aurora/S3 등 관리형 서비스. 온프레미스와 클라우드의 혼합 운영도 검토.
- **성과 [공개 주장]:** 출시/개발 기간 **35% 이상 단축**, AWS 관리형 인프라로 개발·운영 편의 향상.
- **인프라 학습 [해석]:** 다중 AZ, AZ 장애 재현, 데이터 분리, 배포/롤백, hybrid 네트워크, RTO/RPO 기준.
- **미공개:** 실제 복구 목표·장애 훈련 결과. 기사에 ECS와 Auto Scaling Group 용어가 함께 나와 정확한 compute 연결 구조는 그림/문구만으로 확정하지 않음.

### 17. 오픈서베이 — IDC/국내 클라우드에서 AWS
- **원문:** https://www.smileshark.kr/post/case-study-opensurvey-aws-migration
- **문제 [공개]:** IDC 물리 장비 문제와 분산 데이터·VM 운영 복잡성. 월 100만 부 이상 설문 데이터의 **무결성**과 신규 고객 확장/비용 대응 필요.
- **적용 [공개]:** AWS 마이그레이션, EKS/쿠버네티스, EC2 자동 확장 및 Spot 활용, 데이터 무결성 확인을 강조.
- **성과 [공개 주장]:** 더 유연한 인프라 확장/고객 워크로드 대응, 신규 개발 인스턴스 Spot 비용 약 70% 할인 경험. 전체 운영비 70% 절감과는 다름.
- **인프라 학습 [해석]:** migration runbook, 데이터 검증 전/후 비교, EKS autoscaling, Spot 중단 처리, 롤백·비용 평가.
- **미공개:** 이전 과정의 downtime/RPO와 정확한 EKS 노드 수.

---

## 공통 관찰 — 사례에서 반복되는 실제 MSP 업무

| 반복되는 문제 | 증거 사례 | 실무에서 요구되는 산출물 |
| --- | --- | --- |
| 아키텍처 선택과 점진적 현대화 | 잇그린, 해피문데이, 이누씨 | 요구사항/제약, ECS vs EKS 결정기록(ADR), 설계도 |
| DB·캐시·연결 병목 | 호각, 맑은소프트, 그레이박스 | 지표/로그 기반 RCA, p95·쿼리·락·연결 측정, 재실험 |
| 정각/시즌성 또는 deadline 부하 | 맑은소프트, 호각, 퀀팃, 하이퍼세일즈 | 부하 시나리오, capacity plan, 사전 확장/축소 |
| 장애·관측·권한 문제 | 호각, 트라이본즈(목록), 맑은소프트 | 알람, 인시던트 타임라인, Runbook, 재발 방지 |
| 비용 개선 | 잇그린, 그레이박스, 데일리샷, 해피문데이 | 비용 범위/분모 명시, 이전·이후 단가, 비용 보고 |
| 배포 자동화 | 아정네트웍스, 이누씨 | CI/CD, 이미지 관리, 배포·롤백, 접근통제 |
| AI/배치 운영 | 퀀팃, 클로봇, 매경AX, 엠블록컴퍼니 | workflow 재시도, 추론/잡 비용, 실패 가시성 |
| 하이브리드·마이그레이션 | 오픈서베이, 이누씨 | migration plan, 무결성 검증, 장애/복구 실습 |

## 현재 포트폴리오 재설계 전에 내려야 할 판단

1. **수강신청 도메인이 틀렸다고 바로 결론 내리지 말 것.** 맑은소프트는 실제 수강신청/학습 플랫폼의 읽기 병목을 공개한 강한 반례다. 단, 지금의 24개 강의·작은 DB가 같은 병목을 만든다는 뜻은 아니다. 실제 워크로드를 확대할지, DB 읽기 경합/캐시를 실험할지 분리해 판단해야 한다.
2. **MSP 지원용 포트폴리오라면 게임 서버를 억지로 추가할 이유가 적다.** 고객이 겪은 특정 문제를 근거로 AWS 구축/운영/개선을 재현하는 것이 직접적이다. 게임 실시간 세션은 지원 직무의 요구가 명확할 때 검토.
3. **'인프라 설계 의사결정'이 핵심.** ECS/Fargate vs EKS, EC2 vs Fargate, serverless vs 상시 서버를 비용/운영 부담/신뢰성으로 비교하고 선택 이유를 기록.
4. **실무 사고 실험 우선.** LB health check+IAM, DB read saturation, CPU quota/JVM warm-up, ECS Task 장애, AZ 장애, 로그 유실, 배포 실패를 의도적으로 재현. 관측→RCA→복구→검증까지 완료.
5. **운영 기록은 결과물.** k6/raw metrics, incident/Runbook, monthly-style cost/health/security review, ADR, 이후 개선 전후 보고서를 만들어야 단순 앱 개발 포트폴리오와 구분된다.
6. **단계적 구축:** 기존 course-registration-infra의 A–E 로컬 실험을 포기하지 말고 비교 기준선으로 보존. 추가 서비스나 AWS 자원 구성 변경은 별도의 설계 단계에서 결정하고 실행할 것.

### 프로젝트 재설계 후보 (아직 미확정)
- **안 1 · 기존 수강신청 기반 MSP 운영 사례:** 맑은소프트 + 호각 + 잇그린 패턴을 결합해 DB read 병목, 캐시/정합성, ECS 부하·복구, 운영 보고서 재현.
- **안 2 · 배치/AI 인프라 중심:** 퀀팃 + 하이퍼세일즈 + 매경AX 패턴으로 정시 배치 SLA, Step Functions, 컨테이너 실행, 재시도·비용 분석.
- **안 3 · 신규 SaaS의 AWS 현대화:** 잇그린 + 아정네트웍스 + 해피문데이 + 오픈서베이 패턴으로 EC2→ECS, IaC/CI/CD, Multi-AZ, 비용/보안/관측을 평가.

**현재 결론:** 17건 전수 사례는 '게임 도메인'을 강하게 지지하기보다 **운영 관측, 기술 선택, 장애 복구, 정량 성능·비용 개선**에 집중하라는 신호를 준다. 실제 직무 공고/팀 역할과 예산·일정을 본 뒤 하나의 검증 가능한 프로젝트로 좁혀야 한다.

## 추후 검증할 항목
- 원문 404인 트라이본즈: 복구되면 기술·결과 보강.
- 성과 수치의 정의와 측정 방법: 블로그는 홍보·고객 인터뷰 중심이므로 기술적 검증 데이터가 부족한 경우가 많음.
- AWS 실배포 아키텍처: 공개용 설명 그림과 실제 구성 분리.
- 게임 분야: 이번 **고객 사례 목록 17개**에 실시간 멀티플레이 전문 구축 사례가 명시되지 않았다는 사실과, 회사에 해당 기술 역량이 없다는 주장은 다름.
