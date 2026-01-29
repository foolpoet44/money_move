# Money Flow Prediction System - 사용자 매뉴얼

## 📚 목차

1. [시작하기](#1-시작하기)
2. [대시보드 사용법](#2-대시보드-사용법)
3. [API 사용법](#3-api-사용법)
4. [알림 설정](#4-알림-설정)
5. [시나리오별 가이드](#5-시나리오별-가이드)
6. [고급 기능](#6-고급-기능)
7. [FAQ](#7-faq)

---

## 1. 시작하기

### 1.1 최초 설정 (5분)

#### Step 1: API 키 발급

**FRED API (필수)**
```
1. https://fred.stlouisfed.org/ 접속
2. 우측 상단 "My Account" → "API Keys" 클릭
3. "Create API Key" 클릭
4. 생성된 키 복사
```

**Slack Webhook (권장)**
```
1. Slack 워크스페이스에서 Apps 메뉴 열기
2. "Incoming Webhooks" 검색 및 추가
3. 채널 선택 (예: #money-flow-alerts)
4. Webhook URL 복사
```

#### Step 2: 설정 파일 작성

```bash
# 템플릿 복사
cp config/secrets.yaml.example config/secrets.yaml

# 에디터로 열기
notepad config/secrets.yaml  # Windows
```

**최소 설정 (FRED만 사용)**
```yaml
data_sources:
  fred:
    api_key: "YOUR_FRED_API_KEY_HERE"

notifications:
  slack:
    webhook_url: "YOUR_SLACK_WEBHOOK_URL"
    channel: "#money-flow-alerts"
```

#### Step 3: 실행

**Docker 사용 (권장)**
```bash
docker-compose up -d
```

**Python 직접 실행**
```bash
# 가상환경 활성화
.venv\Scripts\activate  # Windows

# 대시보드 실행
streamlit run dashboard/app.py
```

#### Step 4: 접속 확인

```
브라우저에서 http://localhost:8501 접속
```

---

## 2. 대시보드 사용법

### 2.1 화면 구성

```
┌─────────────────────────────────────────────────────────┐
│  Money Flow Prediction System    [Risk Score: 45/100]  │
├─────────────────────────────────────────────────────────┤
│ Sidebar          │  Main Content                        │
│ ┌──────────┐    │  ┌────────────────────────────────┐ │
│ │ Filters  │    │  │  Market Overview               │ │
│ │          │    │  │  - Global Indices Heatmap      │ │
│ │ Settings │    │  │  - Currency Strength Meter     │ │
│ │          │    │  └────────────────────────────────┘ │
│ │ Alerts   │    │  ┌────────────────────────────────┐ │
│ └──────────┘    │  │  Fund Flow Analysis            │ │
│                 │  │  - ETF Flow Chart              │ │
│                 │  │  - Sector Rotation             │ │
│                 │  └────────────────────────────────┘ │
│                 │  ┌────────────────────────────────┐ │
│                 │  │  Active Signals                │ │
│                 │  └────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 2.2 주요 기능

#### Market Overview (시장 개요)

**Risk Score (리스크 점수)**
- 0-20: MINIMAL (최소) - 안정적 시장
- 21-40: LOW (낮음) - 정상 변동
- 41-60: MODERATE (중간) - 주의 필요
- 61-80: HIGH (높음) - 위험 증가
- 81-100: EXTREME (극심) - 위기 상황

**Global Indices Heatmap**
- 녹색: 상승
- 빨간색: 하락
- 색상 진하기: 변동 폭

**Currency Strength Meter**
- 각 통화의 상대적 강도 표시
- USD 강세 = 신흥국 압박 신호

#### Fund Flow Analysis (자금 흐름 분석)

**ETF Flow Chart**
```
해석 방법:
- 녹색 막대: 순유입 (자금 유입)
- 빨간색 막대: 순유출 (자금 유출)
- 막대 크기: 유출입 규모

주의 신호:
- TLT(장기채) 대량 유입 + SPY(주식) 유출 = 리스크오프
- HYG(하이일드) 유출 = 신용 위험 증가
- EWY(한국) 3일 연속 유출 = 한국 자금 이탈
```

**Sector Rotation Diagram**
- 자금이 어느 섹터로 이동하는지 시각화
- 방어적 섹터(헬스케어, 유틸리티) 유입 = 경기 둔화 우려
- 경기민감 섹터(금융, 에너지) 유입 = 경기 회복 기대

#### Signals & Alerts (신호 및 알림)

**신호 해석**

| 시나리오 | 의미 | 대응 |
|---------|------|------|
| korea_capital_outflow | 한국 자금 유출 | 원화 자산 비중 축소 |
| risk_off_transition | 리스크오프 전환 | 주식 비중 축소, 현금 확보 |
| liquidity_crisis | 유동성 위기 | 극도로 보수적 포지션 |
| yield_curve_inversion | 수익률 곡선 역전 | 경기 침체 대비 |
| credit_stress | 신용 경색 | 하이일드 회피 |

**Confidence (신뢰도)**
- 70% 이상: 높은 신뢰도, 즉시 대응 고려
- 50-70%: 중간 신뢰도, 모니터링 강화
- 50% 미만: 낮은 신뢰도, 참고용

#### Predictions (예측)

**Flow Direction (자금 흐름 방향)**
- INFLOW: 유입 예상
- NEUTRAL: 중립
- OUTFLOW: 유출 예상

**확률 분포**
```
예시:
Outflow: 65%
Neutral: 25%
Inflow: 10%

→ 65% 확률로 자금 유출 예상
```

### 2.3 필터 사용

**사이드바 필터**

```python
# 자산 클래스 필터
- All: 전체 보기
- Equity: 주식 관련만
- Bond: 채권 관련만
- Forex: 통화 관련만
- Derivatives: 파생상품만

# 시간 범위
- 1 Day: 최근 1일
- 1 Week: 최근 1주
- 1 Month: 최근 1개월
- Custom: 사용자 지정

# 심각도 필터
- All: 모든 알림
- WARNING+: WARNING 이상만
- CRITICAL+: CRITICAL 이상만
```

---

## 3. API 사용법

### 3.1 API 서버 실행

```bash
# 개발 모드
uvicorn src.api.main:app --reload --port 8000

# 프로덕션 모드
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 3.2 주요 엔드포인트

#### Market Overview

```bash
# 시장 전체 개요
curl http://localhost:8000/api/v1/market/overview

# 응답 예시
{
  "timestamp": "2024-01-29T13:00:00Z",
  "risk_score": 45.2,
  "risk_level": "MODERATE",
  "market_regime": "normal_volatility",
  "key_indicators": {
    "vix": 18.5,
    "dxy": 103.2,
    "treasury_10y": 4.15
  }
}
```

#### Active Signals

```bash
# 모든 활성 신호
curl http://localhost:8000/api/v1/signals

# 심각도 필터링
curl http://localhost:8000/api/v1/signals?severity=high

# 응답 예시
{
  "signals": [
    {
      "id": "sig_20240129_001",
      "timestamp": "2024-01-29T12:30:00Z",
      "scenario": "korea_capital_outflow",
      "severity": "high",
      "confidence": 0.85,
      "triggers": [
        "한미 금리차 -0.6%p",
        "USDKRW +1.2% (1일)",
        "EWY 3일 연속 순유출"
      ],
      "recommendation": "원화 자산 비중 축소 검토"
    }
  ]
}
```

#### Predictions

```bash
# 24시간 예측
curl http://localhost:8000/api/v1/predictions?horizon=24h

# 응답 예시
{
  "horizon": "24h",
  "direction": "outflow",
  "confidence": 0.72,
  "probability_distribution": {
    "outflow": 0.72,
    "neutral": 0.20,
    "inflow": 0.08
  },
  "model_version": "ensemble_v1.2"
}
```

#### ETF Flow Data

```bash
# 특정 ETF 흐름
curl http://localhost:8000/api/v1/etf/flow?symbol=SPY&days=7

# 응답 예시
{
  "symbol": "SPY",
  "period": "7d",
  "net_flow_7d": -1250000000,  # -$1.25B
  "daily_flows": [
    {"date": "2024-01-29", "flow": -350000000},
    {"date": "2024-01-28", "flow": -200000000},
    ...
  ],
  "trend": "outflow_accelerating"
}
```

### 3.3 Python SDK

```python
from src.api.client import MoneyFlowClient

# 클라이언트 초기화
client = MoneyFlowClient(base_url="http://localhost:8000")

# 1. 시장 개요 조회
overview = client.get_market_overview()
print(f"Risk Score: {overview['risk_score']}")

if overview['risk_score'] > 60:
    print("⚠️ High risk detected!")

# 2. 활성 신호 조회
signals = client.get_signals(severity="high")
for signal in signals:
    print(f"[{signal['severity'].upper()}] {signal['scenario']}")
    print(f"  Confidence: {signal['confidence']:.0%}")
    print(f"  Action: {signal['recommendation']}")

# 3. 예측 조회
pred = client.get_predictions(horizon="24h")
print(f"\n24h Forecast: {pred['direction'].upper()}")
print(f"Confidence: {pred['confidence']:.0%}")

# 4. ETF 흐름 조회
etf_flow = client.get_etf_flow(symbol="SPY", days=7)
if etf_flow['net_flow_7d'] < -1e9:  # -$1B 이상 유출
    print("⚠️ SPY experiencing significant outflow!")

# 5. 여러 ETF 비교
symbols = ["SPY", "TLT", "HYG"]
flows = {s: client.get_etf_flow(s, days=3) for s in symbols}

for symbol, data in flows.items():
    flow = data['net_flow_3d']
    print(f"{symbol}: ${flow/1e9:.2f}B")
```

---

## 4. 알림 설정

### 4.1 임계값 설정

`config/config.yaml` 편집:

```yaml
alerts:
  # VIX 임계값
  vix_threshold: 30  # VIX > 30 시 알림
  
  # 환율 변동 임계값
  usdkrw_change_threshold: 1.0  # 1일 1% 이상 변동 시
  
  # ETF 유출 임계값
  etf_outflow_threshold: -100000000  # -$100M 이상 유출 시
  
  # 신용 스프레드
  credit_spread_threshold: 500  # 500bp 이상 시
  
  # 수익률 곡선
  yield_curve_inversion_threshold: -10  # -10bp 이상 역전 시
```

### 4.2 알림 채널 설정

```yaml
notification_channels:
  # 심각도별 채널
  INFO:
    - slack
  
  WARNING:
    - slack
    - email
  
  CRITICAL:
    - slack
    - email
    - telegram
  
  EMERGENCY:
    - slack
    - email
    - telegram
    - sms  # 설정 시
```

### 4.3 알림 빈도 제어

```yaml
alerts:
  # 시간당 최대 알림 수
  rate_limit: 10
  
  # 동일 알림 재전송 간격 (초)
  cooldown_period: 300  # 5분
  
  # 조용한 시간 (선택사항)
  quiet_hours:
    enabled: true
    start: "22:00"
    end: "08:00"
    timezone: "Asia/Seoul"
```

### 4.4 Slack 알림 커스터마이징

```python
# src/alerts/notifiers/slack_notifier.py

# 알림 메시지 템플릿
SLACK_MESSAGE_TEMPLATE = {
    "CRITICAL": {
        "color": "#FF0000",
        "icon": "🚨",
        "title": "CRITICAL ALERT"
    },
    "WARNING": {
        "color": "#FFA500",
        "icon": "⚠️",
        "title": "Warning"
    },
    "INFO": {
        "color": "#0000FF",
        "icon": "ℹ️",
        "title": "Info"
    }
}
```

---

## 5. 시나리오별 가이드

### 5.1 한국 자금 유출 감지

**신호 체인**
```
1. 한미 금리차 역전 (-0.5%p 이상)
   ↓
2. USDKRW 급등 (1일 +1% 이상)
   ↓
3. EWY(한국 ETF) 3일 연속 순유출
   ↓
4. KOSPI 외국인 순매도 가속
   ↓
[결론] 외국인 자금 이탈 본격화
```

**대시보드 확인 사항**
- Market Overview → USDKRW 차트
- Fund Flow → EWY 유출입
- Signals → "korea_capital_outflow" 신호

**대응 전략**
```
Confidence 70% 이상:
→ 원화 자산 비중 10-20% 축소
→ 달러 헤지 검토

Confidence 85% 이상:
→ 원화 자산 비중 30-50% 축소
→ 적극적 달러 헤지
```

### 5.2 리스크오프 전환

**신호 조합**
```
1. VIX 20 → 30 급등
2. TLT(장기채 ETF) 대량 유입
3. HYG(하이일드) 스프레드 확대
4. 금 가격 상승 + 달러 강세 동시 발생
```

**대시보드 확인**
- Market Overview → VIX 게이지
- Fund Flow → TLT vs SPY 흐름 비교
- Signals → "risk_off_transition"

**대응 전략**
```
초기 단계 (VIX 20-25):
→ 주식 비중 10% 축소
→ 현금/단기채 확보

중기 단계 (VIX 25-30):
→ 주식 비중 20-30% 축소
→ 방어적 섹터로 이동

심화 단계 (VIX 30+):
→ 주식 비중 50% 이상 축소
→ 현금 최대 확보
→ 변동성 낮아질 때까지 대기
```

### 5.3 유동성 위기 조기 감지

**위험 신호**
```
1. LIBOR-OIS 스프레드 급등
2. 레포 금리 스파이크
3. MOVE 지수 (채권 변동성) 급등
4. 회사채 발행 급감
```

**대시보드 확인**
- Market Overview → MOVE 지수
- Fund Flow → 회사채 ETF (LQD, HYG) 유출
- Signals → "liquidity_crisis"

**대응 전략**
```
⚠️ 극도로 보수적 포지션
→ 현금 확보 최우선
→ 단기 국채만 보유
→ 위험자산 최소화
→ 2008년 금융위기 재현 가능성 대비
```

---

## 6. 고급 기능

### 6.1 백테스팅

```python
from src.analysis.backtester import Backtester

# 백테스터 초기화
backtester = Backtester(
    start_date="2020-01-01",
    end_date="2023-12-31"
)

# 신호 정확도 테스트
results = backtester.test_signal("korea_capital_outflow")

print(f"Precision: {results['precision']:.2%}")
print(f"Recall: {results['recall']:.2%}")
print(f"F1 Score: {results['f1_score']:.2%}")

# 예측 모델 성능 테스트
model_results = backtester.test_prediction_model(
    model="ensemble",
    horizon="24h"
)

print(f"Accuracy: {model_results['accuracy']:.2%}")
print(f"Sharpe Ratio: {model_results['sharpe_ratio']:.2f}")
```

### 6.2 커스텀 신호 생성

```python
# config/custom_signals.yaml

custom_signals:
  my_scenario:
    name: "My Custom Scenario"
    conditions:
      - indicator: "vix"
        operator: ">"
        threshold: 25
      - indicator: "spy_flow_3d"
        operator: "<"
        threshold: -500000000
      - indicator: "dxy"
        operator: ">"
        threshold: 105
    
    required_conditions: 2  # 3개 중 2개 이상 충족
    
    severity: "high"
    recommendation: "Custom action here"
```

### 6.3 데이터 내보내기

```python
from src.storage.exporter import DataExporter

exporter = DataExporter()

# CSV로 내보내기
exporter.export_signals_to_csv(
    start_date="2024-01-01",
    end_date="2024-01-31",
    output_file="signals_jan2024.csv"
)

# Excel로 내보내기
exporter.export_market_data_to_excel(
    symbols=["SPY", "TLT", "DXY"],
    output_file="market_data.xlsx"
)

# JSON으로 내보내기
exporter.export_predictions_to_json(
    output_file="predictions.json"
)
```

---

## 7. FAQ

### Q1: 대시보드가 업데이트되지 않아요

**A:** 
```bash
# 1. 데이터 수집 상태 확인
curl http://localhost:8000/api/v1/health

# 2. 로그 확인
tail -f logs/collector.log

# 3. 수동 새로고침
# 대시보드 우측 상단 "Rerun" 버튼 클릭
```

### Q2: API 키가 작동하지 않아요

**A:**
```bash
# 1. secrets.yaml 확인
cat config/secrets.yaml

# 2. API 키 유효성 테스트
python scripts/test_api_keys.py

# 3. FRED API 사용량 확인
# https://fred.stlouisfed.org/docs/api/api_key.html
```

### Q3: 알림이 너무 많이 와요

**A:**
```yaml
# config/config.yaml 수정

alerts:
  # 임계값 높이기
  vix_threshold: 35  # 30 → 35
  
  # 빈도 제한 강화
  rate_limit: 5  # 10 → 5
  cooldown_period: 600  # 300 → 600 (10분)
  
  # 심각도 필터링
  min_severity: "WARNING"  # INFO 알림 제외
```

### Q4: 메모리 사용량이 너무 높아요

**A:**
```yaml
# config/config.yaml 수정

performance:
  # 배치 크기 줄이기
  batch_size: 50  # 100 → 50
  
  # 워커 수 줄이기
  max_workers: 2  # 4 → 2
  
  # 캐시 TTL 줄이기
  cache_ttl: 180  # 300 → 180
```

### Q5: 예측 정확도를 높이려면?

**A:**
```python
# 1. 더 많은 과거 데이터 수집
python scripts/backfill_data.py --days 365

# 2. 모델 재학습
python scripts/train_models.py --epochs 100

# 3. 앙상블 가중치 조정
# config/config.yaml
analysis:
  prediction:
    ensemble_weights:
      lstm: 0.3
      transformer: 0.7  # Transformer 비중 증가
```

### Q6: 특정 시장만 모니터링하고 싶어요

**A:**
```yaml
# config/config.yaml

data_collection:
  enabled_markets:
    bonds: true
    forex: true
    etf: true
    derivatives: false  # 파생상품 비활성화
  
  symbols:
    # 한국 관련만
    forex: ["USDKRW"]
    etf: ["EWY"]
```

### Q7: 과거 데이터를 분석하고 싶어요

**A:**
```python
from src.analysis.historical_analyzer import HistoricalAnalyzer

analyzer = HistoricalAnalyzer()

# 특정 기간 분석
results = analyzer.analyze_period(
    start_date="2020-03-01",  # COVID-19 시작
    end_date="2020-04-01"
)

print(f"Period: {results['period']}")
print(f"Max Risk Score: {results['max_risk_score']}")
print(f"Major Signals: {results['major_signals']}")
print(f"Market Regime: {results['market_regime']}")

# 유사 패턴 찾기
similar = analyzer.find_similar_periods(
    reference_date="2020-03-15",
    window_days=30
)
```

---

## 📞 추가 지원

- **문서**: [README.md](README.md)
- **시스템 설계**: [system_design.md](system_design.md)
- **이슈 리포트**: GitHub Issues
- **커뮤니티**: GitHub Discussions

---

**Happy Trading! 📊💰**
