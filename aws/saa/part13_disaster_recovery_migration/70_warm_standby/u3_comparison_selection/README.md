# u3. Warm Standby vs Pilot Light

## Pilot Light

```text
critical core만 실행
application 일부는 중지/미실행
```

## Warm Standby

```text
full system 실행
minimum capacity
```

## 비용 / 복구 감각

```text
Pilot Light
→ 비용 ↓
→ RTO ↑

Warm Standby
→ 비용 ↑
→ RTO ↓
```

## SAA 판단

```text
재해 시 빠르게 scale-up해서 서비스 복구
→ Warm Standby

전체 architecture는 이미 살아 있어야 함
→ Warm Standby
```
