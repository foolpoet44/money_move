# 🚀 Firebase 배포 체크리스트

GitHub Actions를 통한 Firebase 배포를 완료하기 위한 단계별 체크리스트입니다.

## ✅ 1단계: Firebase 프로젝트 설정

- [ ] Firebase 프로젝트 생성
  - [Firebase Console](https://console.firebase.google.com/) 접속
  - 새 프로젝트 생성 또는 기존 프로젝트 선택
  - 프로젝트 ID 확인 (예: `money-39f64`)

- [ ] Firestore 데이터베이스 활성화
  - Firebase Console > Firestore Database
  - "데이터베이스 만들기" 클릭
  - **Native 모드** 선택
  - 리전 선택 (예: `us-central1`)

- [ ] Blaze 플랜으로 업그레이드
  - Firebase Console > 프로젝트 설정 > 사용량 및 결제
  - "Blaze 플랜으로 업그레이드" 클릭
  - ⚠️ Cloud Run 사용을 위해 필요 (무료 할당량 있음)

## ✅ 2단계: Google Cloud API 활성화

- [ ] Google Cloud Console 접속
  - [Google Cloud Console](https://console.cloud.google.com/)
  - Firebase 프로젝트 선택

- [ ] 필요한 API 활성화
  ```bash
  gcloud services enable cloudbuild.googleapis.com
  gcloud services enable run.googleapis.com
  gcloud services enable firestore.googleapis.com
  gcloud services enable cloudscheduler.googleapis.com
  gcloud services enable secretmanager.googleapis.com
  ```

## ✅ 3단계: 서비스 계정 생성

- [ ] 서비스 계정 만들기
  - Google Cloud Console > IAM 및 관리자 > 서비스 계정
  - "서비스 계정 만들기" 클릭
  - 이름: `github-actions-deployer`
  - 설명: `GitHub Actions deployment service account`

- [ ] 역할 부여
  - [ ] Firebase Admin
  - [ ] Cloud Run Admin
  - [ ] Cloud Build Editor
  - [ ] Service Account User
  - [ ] Secret Manager Secret Accessor

- [ ] JSON 키 생성
  - 서비스 계정 선택 > 키 탭
  - "키 추가" > "새 키 만들기" > JSON
  - 다운로드된 JSON 파일 안전하게 보관

## ✅ 4단계: GitHub Secrets 설정

- [ ] GitHub 저장소 설정 접속
  - GitHub 저장소 > Settings > Secrets and variables > Actions

- [ ] `FIREBASE_PROJECT_ID` 추가
  - Name: `FIREBASE_PROJECT_ID`
  - Value: Firebase 프로젝트 ID (예: `money-39f64`)

- [ ] `FIREBASE_SERVICE_ACCOUNT` 추가
  - Name: `FIREBASE_SERVICE_ACCOUNT`
  - Value: 3단계에서 다운로드한 JSON 파일의 **전체 내용**
  - ⚠️ JSON 형식 그대로 복사 (줄바꿈 포함)

## ✅ 5단계: 로컬 파일 확인

- [ ] `.firebaserc` 파일 확인
  ```json
  {
    "projects": {
      "default": "YOUR_PROJECT_ID"
    }
  }
  ```

- [ ] `firebase.json` 파일 확인
  - Hosting 설정 확인
  - Firestore 규칙 및 인덱스 경로 확인

- [ ] `firestore.rules` 파일 확인
  - 보안 규칙이 적절한지 확인

- [ ] `firestore.indexes.json` 파일 확인
  - 필요한 인덱스가 정의되어 있는지 확인

- [ ] `Dockerfile` 파일 확인
  - Cloud Run 배포를 위한 Dockerfile 존재 확인

- [ ] `requirements-firebase.txt` 파일 확인
  - Firebase 무료 티어에 최적화된 의존성 확인

## ✅ 6단계: GitHub Actions 워크플로우 확인

- [ ] `.github/workflows/firebase-deploy.yml` 파일 확인
  - 워크플로우 파일이 존재하는지 확인
  - 트리거 설정 확인 (main/master 브랜치)

- [ ] 워크플로우 단계 확인
  - [ ] Checkout repository
  - [ ] Set up Python
  - [ ] Install dependencies
  - [ ] Set up Node.js
  - [ ] Install Firebase CLI
  - [ ] Authenticate to Google Cloud
  - [ ] Deploy Firestore
  - [ ] Deploy Hosting
  - [ ] Deploy Cloud Run

## ✅ 7단계: 배포 테스트

### 로컬 테스트 (선택사항)

- [ ] Firebase CLI 설치 확인
  ```bash
  firebase --version
  ```

- [ ] Firebase 로그인
  ```bash
  firebase login
  ```

- [ ] 로컬 배포 스크립트 실행
  ```bash
  chmod +x scripts/deploy_firebase.sh
  ./scripts/deploy_firebase.sh
  ```

### GitHub Actions 배포

- [ ] 코드 커밋 및 푸시
  ```bash
  git add .
  git commit -m "Setup Firebase deployment"
  git push origin main
  ```

- [ ] GitHub Actions 실행 확인
  - GitHub 저장소 > Actions 탭
  - "Firebase Deployment" 워크플로우 확인
  - 각 단계가 성공적으로 완료되는지 확인

## ✅ 8단계: 배포 확인

- [ ] Firebase Hosting 확인
  - URL: `https://YOUR_PROJECT_ID.web.app`
  - URL: `https://YOUR_PROJECT_ID.firebaseapp.com`
  - 페이지가 정상적으로 로드되는지 확인

- [ ] Firestore 확인
  - Firebase Console > Firestore Database
  - 규칙 및 인덱스가 배포되었는지 확인

- [ ] Cloud Run 확인
  - Google Cloud Console > Cloud Run
  - `money-flow-dashboard` 서비스 확인
  - URL 클릭하여 대시보드 접속 확인

## ✅ 9단계: 모니터링 설정

- [ ] Cloud Logging 확인
  - Google Cloud Console > Logging
  - 배포 로그 확인

- [ ] Cloud Monitoring 설정
  - Google Cloud Console > Monitoring
  - 알림 정책 설정 (선택사항)

- [ ] Firebase Console 모니터링
  - Firebase Console > 사용량 및 결제
  - 무료 할당량 사용량 확인

## ✅ 10단계: 문서화

- [ ] 배포 URL 문서화
  - README.md에 배포 URL 추가
  - 팀원들과 공유

- [ ] 환경 변수 문서화
  - 필요한 환경 변수 목록 작성
  - Secret Manager에 저장할 값 정리

- [ ] 운영 가이드 작성
  - 배포 프로세스 문서화
  - 롤백 절차 문서화
  - 문제 해결 가이드 작성

## 🔧 문제 해결

### 인증 오류
```
Error: Unable to authenticate
```
**해결**: `FIREBASE_SERVICE_ACCOUNT` Secret이 올바른 JSON 형식인지 확인

### API 활성화 오류
```
Error: API [xxx] not enabled
```
**해결**: 
```bash
gcloud services enable [API_NAME] --project=[PROJECT_ID]
```

### Cloud Run 배포 실패
```
Error: Cloud Run deployment failed
```
**해결**:
1. Blaze 플랜으로 업그레이드 확인
2. Cloud Run API 활성화 확인
3. Dockerfile 문법 확인

### Firestore 규칙 배포 실패
```
Error: Firestore rules deployment failed
```
**해결**:
1. `firestore.rules` 파일 문법 확인
2. Firestore 데이터베이스가 활성화되어 있는지 확인

## 📚 참고 문서

- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - 상세 배포 가이드
- [FIREBASE_SETUP.md](FIREBASE_SETUP.md) - Firebase 초기 설정
- [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) - GitHub Actions 설정

## 🎉 완료!

모든 체크리스트를 완료했다면 배포가 성공적으로 완료된 것입니다!

다음 단계:
1. 배포된 애플리케이션 테스트
2. 모니터링 대시보드 확인
3. 사용량 추적 시작
4. 팀원들에게 URL 공유

---

**문제가 발생하면**: 
- GitHub Issues에 문제 보고
- Firebase Console의 로그 확인
- Google Cloud Console의 로그 확인
