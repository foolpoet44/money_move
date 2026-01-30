#!/bin/bash

# Firebase 초기 설정 스크립트
# 무료 티어 범위에서 Money Flow 프로젝트를 설정합니다

set -e

echo "🔥 Firebase 프로젝트 초기 설정을 시작합니다..."

# 컬러 출력을 위한 함수
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

success() {
    echo -e "${GREEN}✓ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

error() {
    echo -e "${RED}✗ $1${NC}"
    exit 1
}

# 1. Firebase CLI 설치 확인
echo "📦 Firebase CLI 확인 중..."
if ! command -v firebase &> /dev/null; then
    warning "Firebase CLI가 설치되어 있지 않습니다."
    echo "설치 중..."
    npm install -g firebase-tools || error "Firebase CLI 설치 실패"
fi
success "Firebase CLI 설치됨: $(firebase --version)"

# 2. gcloud CLI 설치 확인
echo "📦 Google Cloud SDK 확인 중..."
if ! command -v gcloud &> /dev/null; then
    warning "Google Cloud SDK가 설치되어 있지 않습니다."
    echo "다운로드: https://cloud.google.com/sdk/docs/install"
    error "Google Cloud SDK를 먼저 설치해주세요"
fi
success "Google Cloud SDK 설치됨: $(gcloud --version | head -n 1)"

# 3. Firebase 로그인
echo "🔐 Firebase 로그인..."
firebase login || error "Firebase 로그인 실패"
success "Firebase 로그인 완료"

# 4. 프로젝트 ID 입력
echo ""
echo "Firebase 프로젝트를 생성하거나 기존 프로젝트를 사용하세요:"
echo "👉 https://console.firebase.google.com/"
echo ""
read -p "Firebase 프로젝트 ID를 입력하세요: " PROJECT_ID

if [ -z "$PROJECT_ID" ]; then
    error "프로젝트 ID가 필요합니다"
fi

# 5. .firebaserc 파일 업데이트
echo "📝 .firebaserc 업데이트 중..."
cat > .firebaserc << EOF
{
  "projects": {
    "default": "$PROJECT_ID"
  }
}
EOF
success ".firebaserc 업데이트 완료"

# 6. gcloud 프로젝트 설정
echo "🔧 Google Cloud 프로젝트 설정..."
gcloud config set project $PROJECT_ID || error "gcloud 프로젝트 설정 실패"
success "Google Cloud 프로젝트 설정 완료"

# 7. 필요한 API 활성화
echo "🔌 필요한 Google Cloud API 활성화 중..."
APIs=(
    "cloudbuild.googleapis.com"
    "run.googleapis.com"
    "firestore.googleapis.com"
    "cloudscheduler.googleapis.com"
    "secretmanager.googleapis.com"
)

for api in "${APIs[@]}"; do
    echo "  활성화: $api"
    gcloud services enable $api --project=$PROJECT_ID
done
success "모든 API 활성화 완료"

# 8. Firestore 초기화
echo "🗄️  Firestore 데이터베이스 확인..."
warning "Firebase 콘솔에서 Firestore를 활성화해야 합니다:"
echo "👉 https://console.firebase.google.com/project/$PROJECT_ID/firestore"
echo ""
read -p "Firestore를 활성화했습니까? (y/n): " firestore_ready
if [ "$firestore_ready" != "y" ]; then
    warning "나중에 Firestore를 활성화해주세요"
fi

# 9. config 디렉토리 확인
echo "📁 설정 파일 확인..."
if [ ! -f "config/secrets.yaml" ]; then
    if [ -f "config/secrets.yaml.example" ]; then
        cp config/secrets.yaml.example config/secrets.yaml
        warning "config/secrets.yaml 파일을 생성했습니다. API 키를 입력해주세요."
    fi
fi

# 10. public 디렉토리 확인
if [ ! -d "public" ]; then
    warning "public 디렉토리가 없습니다. 생성된 파일을 확인해주세요."
fi

# 완료 메시지
echo ""
echo "============================================"
success "🎉 Firebase 초기 설정이 완료되었습니다!"
echo "============================================"
echo ""
echo "다음 단계:"
echo "1. config/secrets.yaml 파일에 API 키 입력"
echo "2. Firebase 콘솔에서 Firestore 활성화"
echo "3. 배포: ./scripts/deploy_firebase.sh"
echo ""
echo "프로젝트 ID: $PROJECT_ID"
echo "Firebase 콘솔: https://console.firebase.google.com/project/$PROJECT_ID"
echo ""
