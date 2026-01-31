# GitHub Actions 자동 배포 설정 가이드

Firebase를 통한 자동 배포를 GitHub Actions로 설정하는 단계별 가이드입니다.

## 📋 목차

1. [개요](#개요)
2. [사전 준비사항](#사전-준비사항)
3. [Firebase 서비스 계정 생성](#firebase-서비스-계정-생성)
4. [GitHub Secrets 설정](#github-secrets-설정)
5. [워크플로우 사용법](#워크플로우-사용법)
6. [문제 해결](#문제-해결)

---

## 🎯 개요

GitHub Actions를 사용하면 코드를 `main` 브랜치에 푸시할 때마다 자동으로 Firebase에 배포할 수 있습니다.

### 주요 기능

- ✅ **자동 배포**: main 브랜치 푸시 시 자동 배포
- ✅ **수동 트리거**: GitHub UI에서 수동으로 배포 실행
- ✅ **테스트 자동화**: PR 생성 시 자동 테스트 실행
- ✅ **보안**: 서비스 계정 키를 GitHub Secrets로 안전하게 관리
- ✅ **다중 서비스 배포**: Hosting, Firestore, Cloud Run 동시 배포

---

## 🔧 사전 준비사항

### 1. Firebase 프로젝트 설정

`.firebaserc` 파일에서 실제 Firebase 프로젝트 ID로 업데이트:

```json
{
  "projects": {
    "default": "your-actual-project-id"
  }
}
```

Firebase 프로젝트 ID는 [Firebase 콘솔](https://console.firebase.google.com/)의 프로젝트 설정에서 확인할 수 있습니다.

### 2. GitHub 저장소 준비

GitHub에 코드가 푸시되어 있어야 합니다:

```bash
git init
git add .
git commit -m "Initial commit with GitHub Actions"
git remote add origin https://github.com/YOUR_USERNAME/money_move.git
git push -u origin main
```

---

## 🔑 Firebase 서비스 계정 생성

GitHub Actions가 Firebase에 배포하려면 서비스 계정 키가 필요합니다.

### 방법 1: Firebase CLI 사용 (권장)

```bash
# Firebase 로그인
firebase login

# 서비스 계정 키 생성
firebase init hosting:github

# 프롬프트에 따라 진행:
# 1. GitHub 저장소 선택
# 2. 자동 배포 설정 여부 선택
# 3. GitHub Secrets 자동 설정
```

이 방법을 사용하면 Firebase CLI가 자동으로 서비스 계정을 생성하고 GitHub Secrets에 추가합니다.

### 방법 2: Google Cloud Console 수동 생성

#### Step 1: 서비스 계정 생성

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. Firebase 프로젝트 선택
3. **IAM 및 관리자** > **서비스 계정** 메뉴로 이동
4. **서비스 계정 만들기** 클릭
5. 다음 정보 입력:
   - **이름**: `github-actions-deployer`
   - **설명**: `GitHub Actions용 Firebase 배포 계정`
6. **만들고 계속하기** 클릭

#### Step 2: 권한 부여

다음 역할을 추가합니다:

- **Firebase Admin** (firebase.admin)
- **Cloud Run Admin** (run.admin)
- **Service Account User** (iam.serviceAccountUser)
- **Storage Object Admin** (storage.objectAdmin)

#### Step 3: 키 생성

1. 생성된 서비스 계정 클릭
2. **키** 탭 선택
3. **키 추가** > **새 키 만들기**
4. **JSON** 형식 선택
5. **만들기** 클릭 → JSON 파일이 자동으로 다운로드됩니다

⚠️ **중요**: 이 JSON 파일은 안전하게 보관하고, 절대 Git에 커밋하지 마세요!

---

## 🔐 GitHub Secrets 설정

### Step 1: GitHub 저장소 설정 페이지로 이동

1. GitHub 저장소 페이지 열기
2. **Settings** 탭 클릭
3. 좌측 메뉴에서 **Secrets and variables** > **Actions** 선택

### Step 2: Secrets 추가

**Add repository secret** 버튼을 클릭하고 다음 secrets를 추가합니다:

#### 1. FIREBASE_SERVICE_ACCOUNT

- **Name**: `FIREBASE_SERVICE_ACCOUNT`
- **Value**: 다운로드한 서비스 계정 JSON 파일의 전체 내용

```bash
# JSON 파일 내용 복사 (macOS)
cat ~/Downloads/your-project-id-xxxxx.json | pbcopy

# JSON 파일 내용 복사 (Linux)
cat ~/Downloads/your-project-id-xxxxx.json | xclip -selection clipboard
```

JSON 내용을 그대로 붙여넣기합니다.

#### 2. FIREBASE_PROJECT_ID

- **Name**: `FIREBASE_PROJECT_ID`
- **Value**: Firebase 프로젝트 ID (예: `money-flow-12345`)

### Step 3: 선택적 Secrets (추가 기능용)

#### FRED_API_KEY

- **Name**: `FRED_API_KEY`
- **Value**: FRED API 키
- **용도**: 데이터 수집 기능 활성화

#### SLACK_WEBHOOK_URL

- **Name**: `SLACK_WEBHOOK_URL`
- **Value**: Slack Webhook URL
- **용도**: 배포 알림 전송

---

## 🚀 워크플로우 사용법

### 자동 배포 (main 브랜치 푸시)

```bash
# 로컬에서 변경사항 커밋
git add .
git commit -m "Update dashboard features"
git push origin main
```

→ 자동으로 GitHub Actions가 실행되어 Firebase에 배포됩니다!

### 수동 배포

1. GitHub 저장소 페이지에서 **Actions** 탭 클릭
2. 좌측에서 **Firebase Deployment** 워크플로우 선택
3. **Run workflow** 버튼 클릭
4. 환경 선택 (production/staging)
5. **Run workflow** 확인

### 배포 상태 확인

#### GitHub Actions 로그

1. **Actions** 탭에서 실행 중인 워크플로우 클릭
2. 각 단계별 로그 확인
3. 성공 시 배포 URL이 표시됩니다

#### Firebase 콘솔

- **Hosting**: https://console.firebase.google.com/project/YOUR_PROJECT_ID/hosting
- **Cloud Run**: https://console.cloud.google.com/run?project=YOUR_PROJECT_ID
- **Firestore**: https://console.firebase.google.com/project/YOUR_PROJECT_ID/firestore

---

## 📊 워크플로우 구성

### firebase-deploy.yml

**트리거:**
- `main` 또는 `master` 브랜치에 푸시
- 수동 실행 (workflow_dispatch)

**배포 순서:**
1. Python 및 Node.js 환경 설정
2. Firebase CLI 설치
3. Google Cloud 인증
4. Firestore 규칙 및 인덱스 배포
5. Firebase Hosting 배포
6. Cloud Run 서비스 배포

### test.yml

**트리거:**
- Pull Request 생성/업데이트
- `develop` 또는 `feature/**` 브랜치에 푸시

**테스트 항목:**
1. 코드 포맷팅 검사 (Black)
2. Import 정렬 검사 (isort)
3. 린팅 (flake8)
4. 단위 테스트 (pytest)
5. 보안 취약점 스캔 (safety, bandit)

---

## 🛠️ 문제 해결

### 배포 실패: "Permission denied"

**원인**: 서비스 계정에 필요한 권한이 없습니다.

**해결방법**:
1. Google Cloud Console에서 서비스 계정 확인
2. 필요한 역할 추가:
   - Firebase Admin
   - Cloud Run Admin
   - Service Account User

```bash
# gcloud CLI로 권한 부여
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/firebase.admin"
```

### 배포 실패: "API not enabled"

**원인**: 필요한 Google Cloud API가 활성화되지 않았습니다.

**해결방법**:

```bash
# 로컬에서 필요한 API 활성화
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable cloudscheduler.googleapis.com
```

### 배포 실패: "Invalid credentials"

**원인**: GitHub Secrets의 서비스 계정 키가 잘못되었습니다.

**해결방법**:
1. 서비스 계정 JSON 파일 다시 다운로드
2. GitHub Secrets에서 `FIREBASE_SERVICE_ACCOUNT` 업데이트
3. JSON 형식이 올바른지 확인 (전체 내용 복사)

### 테스트 실패: "Module not found"

**원인**: 필요한 Python 패키지가 설치되지 않았습니다.

**해결방법**:
1. `requirements.txt` 확인 및 업데이트
2. 테스트용 의존성 추가:

```bash
# requirements-dev.txt 생성
pytest>=7.0.0
pytest-cov>=4.0.0
flake8>=6.0.0
black>=23.0.0
isort>=5.12.0
safety>=2.3.0
bandit>=1.7.0
```

3. GitHub Actions 워크플로우에서 설치:

```yaml
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Cloud Run 배포 시 타임아웃

**원인**: Docker 이미지 빌드가 너무 오래 걸립니다.

**해결방법**:
1. `.dockerignore` 파일 확인
2. 불필요한 파일 제외
3. 레이어 캐싱 최적화

```dockerfile
# Dockerfile.streamlit에서 캐싱 최적화
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

---

## 📈 모범 사례

### 1. 브랜치 전략

```
main (production) ← 자동 배포
  ↑
develop (staging) ← 자동 테스트
  ↑
feature/* ← 자동 테스트
```

### 2. 환경별 설정

프로덕션과 스테이징 환경을 분리:

```yaml
# .github/workflows/firebase-deploy.yml
on:
  push:
    branches:
      - main  # production
      - develop  # staging
```

### 3. 배포 전 테스트 필수

PR에서 모든 테스트가 통과한 후에만 병합:

1. Branch protection rules 설정
2. Required status checks 활성화
3. Tests 워크플로우 통과 필수

### 4. 롤백 계획

배포 실패 시:

```bash
# Firebase Hosting 이전 버전으로 롤백
firebase hosting:clone SOURCE_SITE_ID:SOURCE_VERSION TARGET_SITE_ID:live

# Cloud Run 이전 리비전으로 롤백
gcloud run services update-traffic money-flow-dashboard \
  --to-revisions=PREVIOUS_REVISION=100 \
  --region us-central1
```

---

## 📚 추가 리소스

- [GitHub Actions 문서](https://docs.github.com/en/actions)
- [Firebase CLI 문서](https://firebase.google.com/docs/cli)
- [Cloud Run 문서](https://cloud.google.com/run/docs)
- [서비스 계정 관리](https://cloud.google.com/iam/docs/service-accounts)

---

## 🔒 보안 체크리스트

배포 전 확인사항:

- [ ] 서비스 계정 JSON 파일이 Git에 커밋되지 않았는지 확인
- [ ] `.gitignore`에 `*.json`, `config/secrets.yaml` 포함 확인
- [ ] GitHub Secrets가 올바르게 설정되었는지 확인
- [ ] 서비스 계정 권한이 최소 권한 원칙을 따르는지 확인
- [ ] Firestore 보안 규칙이 프로덕션에 적합한지 확인

---

배포 과정에서 문제가 발생하면 GitHub Actions 로그와 Firebase 콘솔을 확인하세요!
