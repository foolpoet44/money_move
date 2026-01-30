#!/bin/bash

# Firebase 배포 스크립트 (무료 티어 최적화)
# Money Flow Prediction System을 Firebase + Cloud Run에 배포합니다

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

success() { echo -e "${GREEN}✓ $1${NC}"; }
warning() { echo -e "${YELLOW}⚠ $1${NC}"; }
error() { echo -e "${RED}✗ $1${NC}"; exit 1; }
info() { echo -e "${BLUE}ℹ $1${NC}"; }

echo "🚀 Firebase 배포를 시작합니다..."

# 프로젝트 ID 가져오기
PROJECT_ID=$(firebase use | grep "Now using project" | awk '{print $4}' | tr -d "'")
if [ -z "$PROJECT_ID" ]; then
    PROJECT_ID=$(cat .firebaserc | grep -o '"default"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)
fi

info "프로젝트 ID: $PROJECT_ID"

# 1. 사전 검증
echo ""
echo "📋 사전 검증 중..."

# Firebase CLI 확인
if ! command -v firebase &> /dev/null; then
    error "Firebase CLI가 설치되어 있지 않습니다"
fi

# gcloud CLI 확인
if ! command -v gcloud &> /dev/null; then
    error "Google Cloud SDK가 설치되어 있지 않습니다"
fi

# 로그인 상태 확인
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
    error "gcloud 로그인이 필요합니다: gcloud auth login"
fi

success "사전 검증 완료"

# 2. 환경 변수 설정
echo ""
echo "🔧 환경 변수 설정 중..."

# Cloud Run 서비스 이름
DASHBOARD_SERVICE="money-flow-dashboard"
REGION="us-central1"

success "환경 변수 설정 완료"

# 3. Streamlit Dashboard를 Cloud Run에 배포
echo ""
echo "📦 Streamlit Dashboard를 Cloud Run에 배포 중..."

# Docker 이미지 빌드 및 푸시
IMAGE_NAME="gcr.io/$PROJECT_ID/$DASHBOARD_SERVICE"
info "이미지 빌드: $IMAGE_NAME"

docker build -t $IMAGE_NAME -f Dockerfile.streamlit . || error "Docker 이미지 빌드 실패"
docker push $IMAGE_NAME || error "Docker 이미지 푸시 실패"

# Cloud Run에 배포 (무료 티어 최적화)
info "Cloud Run 배포 중..."
gcloud run deploy $DASHBOARD_SERVICE \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --min-instances 0 \
    --max-instances 1 \
    --memory 512Mi \
    --cpu 1 \
    --timeout 300 \
    --project $PROJECT_ID \
    || error "Cloud Run 배포 실패"

# Cloud Run URL 가져오기
DASHBOARD_URL=$(gcloud run services describe $DASHBOARD_SERVICE \
    --platform managed \
    --region $REGION \
    --format 'value(status.url)' \
    --project $PROJECT_ID)

success "Dashboard 배포 완료: $DASHBOARD_URL"

# 4. Firebase Hosting + Firestore 규칙 배포
echo ""
echo "🔥 Firebase Hosting 및 Firestore 배포 중..."

# firebase.json에서 Cloud Run URL 업데이트
info "firebase.json 업데이트 중..."

firebase deploy --only hosting,firestore || error "Firebase 배포 실패"

success "Firebase Hosting 배포 완료"

# 5. Firestore 인덱스 배포
echo ""
echo "🗂️  Firestore 인덱스 배포 중..."
firebase deploy --only firestore:indexes || warning "Firestore 인덱스 배포 실패 (수동 생성 필요)"

# 6. 배포 완료 정보 출력
echo ""
echo "============================================"
success "🎉 배포가 완료되었습니다!"
echo "============================================"
echo ""
echo "📍 배포된 서비스:"
echo "  • Firebase Hosting: https://$PROJECT_ID.web.app"
echo "  • Firebase Hosting: https://$PROJECT_ID.firebaseapp.com"
echo "  • Dashboard (Cloud Run): $DASHBOARD_URL"
echo ""
echo "📊 무료 티어 사용량 모니터링:"
echo "  • Firebase 콘솔: https://console.firebase.google.com/project/$PROJECT_ID"
echo "  • Cloud Run 콘솔: https://console.cloud.google.com/run?project=$PROJECT_ID"
echo "  • Firestore 콘솔: https://console.cloud.google.com/firestore?project=$PROJECT_ID"
echo ""

# 7. 비용 최적화 팁
info "💡 무료 티어 최적화 팁:"
echo "  1. Cloud Run 최소 인스턴스: 0 (Cold Start 허용)"
echo "  2. Firestore 쿼리 캐싱 활용"
echo "  3. 데이터 수집 간격: 5-10분"
echo "  4. Cloud Scheduler: 3개 작업까지 무료"
echo ""

warning "중요: config/secrets.yaml의 API 키는 Google Secret Manager를 사용하세요"
echo "  gcloud secrets create fred-api-key --data-file=- < config/secrets.yaml"
echo ""
