# 💰 Money Flow Prediction System

> **"물의 흐름을 읽는 자가 시장을 지배한다"**

실시간 글로벌 자금 흐름을 추적하고 AI 기반 예측으로 시장의 다음 움직임을 포착하는 통합 금융 분석 플랫폼

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active%20Development-orange.svg)]()

---

## 📋 목차

- [개요](#-개요)
- [주요 기능](#-주요-기능)
- [시스템 아키텍처](#-시스템-아키텍처)
- [빠른 시작](#-빠른-시작)
- [설치 가이드](#-설치-가이드)
- [사용 방법](#-사용-방법)
- [데이터 소스](#-데이터-소스)
- [설정](#-설정)
- [API 문서](#-api-문서)
- [대시보드](#-대시보드)
- [개발 가이드](#-개발-가이드)
- [테스트](#-테스트)
- [배포](#-배포)
- [문제 해결](#-문제-해결)
- [기여하기](#-기여하기)
- [라이선스](#-라이선스)

---

## 🎯 개요

Money Flow Prediction System은 글로벌 자금시장의 흐름을 실시간으로 추적하고, 머신러닝 기반 예측 모델을 통해 자금 이동 방향을 예측하는 통합 플랫폼입니다.

### 핵심 철학

자금시장에서 돈의 이동은 세 가지 본능을 따릅니다:

1. **수익률 추구** (Return Seeking) - 더 높은 수익을 찾아 이동
2. **위험 회피** (Risk Aversion) - 불확실성 시 안전자산으로 이동
3. **유동성 추구** (Liquidity Preference) - 위기 시 환금성 높은 자산 선호

본 시스템은 이러한 자금의 흐름을 **조기에 감지**하고 **방향을 예측**하여 투자 의사결정을 지원합니다.

### 왜 이 시스템이 필요한가?

- ✅ **조기 경보**: 자금 흐름 이상 징후를 실시간으로 탐지
- ✅ **데이터 통합**: 분산된 시장 데이터를 하나의 맥락으로 통합
- ✅ **AI 예측**: LSTM/Transformer 기반 시계열 예측
- ✅ **자동화**: 24/7 무중단 모니터링 및 알림
- ✅ **시나리오 분석**: 과거 유사 사례 매칭 및 대응 전략 제시

---

## 🚀 주요 기능

### 1. 실시간 데이터 수집
- 📊 **채권 시장**: 미국 국채 수익률, 회사채 스프레드, 신용 스프레드
- 💱 **통화 시장**: 주요 통화쌍, 달러 인덱스(DXY), 이머징 통화
- 📈 **ETF 자금 흐름**: 주식/채권/섹터/국가별 ETF 순유출입
- 📉 **파생상품**: VIX, MOVE, Put/Call Ratio, 옵션 플로우

### 2. 이상 징후 탐지
- 🔍 **통계적 방법**: Z-Score, IQR 기반 이상치 탐지
- 🤖 **머신러닝**: Isolation Forest, Autoencoder 기반 이상 탐지
- 📊 **패턴 매칭**: 과거 유사 패턴 식별 및 비교

### 3. 자금 흐름 예측
- 🧠 **LSTM 모델**: 단기 시계열 예측 (24-48시간)
- 🔮 **Transformer 모델**: 장기 의존성 포착 (1주일)
- 🎯 **앙상블 예측**: 다중 모델 결합으로 정확도 향상

### 4. 실시간 알림
- 📧 **이메일**: 중요 신호 발생 시 이메일 알림
- 💬 **Slack**: 실시간 Slack 채널 알림
- 📱 **Telegram**: 모바일 푸시 알림 (선택사항)
- 🔔 **심각도 기반**: INFO/WARNING/CRITICAL/EMERGENCY 레벨 구분

### 5. 인터랙티브 대시보드
- 📊 **실시간 차트**: Plotly 기반 인터랙티브 시각화
- 🗺️ **자금 흐름 맵**: 국가/섹터별 자금 이동 시각화
- 📈 **예측 결과**: 확률 분포 및 신뢰 구간 표시
- ⚡ **실시간 업데이트**: 1분 단위 자동 갱신

---

## 🏗️ 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                        Data Sources                              │
│  Yahoo Finance │ FRED │ Polygon.io │ Alpha Vantage │ News APIs  │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Data Collection Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │Bond Collector│  │Forex Collector│  │ ETF Collector│          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Stream Processing Layer                         │
│  Real-time Normalization │ Feature Engineering │ Buffering      │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Storage Layer                               │
│  InfluxDB (Time-Series) │ Redis (Cache) │ PostgreSQL (Meta)     │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Analysis Engine                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Anomaly    │  │   Signal     │  │  ML Prediction│          │
│  │   Detection  │  │  Generator   │  │    Models     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Alert & Action Layer                          │
│  Risk Scoring │ Scenario Matching │ Alert Dispatch              │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Presentation Layer                             │
│  Dashboard │ REST API │ Mobile App │ Notifications              │
└─────────────────────────────────────────────────────────────────┘
```

---

## ⚡ 빠른 시작

### 사전 요구사항

- Python 3.10 이상
- Docker & Docker Compose (선택사항, 권장)
- Git
- **Firebase CLI** (Firebase 배포용)
- **Google Cloud SDK** (Firebase 배포용)

### 🔥 Firebase 배포 (무료 티어, 권장)

```bash
# 1. 저장소 클론
git clone https://github.com/your-username/money_move.git
cd money_move

# 2. Firebase 초기 설정
./scripts/setup_firebase.sh
# 프롬프트에 따라 Firebase 프로젝트 ID 입력

# 3. API 키 설정
cp config/secrets.yaml.example config/secrets.yaml
# FRED API 키 입력 (https://fred.stlouisfed.org/)

# 4. Firebase 배포
./scripts/deploy_firebase.sh

# 5. 배포 완료 후 URL 확인
# https://YOUR_PROJECT_ID.web.app
```

> **🎯 Firebase 배포의 장점:**
> - ✅ **완전 무료**: 무료 티어 범위 내에서 운영 가능
> - ✅ **자동 스케일링**: 트래픽에 따라 자동 확장
> - ✅ **HTTPS 기본 제공**: 별도 설정 없이 보안 연결
> - ✅ **글로벌 CDN**: 전 세계 어디서나 빠른 접속
> 
> 자세한 설정 가이드는 [FIREBASE_SETUP.md](FIREBASE_SETUP.md)를 참조하세요.

---

### 1분 설치 (Docker 사용 - 로컬 개발용)

```bash
# 1. 저장소 클론
git clone https://github.com/your-username/money_move.git
cd money_move

# 2. 환경 설정 파일 복사
cp config/secrets.yaml.example config/secrets.yaml

# 3. secrets.yaml 편집 (최소한 FRED API 키 필요)
# 텍스트 에디터로 config/secrets.yaml 열어서 API 키 입력

# 4. Docker Compose로 전체 스택 실행
docker-compose up -d

# 5. 대시보드 접속
# 브라우저에서 http://localhost:8501 열기
```

### 로컬 설치 (Python 환경)

```bash
# 1. 저장소 클론
git clone https://github.com/your-username/money_move.git
cd money_move

# 2. 가상환경 생성 및 활성화
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 환경 설정
cp config/secrets.yaml.example config/secrets.yaml
# secrets.yaml 파일 편집하여 API 키 입력

# 5. 데이터베이스 초기화 (선택사항)
python scripts/setup_db.py

# 6. 대시보드 실행
streamlit run dashboard/app.py
```


---

## 📦 설치 가이드

### 상세 설치 단계

#### 1. Python 환경 설정

```bash
# Python 버전 확인
python --version  # 3.10 이상이어야 함

# 가상환경 생성
python -m venv .venv

# 가상환경 활성화
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Windows CMD
.venv\Scripts\activate.bat
# macOS/Linux
source .venv/bin/activate
```

#### 2. 의존성 설치

```bash
# 기본 의존성 설치
pip install -r requirements.txt

# 개발 의존성 추가 설치 (선택사항)
pip install -r requirements-dev.txt
```

#### 3. 데이터베이스 설정

**Option A: Docker 사용 (권장)**

```bash
# Docker Compose로 InfluxDB, Redis, PostgreSQL 실행
docker-compose up -d influxdb redis postgres

# InfluxDB 초기 설정
# 브라우저에서 http://localhost:8086 접속
# Organization: money_flow
# Bucket: market_data
# Token 생성 후 config/secrets.yaml에 저장
```

**Option B: 로컬 설치**

```bash
# InfluxDB 설치 (Windows)
# https://portal.influxdata.com/downloads/ 에서 다운로드

# Redis 설치 (Windows)
# https://github.com/microsoftarchive/redis/releases 에서 다운로드

# PostgreSQL 설치 (선택사항)
# https://www.postgresql.org/download/ 에서 다운로드
```

#### 4. API 키 발급

**필수: FRED API Key**
1. https://fred.stlouisfed.org/ 접속
2. 계정 생성 (무료)
3. API Keys 메뉴에서 키 발급
4. `config/secrets.yaml`의 `data_sources.fred.api_key`에 입력

**선택사항: 기타 API Keys**
- Polygon.io: https://polygon.io/ (프리미엄 데이터)
- Alpha Vantage: https://www.alphavantage.co/ (무료 티어 제한적)

#### 5. 알림 설정

**Slack Webhook (권장)**
1. Slack 워크스페이스에서 앱 추가
2. Incoming Webhooks 활성화
3. Webhook URL 생성
4. `config/secrets.yaml`의 `notifications.slack.webhook_url`에 입력

**이메일 알림 (Gmail 예시)**
1. Gmail 계정에서 2단계 인증 활성화
2. 앱 비밀번호 생성: https://myaccount.google.com/apppasswords
3. `config/secrets.yaml`의 `notifications.email` 섹션 설정

---

## 🎮 사용 방법

### 대시보드 사용

#### 1. 대시보드 실행

```bash
# Streamlit 대시보드 실행
streamlit run dashboard/app.py

# 브라우저에서 자동으로 열림 (http://localhost:8501)
```

#### 2. 대시보드 주요 기능

**Market Overview (시장 개요)**
- 글로벌 지수 히트맵
- 통화 강도 미터
- 변동성 게이지
- 실시간 업데이트

**Fund Flow Analysis (자금 흐름 분석)**
- ETF 자금 흐름 차트
- 섹터 로테이션 Sankey 다이어그램
- 지리적 자금 흐름 맵

**Signals & Alerts (신호 및 알림)**
- 활성 신호 테이블
- 알림 타임라인
- 시나리오 확률 차트

**Predictions (예측)**
- 자금 흐름 방향 예측
- 신뢰 구간
- 유사 과거 사례

#### 3. 필터 및 설정

사이드바에서 다음을 조정할 수 있습니다:
- 자산 클래스 필터 (주식/채권/통화/파생상품)
- 시간 범위 (1일/1주일/1개월)
- 알림 심각도 (INFO/WARNING/CRITICAL)
- 알림 임계값 설정

### API 사용

#### 1. API 서버 실행

```bash
# FastAPI 서버 실행
uvicorn src.api.main:app --reload --port 8000

# API 문서 확인
# 브라우저에서 http://localhost:8000/docs 접속
```

#### 2. API 엔드포인트

**시장 개요 조회**
```bash
curl http://localhost:8000/api/v1/market/overview
```

**활성 신호 조회**
```bash
# 모든 신호
curl http://localhost:8000/api/v1/signals

# 심각도 필터링
curl http://localhost:8000/api/v1/signals?severity=high

# 시간 범위 지정
curl "http://localhost:8000/api/v1/signals?start_time=2024-01-01T00:00:00Z&end_time=2024-01-02T00:00:00Z"
```

**예측 결과 조회**
```bash
# 24시간 예측
curl http://localhost:8000/api/v1/predictions?horizon=24h

# 1주일 예측
curl http://localhost:8000/api/v1/predictions?horizon=1w
```

**ETF 자금 흐름 조회**
```bash
# 특정 ETF
curl http://localhost:8000/api/v1/etf/flow?symbol=SPY

# 여러 ETF
curl "http://localhost:8000/api/v1/etf/flow?symbols=SPY,QQQ,TLT"
```

#### 3. Python SDK 사용

```python
from src.api.client import MoneyFlowClient

# 클라이언트 초기화
client = MoneyFlowClient(base_url="http://localhost:8000")

# 시장 개요 조회
overview = client.get_market_overview()
print(f"Risk Score: {overview['risk_score']}")
print(f"Market Regime: {overview['market_regime']}")

# 신호 조회
signals = client.get_signals(severity="high")
for signal in signals:
    print(f"{signal['timestamp']}: {signal['scenario']} - {signal['recommendation']}")

# 예측 조회
predictions = client.get_predictions(horizon="24h")
print(f"Direction: {predictions['direction']}")
print(f"Confidence: {predictions['confidence']:.2%}")

# ETF 흐름 조회
etf_flow = client.get_etf_flow(symbol="SPY", days=7)
print(f"7-day net flow: ${etf_flow['net_flow_7d']:,.0f}")
```

### 알림 설정

#### 임계값 설정

`config/config.yaml` 파일에서 알림 임계값을 조정:

```yaml
alerts:
  # VIX 임계값
  vix_threshold: 30
  
  # 환율 변동 임계값 (%)
  usdkrw_change_threshold: 1.0
  
  # ETF 유출 임계값 (달러)
  etf_outflow_threshold: -100000000  # -$100M
  
  # 신용 스프레드 임계값 (bp)
  credit_spread_threshold: 500
  
  # 수익률 곡선 역전 임계값 (bp)
  yield_curve_inversion_threshold: -10
```

#### 알림 채널 설정

```yaml
notification_channels:
  # 심각도별 채널 설정
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
    - sms
```

---

## 📊 데이터 소스

### 무료 데이터 소스

#### 1. Yahoo Finance (yfinance)
- **데이터**: 주식, ETF, 환율, 지수
- **빈도**: 1분 단위 (지연: 15-20분)
- **비용**: 무료
- **제한**: 2000 requests/hour
- **설정**: API 키 불필요

```python
# 사용 예시
import yfinance as yf

# ETF 데이터 조회
spy = yf.Ticker("SPY")
hist = spy.history(period="1d", interval="1m")
```

#### 2. FRED (Federal Reserve Economic Data)
- **데이터**: 미국 국채 수익률, 경제 지표
- **빈도**: 일별
- **비용**: 무료
- **제한**: 120 requests/minute
- **설정**: API 키 필요 (무료 발급)

```python
# 사용 예시
from fredapi import Fred

fred = Fred(api_key='YOUR_API_KEY')
# 10년물 국채 수익률
treasury_10y = fred.get_series('DGS10')
```

#### 3. Alpha Vantage
- **데이터**: 주식, 외환, 암호화폐, 기술 지표
- **빈도**: 1분 단위
- **비용**: 무료 (제한적)
- **제한**: 5 requests/minute (무료 티어)
- **설정**: API 키 필요

### 프리미엄 데이터 소스 (선택사항)

#### 1. Polygon.io
- **데이터**: 실시간 주식, 옵션, 외환, 암호화폐
- **빈도**: 실시간
- **비용**: $199/month (Starter)
- **장점**: 높은 품질, 낮은 지연시간

#### 2. Quandl/Nasdaq Data Link
- **데이터**: 대체 데이터, 선물, 옵션
- **빈도**: 실시간
- **비용**: 데이터셋별 상이
- **장점**: 독점 데이터셋 제공

### 수집 데이터 목록

#### 채권 시장
```python
BOND_TICKERS = {
    "us_treasuries": ["^IRX", "^FVX", "^TNX", "^TYX"],  # 3M, 5Y, 10Y, 30Y
    "bond_etfs": ["TLT", "IEF", "SHY", "TIP"],
    "corporate": ["LQD", "HYG"],  # Investment Grade, High Yield
}
```

#### 통화 시장
```python
FOREX_PAIRS = {
    "major": ["DXY", "EURUSD", "USDJPY", "GBPUSD"],
    "emerging": ["USDKRW", "USDCNY", "USDINR", "USDBRL"],
    "commodity": ["AUDUSD", "NZDUSD", "USDCAD"],
}
```

#### ETF 자금 흐름
```python
ETF_UNIVERSE = {
    "equity": ["SPY", "QQQ", "IWM", "DIA"],
    "sectors": ["XLF", "XLE", "XLV", "XLK", "XLI", "XLP", "XLU", "XLB"],
    "international": ["EWY", "EWJ", "EEM", "VWO", "EFA"],
    "volatility": ["VXX", "UVXY"],
}
```

#### 파생상품
```python
DERIVATIVES = {
    "volatility": ["^VIX", "^VVIX", "^MOVE"],
    "futures": ["ES=F", "NQ=F", "YM=F", "RTY=F"],  # E-mini futures
}
```

---

## ⚙️ 설정

### 환경 변수

`.env` 파일 또는 환경 변수로 설정 가능:

```bash
# 환경 설정
ENVIRONMENT=production  # development, staging, production

# 로그 레벨
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# 데이터베이스
INFLUXDB_URL=http://localhost:8086
INFLUXDB_ORG=money_flow
INFLUXDB_BUCKET=market_data

REDIS_HOST=localhost
REDIS_PORT=6379

# API 설정
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# 대시보드
DASHBOARD_PORT=8501
DASHBOARD_UPDATE_INTERVAL=60  # seconds
```

### 설정 파일 구조

```
config/
├── config.yaml          # 메인 설정 파일
├── secrets.yaml         # 민감 정보 (gitignore)
├── secrets.yaml.example # 템플릿
└── logging.yaml         # 로깅 설정
```

### config.yaml 주요 설정

```yaml
# 데이터 수집 설정
data_collection:
  update_intervals:
    bonds: 60  # seconds
    forex: 30
    etf: 300
    derivatives: 60
  
  retry_policy:
    max_retries: 3
    backoff_factor: 2

# 분석 설정
analysis:
  anomaly_detection:
    z_score_threshold: 3.0
    isolation_forest_contamination: 0.1
  
  prediction:
    model_type: "ensemble"  # lstm, transformer, ensemble
    horizon_default: "24h"
    confidence_threshold: 0.7

# 알림 설정
alerts:
  enabled: true
  rate_limit: 10  # max alerts per hour
  cooldown_period: 300  # seconds between same alert

# 성능 설정
performance:
  cache_ttl: 300  # seconds
  batch_size: 100
  max_workers: 4
```

---

## 📚 API 문서

### REST API

API 서버 실행 후 자동 생성된 문서 확인:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 주요 엔드포인트

#### Market Data

```
GET /api/v1/market/overview
GET /api/v1/market/bonds
GET /api/v1/market/forex
GET /api/v1/market/etf
```

#### Signals & Alerts

```
GET /api/v1/signals
GET /api/v1/signals/{signal_id}
POST /api/v1/signals/subscribe
DELETE /api/v1/signals/subscribe/{subscription_id}
```

#### Predictions

```
GET /api/v1/predictions
GET /api/v1/predictions/flow-direction
GET /api/v1/predictions/scenarios
```

#### Analytics

```
GET /api/v1/analytics/risk-score
GET /api/v1/analytics/correlation
GET /api/v1/analytics/historical-patterns
```

자세한 API 문서는 [MANUAL.md](MANUAL.md)를 참조하세요.

---

## 📊 대시보드

### 대시보드 구성

#### 1. Market Overview (시장 개요)
- 실시간 리스크 스코어
- 글로벌 지수 히트맵
- 통화 강도 미터
- VIX 게이지

#### 2. Fund Flow Analysis (자금 흐름 분석)
- ETF 순유출입 차트
- 섹터 로테이션 다이어그램
- 국가별 자금 흐름 맵
- 크로스 마켓 상관관계

#### 3. Signals & Alerts (신호 및 알림)
- 활성 신호 테이블
- 신호 타임라인
- 시나리오 확률 분포
- 과거 신호 성과

#### 4. Predictions (예측)
- 24시간 자금 흐름 예측
- 신뢰 구간 차트
- 유사 과거 사례
- 모델 성능 지표

### 대시보드 커스터마이징

`dashboard/config.py`에서 대시보드 레이아웃 수정:

```python
DASHBOARD_CONFIG = {
    "theme": "dark",  # light, dark
    "update_interval": 60,  # seconds
    "charts": {
        "default_timeframe": "1d",
        "color_scheme": "viridis",
    },
    "widgets": {
        "risk_score": {"enabled": True, "position": "top"},
        "etf_flow": {"enabled": True, "position": "main"},
        "signals": {"enabled": True, "position": "sidebar"},
    }
}
```

---

## 🛠️ 개발 가이드

### 프로젝트 구조

```
money_move/
├── src/                        # 소스 코드
│   ├── data_collection/        # 데이터 수집
│   │   ├── collectors/         # 개별 수집기
│   │   │   ├── base_collector.py
│   │   │   ├── fred_collector.py
│   │   │   ├── yahoo_collector.py
│   │   │   └── etf_flow_collector.py
│   │   └── scheduler.py        # 수집 스케줄러
│   │
│   ├── processing/             # 데이터 처리
│   │   ├── stream_processor.py # 실시간 스트림 처리
│   │   ├── normalizer.py       # 데이터 정규화
│   │   └── feature_engineer.py # 피처 엔지니어링
│   │
│   ├── analysis/               # 분석 엔진
│   │   ├── anomaly_detector.py # 이상 탐지
│   │   ├── signal_generator.py # 신호 생성
│   │   └── pattern_matcher.py  # 패턴 매칭
│   │
│   ├── models/                 # ML 모델
│   │   ├── lstm_predictor.py   # LSTM 모델
│   │   ├── transformer_predictor.py
│   │   └── ensemble.py         # 앙상블 모델
│   │
│   ├── alerts/                 # 알림 시스템
│   │   ├── alert_engine.py     # 알림 엔진
│   │   ├── notifiers/          # 알림 채널
│   │   │   ├── email_notifier.py
│   │   │   ├── slack_notifier.py
│   │   │   └── telegram_notifier.py
│   │   └── risk_scorer.py      # 리스크 점수
│   │
│   ├── storage/                # 데이터베이스
│   │   ├── influxdb_client.py  # InfluxDB 클라이언트
│   │   ├── redis_client.py     # Redis 클라이언트
│   │   └── models.py           # 데이터 모델
│   │
│   └── api/                    # REST API
│       ├── main.py             # FastAPI 앱
│       ├── routes/             # API 라우트
│       └── schemas.py          # Pydantic 스키마
│
├── dashboard/                  # Streamlit 대시보드
│   ├── app.py                  # 메인 앱
│   ├── components/             # UI 컴포넌트
│   │   ├── market_overview.py
│   │   ├── fund_flow.py
│   │   ├── signals.py
│   │   └── predictions.py
│   └── utils/                  # 유틸리티
│
├── tests/                      # 테스트
│   ├── unit/                   # 단위 테스트
│   ├── integration/            # 통합 테스트
│   └── fixtures/               # 테스트 픽스처
│
├── scripts/                    # 유틸리티 스크립트
│   ├── setup_db.py             # DB 초기화
│   ├── backfill_data.py        # 과거 데이터 수집
│   └── train_models.py         # 모델 학습
│
├── config/                     # 설정 파일
│   ├── config.yaml
│   ├── secrets.yaml.example
│   └── logging.yaml
│
├── docker-compose.yml          # Docker Compose 설정
├── Dockerfile                  # Docker 이미지
├── requirements.txt            # Python 의존성
├── .gitignore
├── README.md                   # 이 파일
└── MANUAL.md                   # 사용자 매뉴얼
```

### 코드 스타일

프로젝트는 다음 코드 스타일을 따릅니다:

```bash
# 포맷팅 (Black)
black src/ dashboard/ tests/ --line-length 100

# 린팅 (Flake8)
flake8 src/ dashboard/ tests/ --max-line-length 100

# 타입 체크 (MyPy)
mypy src/ --strict

# Import 정렬 (isort)
isort src/ dashboard/ tests/
```

### 새로운 데이터 수집기 추가

```python
# src/data_collection/collectors/my_collector.py

from .base_collector import BaseCollector
from typing import Dict, List

class MyCollector(BaseCollector):
    """새로운 데이터 소스 수집기"""
    
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
    
    async def collect(self) -> List[Dict]:
        """데이터 수집 구현"""
        # 데이터 수집 로직
        data = await self.fetch_data()
        
        # 정규화
        normalized = self.normalize(data)
        
        return normalized
    
    def normalize(self, data: Dict) -> List[Dict]:
        """데이터 정규화"""
        # 표준 형식으로 변환
        return [
            {
                "timestamp": item["time"],
                "symbol": item["ticker"],
                "value": item["price"],
                "metadata": {...}
            }
            for item in data
        ]
```

### 새로운 신호 추가

```python
# src/analysis/signal_generator.py

def check_my_scenario(self, market_state: Dict) -> bool:
    """새로운 시나리오 체크"""
    conditions = [
        market_state.get("indicator_1") > threshold_1,
        market_state.get("indicator_2") < threshold_2,
        # 추가 조건...
    ]
    
    return sum(conditions) >= required_conditions

# signals 리스트에 추가
if self.check_my_scenario(market_state):
    signals.append({
        "scenario": "my_scenario",
        "severity": "high",
        "confidence": 0.80,
        "triggers": [...],
        "recommendation": "..."
    })
```

---

## 🧪 테스트

### 테스트 실행

```bash
# 전체 테스트 실행
pytest

# 커버리지 포함
pytest --cov=src --cov-report=html --cov-report=term

# 특정 테스트만 실행
pytest tests/unit/test_collectors.py -v

# 마커 기반 실행
pytest -m "not slow"  # 느린 테스트 제외
pytest -m integration  # 통합 테스트만
```

### 테스트 작성

```python
# tests/unit/test_collectors.py

import pytest
from src.data_collection.collectors.fred_collector import FREDCollector

@pytest.fixture
def fred_collector():
    """FRED 수집기 픽스처"""
    return FREDCollector(api_key="test_key")

def test_collect_treasury_yields(fred_collector):
    """국채 수익률 수집 테스트"""
    data = fred_collector.collect_treasury_yields()
    
    assert len(data) > 0
    assert "DGS10" in data
    assert data["DGS10"] > 0

@pytest.mark.asyncio
async def test_async_collect(fred_collector):
    """비동기 수집 테스트"""
    data = await fred_collector.collect_async()
    
    assert isinstance(data, list)
    assert all("timestamp" in item for item in data)
```

---

## 🚀 배포

### Docker 배포

```bash
# 이미지 빌드
docker build -t money-flow:latest .

# 컨테이너 실행
docker run -d \
  --name money-flow \
  -p 8000:8000 \
  -p 8501:8501 \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/data:/app/data \
  money-flow:latest

# Docker Compose 사용
docker-compose up -d --build
```

### 프로덕션 배포 체크리스트

- [ ] 환경 변수 설정 (`ENVIRONMENT=production`)
- [ ] 시크릿 관리 (AWS Secrets Manager, HashiCorp Vault 등)
- [ ] 데이터베이스 백업 설정
- [ ] 모니터링 설정 (Prometheus, Grafana)
- [ ] 로그 집계 (ELK Stack, CloudWatch)
- [ ] SSL/TLS 인증서 설정
- [ ] 방화벽 규칙 설정
- [ ] 자동 재시작 설정 (systemd, supervisor)
- [ ] 알림 채널 테스트
- [ ] 성능 테스트 완료

### 클라우드 배포

**AWS 배포 예시**

```bash
# ECR에 이미지 푸시
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker tag money-flow:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/money-flow:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/money-flow:latest

# ECS 서비스 업데이트
aws ecs update-service --cluster money-flow-cluster --service money-flow-service --force-new-deployment
```

---

## 🔧 문제 해결

### 자주 발생하는 문제

#### 1. API 키 오류

```
Error: FRED API key is invalid
```

**해결 방법:**
- `config/secrets.yaml`에 올바른 API 키가 입력되었는지 확인
- FRED 웹사이트에서 키가 활성화되었는지 확인
- API 사용량 제한을 초과하지 않았는지 확인

#### 2. 데이터베이스 연결 실패

```
Error: Failed to connect to InfluxDB
```

**해결 방법:**
```bash
# InfluxDB 상태 확인
docker ps | grep influxdb

# InfluxDB 재시작
docker-compose restart influxdb

# 로그 확인
docker-compose logs influxdb
```

#### 3. 메모리 부족

```
Error: Out of memory
```

**해결 방법:**
- `config/config.yaml`에서 `batch_size` 줄이기
- `max_workers` 줄이기
- Docker 메모리 제한 늘리기

```yaml
# docker-compose.yml
services:
  app:
    mem_limit: 4g
    memswap_limit: 4g
```

#### 4. 알림이 오지 않음

**체크리스트:**
- [ ] `config/config.yaml`에서 `alerts.enabled: true` 확인
- [ ] Slack Webhook URL이 올바른지 확인
- [ ] 이메일 SMTP 설정 확인
- [ ] 알림 임계값이 너무 높지 않은지 확인
- [ ] 로그에서 에러 메시지 확인

```bash
# 로그 확인
tail -f logs/app.log | grep -i alert
```

### 로그 확인

```bash
# 애플리케이션 로그
tail -f logs/app.log

# 데이터 수집 로그
tail -f logs/collector.log

# 알림 로그
tail -f logs/alerts.log

# Docker 로그
docker-compose logs -f app
```

### 디버그 모드

```bash
# 디버그 모드로 실행
export LOG_LEVEL=DEBUG
python -m src.main

# 또는
LOG_LEVEL=DEBUG streamlit run dashboard/app.py
```

---

## 🤝 기여하기

기여를 환영합니다! 다음 절차를 따라주세요:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 기여 가이드라인

- 코드 스타일 가이드 준수 (Black, Flake8)
- 테스트 작성 (커버리지 80% 이상)
- 문서 업데이트
- 커밋 메시지 규칙 준수 (Conventional Commits)

---

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

---

## 📞 문의 및 지원

- **이슈 트래커**: [GitHub Issues](https://github.com/your-username/money_move/issues)
- **토론**: [GitHub Discussions](https://github.com/your-username/money_move/discussions)
- **이메일**: your-email@example.com

---

## 🙏 감사의 말

이 프로젝트는 다음 오픈소스 프로젝트들을 사용합니다:

- [yfinance](https://github.com/ranaroussi/yfinance) - Yahoo Finance 데이터
- [Streamlit](https://streamlit.io/) - 대시보드 프레임워크
- [FastAPI](https://fastapi.tiangolo.com/) - API 프레임워크
- [PyTorch](https://pytorch.org/) - 머신러닝 프레임워크
- [InfluxDB](https://www.influxdata.com/) - 시계열 데이터베이스

---

## 📈 로드맵

### v1.0 (현재)
- [x] 기본 데이터 수집
- [x] 실시간 대시보드
- [x] 이상 탐지
- [x] 알림 시스템

### v1.1 (계획 중)
- [ ] 모바일 앱
- [ ] 고급 ML 모델 (Attention, GNN)
- [ ] 백테스팅 엔진
- [ ] 포트폴리오 최적화

### v2.0 (미래)
- [ ] 블록체인 데이터 통합
- [ ] 소셜 미디어 센티먼트 분석
- [ ] 자동 거래 연동
- [ ] 멀티 사용자 지원

---

**"물의 흐름을 읽는 자가 시장을 지배한다"**

Happy Trading! 📊💰
