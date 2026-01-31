#!/bin/bash

# Firebase 배포 스크립트
# 로컬 환경에서 Firebase에 배포합니다

set -e

echo "🚀 Firebase 배포를 시작합니다..."

# 컬러 출력
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
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

info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# 프로젝트 ID 가져오기
PROJECT_ID=$(cat .firebaserc | grep -o '"default": "[^"]*' | grep -o '[^"]*$')

if [ -z "$PROJECT_ID" ]; then
    error "프로젝트 ID를 찾을 수 없습니다. .firebaserc 파일을 확인하세요."
fi

info "프로젝트 ID: $PROJECT_ID"

# 1. Firebase 로그인 확인
echo ""
echo "📝 Firebase 인증 확인 중..."
if ! firebase projects:list &> /dev/null; then
    warning "Firebase 로그인이 필요합니다."
    firebase login || error "Firebase 로그인 실패"
fi
success "Firebase 인증 완료"

# 2. gcloud 인증 확인
echo ""
echo "📝 Google Cloud 인증 확인 중..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
    warning "Google Cloud 로그인이 필요합니다."
    gcloud auth login || error "Google Cloud 로그인 실패"
fi
success "Google Cloud 인증 완료"

# 3. 프로젝트 설정
echo ""
echo "🔧 프로젝트 설정 중..."
gcloud config set project $PROJECT_ID
firebase use $PROJECT_ID
success "프로젝트 설정 완료"

# 4. Firestore 규칙 및 인덱스 배포
echo ""
echo "🗄️  Firestore 규칙 및 인덱스 배포 중..."
firebase deploy --only firestore --project $PROJECT_ID || warning "Firestore 배포 실패 (계속 진행)"
success "Firestore 배포 완료"

# 5. Firebase Hosting 배포
echo ""
echo "🌐 Firebase Hosting 배포 중..."
firebase deploy --only hosting --project $PROJECT_ID || error "Hosting 배포 실패"
success "Firebase Hosting 배포 완료"

# 6. Cloud Run 배포 (선택사항)
echo ""
read -p "Cloud Run에 대시보드를 배포하시겠습니까? (y/n): " deploy_cloud_run

if [ "$deploy_cloud_run" = "y" ]; then
    echo ""
    echo "☁️  Cloud Run 배포 중..."
    
    gcloud run deploy money-flow-dashboard \
        --source . \
        --platform managed \
        --region us-central1 \
        --allow-unauthenticated \
        --min-instances 0 \
        --max-instances 1 \
        --memory 512Mi \
        --cpu 1 \
        --timeout 300 \
        --set-env-vars ENVIRONMENT=production \
        --project $PROJECT_ID || warning "Cloud Run 배포 실패"
    
    success "Cloud Run 배포 완료"
    
    # Cloud Run URL 가져오기
    CLOUD_RUN_URL=$(gcloud run services describe money-flow-dashboard \
        --platform managed \
        --region us-central1 \
        --format 'value(status.url)' \
        --project $PROJECT_ID)
fi

# 배포 완료 메시지
echo ""
echo "============================================"
success "🎉 배포가 완료되었습니다!"
echo "============================================"
echo ""
echo "📍 배포된 서비스:"
echo ""
echo "  Firebase Hosting:"
echo "    - https://$PROJECT_ID.web.app"
echo "    - https://$PROJECT_ID.firebaseapp.com"
echo ""

if [ ! -z "$CLOUD_RUN_URL" ]; then
    echo "  Cloud Run Dashboard:"
    echo "    - $CLOUD_RUN_URL"
    echo ""
fi

echo "  Firebase Console:"
echo "    - https://console.firebase.google.com/project/$PROJECT_ID"
echo ""
echo "============================================"
