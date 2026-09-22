# 75. Classic Solutions Architecture

강의의 Classic Solutions Architecture는 EC2, ELB, Auto Scaling, RDS, ElastiCache, EFS 같은 서비스를 **하나의 3-tier 웹 아키텍처**로 조합하는 연습이다.

## Units

- [ ] [u1. Stateless Web App](./u1_stateless_web_app/README.md)
- [ ] [u2. Stateful Web App / Session](./u2_stateful_session/README.md)
- [ ] [u3. Database / Cache Scaling](./u3_database_cache_scaling/README.md)
- [ ] [u4. Shared Storage / WordPress](./u4_shared_storage_wordpress/README.md)
- [ ] [u5. Security Group Chaining](./u5_security_group_chaining/README.md)

## 전체 그림

```text
Route 53
   ↓
ELB
   ↓
Auto Scaling EC2
   ├→ ElastiCache
   ├→ RDS
   └→ EFS (필요 시)
```

## 핵심

서비스 하나씩 외우는 것이 아니라 다음 질문으로 설계한다.

```text
Web tier를 어떻게 scale할까?
Session은 어디에 둘까?
Read 부하는 어떻게 줄일까?
DB HA는 어떻게 확보할까?
Shared file은 어디에 둘까?
Security Group은 어느 계층만 허용할까?
```
