# u6. Global Accelerator & CloudFront Comparison

CloudFront와 Global Accelerator는 둘 다 글로벌 사용자의 성능을 개선하지만 방식이 다르다.

## 1. Global Accelerator

Global Accelerator는 사용자 요청을 가까운 AWS Edge Location으로 받아 AWS 글로벌 네트워크를 통해 최적의 AWS endpoint로 전달한다.

```text
User
 ↓
가까운 AWS Edge
 ↓ AWS Global Network
ALB / NLB / EC2 / Elastic IP
```

핵심은 **콘텐츠를 Edge에 캐시하는 서비스가 아니라 네트워크 경로를 최적화하는 서비스**라는 점이다.

## 2. Anycast IP

Global Accelerator는 고정된 Anycast IP를 제공한다.

Anycast는 여러 위치가 같은 IP를 광고하고 사용자가 네트워크상 가까운 진입점으로 연결되는 방식이라고 이해하면 된다.

```text
사용자가 보는 IP
1.2.3.4

서울 사용자 → 가까운 Edge
미국 사용자 → 가까운 Edge
```

서비스 endpoint가 뒤에서 바뀌어도 사용자가 바라보는 고정 IP를 유지할 수 있다.

## 3. Health Check와 장애 전환

Global Accelerator는 endpoint 상태를 확인하고 비정상 endpoint를 피해 정상 endpoint로 트래픽을 보낼 수 있다.

예:

```text
서울 Region endpoint 장애
→ unhealthy
→ 도쿄 Region endpoint로 트래픽 전환
```

글로벌 애플리케이션에서 빠른 failover 요구와 연결된다.

## 4. CloudFront와 비교

```text
CloudFront
→ CDN
→ HTTP/HTTPS 콘텐츠 캐시
→ S3/HTTP Origin
→ 반복 조회 성능 개선

Global Accelerator
→ 네트워크 경로 최적화
→ TCP/UDP 포함
→ 고정 Anycast IP
→ ALB/NLB/EC2/EIP endpoint
→ 빠른 글로벌 failover
```

예를 들어 이미지/영상 콘텐츠 배포는 CloudFront가 자연스럽고, 실시간 게임이나 글로벌 TCP 애플리케이션처럼 캐시가 의미 없고 네트워크 지연을 줄여야 한다면 Global Accelerator가 더 적합할 수 있다.

## SAA 판단

```text
정적 콘텐츠를 Edge에 Cache
→ CloudFront

HTTP 콘텐츠 CDN
→ CloudFront

TCP/UDP 애플리케이션 글로벌 가속
→ Global Accelerator

고정 글로벌 IP 필요
→ Global Accelerator

멀티 리전 endpoint 사이 빠른 장애 전환
→ Global Accelerator
```
