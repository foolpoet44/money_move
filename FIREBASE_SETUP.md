# Firebase 호스팅 설정 가이드

## 📋 목차

1. [사전 준비사항](#사전-준비사항)
2. [Firebase 프로젝트 생성](#firebase-프로젝트-생성)
3. [프로젝트 초기 설정](#프로젝트-초기-설정)
4. [배포](#배포)
5. [무료 티어 최적화](#무료-티어-최적화)
6. [문제 해결](#문제-해결)

---

## 🎯 사전 준비사항

### 필수 도구 설치

#### 1. Node.js 및 npm
```bash
# macOS (Homebrew 사용)
brew install node

# 설치 확인
node --version
npm --version
```

#### 2. Firebase CLI
```bash
# npm으로 설치
npm install -g firebase-tools

# 설치 확인
firebase --version
```

#### 3. Google Cloud SDK
```bash
# macOS (Homebrew 사용)
brew install --cask google-cloud-sdk

# 초기화
gcloud init

# 설치 확인
gcloud --version
```

#### 4. Docker
```bash
# macOS (Homebrew 사용)
brew install --cask docker

# Docker Desktop 실행 후 확인
docker --version
```

---

## 🔥 Firebase 프로젝트 생성

### 1. Firebase 콘솔에서 프로젝트 생성

1. Firebase 콘솔 접속: https://console.firebase.google.com/
2. **"프로젝트 추가"** 클릭
3. 프로젝트 이름 입력 (예: `money-flow`)
4. Google Analytics 설정 (선택사항, 무료)
5. 프로젝트 생성 완료

### 2. 프로젝트 ID 확인

프로젝트 설정에서 **프로젝트 ID**를 확인하고 메모합니다.
- 예: `money-flow-12345`

### 3. 필요한 서비스 활성화

Firebase 콘솔에서 다음 서비스를 활성화합니다:

#### Firestore 데이터베이스
1. 좌측 메뉴에서 **"Firestore Database"** 선택
2. **"데이터베이스 만들기"** 클릭
3. **프로덕션 모드**로 시작 (보안 규칙은 이미 준비됨)
4. 위치 선택: **us-central** (무료 티어)

#### Firebase Hosting
1. 좌측 메뉴에서 **"Hosting"** 선택
2. **"시작하기"** 클릭

---

## ⚙️ 프로젝트 초기 설정

### 자동 설정 스크립트 실행

```bash
# 프로젝트 디렉토리로 이동
cd /Users/dkmac/Desktop/@26/money_move/money_move

# 설정 스크립트 실행
./scripts/setup_firebase.sh
```

스크립트가 다음 작업을 자동으로 수행합니다:
- ✅ Firebase CLI 로그인
- ✅ 프로젝트 ID 설정 (`.firebaserc` 업데이트)
- ✅ 필요한 Google Cloud API 활성화
- ✅ gcloud 프로젝트 설정

### 수동 설정 (선택사항)

자동 스크립트 대신 수동으로 설정하려면:

```bash
# 1. Firebase 로그인
firebase login

# 2. gcloud 로그인
gcloud auth login

# 3. 프로젝트 설정
firebase use --add
# 프로젝트 ID 선택 후 alias는 'default'로 설정

# 4. gcloud 프로젝트 설정
gcloud config set project YOUR_PROJECT_ID

# 5. 필요한 API 활성화
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable cloudscheduler.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

---

## 🚀 배포

### 1. API 키 설정

```bash
# config/secrets.yaml 파일 편집
cp config/secrets.yaml.example config/secrets.yaml
nano config/secrets.yaml
```

**FRED API 키** (필수):
1. https://fred.stlouisfed.org/ 에서 계정 생성
2. API Keys 메뉴에서 키 발급
3. `config/secrets.yaml`에 입력

### 2. Secret Manager에 API 키 저장 (보안 강화)

```bash
# FRED API 키를 Secret Manager에 저장
echo -n "YOUR_FRED_API_KEY" | gcloud secrets create fred-api-key \
    --data-file=- \
    --replication-policy="automatic"

# Slack Webhook URL (선택사항)
echo -n "YOUR_SLACK_WEBHOOK" | gcloud secrets create slack-webhook \
    --data-file=- \
    --replication-policy="automatic"
```

### 3. 배포 스크립트 실행

```bash
# 전체 배포 (Cloud Run + Firebase Hosting + Firestore)
./scripts/deploy_firebase.sh
```

배포 스크립트가 다음 작업을 수행합니다:
1. Streamlit Dashboard를 Docker 이미지로 빌드
2. Google Container Registry에 푸시
3. Cloud Run에 배포 (무료 티어 설정)
4. Firebase Hosting 배포
5. Firestore 규칙 및 인덱스 배포

### 4. 개별 배포 (선택사항)

#### Firebase Hosting만 배포
```bash
firebase deploy --only hosting
```

#### Firestore 규칙만 배포
```bash
firebase deploy --only firestore:rules
```

#### Cloud Run만 배포
```bash
gcloud run deploy money-flow-dashboard \
    --source . \
    --region us-central1 \
    --allow-unauthenticated \
    --min-instances 0 \
    --max-instances 1 \
    --memory 512Mi
```

---

## 💰 무료 티어 최적화

### Firebase/Google Cloud 무료 티어 한도

| 서비스 | 무료 한도 | 최적화 방법 |
|--------|----------|------------|
| **Firebase Hosting** | 10GB 저장, 360MB/일 전송 | 정적 파일 최소화, CDN 캐싱 |
| **Cloud Run** | 200만 요청/월, 360,000 GB-초 | 최소 인스턴스 0, 512MB RAM |
| **Firestore** | 1GB 저장, 50K 읽기/일, 20K 쓰기/일 | 데이터 수집 간격 증가 (5-10분) |
| **Cloud Scheduler** | 3개 작업 무료 | 핵심 데이터만 수집 |
| **Secret Manager** | 6개 활성 시크릿 무료 | API 키만 저장 |

### 비용 절감 설정

#### 1. Cloud Run 설정 (이미 적용됨)
```bash
--min-instances 0        # Cold Start 허용
--max-instances 1        # 동시 최대 1개 인스턴스
--memory 512Mi           # 최소 메모리
--cpu 1                  # 1 vCPU
--timeout 300            # 5분 타임아웃
```

#### 2. 데이터 수집 간격 조정

`config/config.yaml` 파일에서:
```yaml
data_collection:
  update_intervals:
    bonds: 600     # 10분 (원래 60초)
    forex: 300     # 5분 (원래 30초)
    etf: 600       # 10분 (원래 300초)
    derivatives: 300  # 5분 (원래 60초)
```

#### 3. Firestore 쿼리 최적화

- 필요한 필드만 선택
- 캐싱 활용 (Redis 대신 메모리 캐시)
- 배치 작업 사용

#### 4. 데이터 보관 기간 제한

```python
# src/storage/firestore_client.py
RETENTION_DAYS = 30  # 30일 이상 데이터 자동 삭제
```

---

## 🔍 배포 확인

### 1. 배포된 URL 확인

```bash
# Firebase Hosting URL
echo "https://YOUR_PROJECT_ID.web.app"
echo "https://YOUR_PROJECT_ID.firebaseapp.com"

# Cloud Run Dashboard URL
gcloud run services describe money-flow-dashboard \
    --platform managed \
    --region us-central1 \
    --format 'value(status.url)'
```

### 2. 로그 확인

```bash
# Cloud Run 로그
gcloud logging read "resource.type=cloud_run_revision \
    AND resource.labels.service_name=money-flow-dashboard" \
    --limit 50 \
    --format json

# Firebase Hosting 로그
firebase hosting:logs
```

### 3. 사용량 모니터링

**Firebase 콘솔**:
- https://console.firebase.google.com/project/YOUR_PROJECT_ID/usage

**Cloud Run 콘솔**:
- https://console.cloud.google.com/run?project=YOUR_PROJECT_ID

**Firestore 콘솔**:
- https://console.cloud.google.com/firestore?project=YOUR_PROJECT_ID

---

## 🛠️ 문제 해결

### 배포 실패 시

#### 1. Docker 빌드 실패
```bash
# Docker 데몬 확인
docker ps

# 수동 빌드 테스트
docker build -t test-image -f Dockerfile.streamlit .
```

#### 2. Cloud Run 배포 실패
```bash
# 권한 확인
gcloud projects get-iam-policy YOUR_PROJECT_ID

# Cloud Run API 활성화 확인
gcloud services list --enabled | grep run
```

#### 3. Firebase 배포 실패
```bash
# Firebase 프로젝트 확인
firebase projects:list

# 다시 로그인
firebase logout
firebase login
```

### Firestore 쿼리 제한 초과 시

```yaml
# config/config.yaml에서 간격 증가
data_collection:
  update_intervals:
    bonds: 1200    # 20분
    forex: 600     # 10분
```

### Cloud Run Cold Start 문제

무료 티어에서는 `min-instances: 0`으로 설정되어 첫 요청 시 지연이 발생할 수 있습니다.
- 해결: 유료 전환 후 `min-instances: 1` 설정 (월 $6-10)

---

## 📚 추가 리소스

- [Firebase 공식 문서](https://firebase.google.com/docs)
- [Cloud Run 문서](https://cloud.google.com/run/docs)
- [Firestore 가격 정책](https://firebase.google.com/pricing)
- [무료 티어 한도](https://cloud.google.com/free)

---

## 🔐 보안 권장사항

1. **Firestore 규칙 검증**: `firestore.rules` 파일 확인
2. **Secret Manager 사용**: 환경 변수 대신 Secret Manager 사용
3. **IAM 권한 최소화**: 필요한 권한만 부여
4. **HTTPS 강제**: Firebase Hosting은 기본적으로 HTTPS

---

배포 문제가 발생하면 로그를 확인하고 Firebase 콘솔에서 상태를 모니터링하세요.
