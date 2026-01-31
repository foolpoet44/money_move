# GitHub Actions 배포 설정 가이드

이 문서는 GitHub Actions를 통해 Firebase에 자동 배포하기 위한 설정 방법을 안내합니다.

## 📋 사전 요구사항

1. **Firebase 프로젝트 생성**
   - [Firebase Console](https://console.firebase.google.com/)에서 프로젝트 생성
   - Firestore 데이터베이스 활성화 (Native 모드)
   - Blaze (종량제) 플랜으로 업그레이드 (Cloud Run 사용을 위해 필요)

2. **Google Cloud 설정**
   - [Google Cloud Console](https://console.cloud.google.com/)에서 프로젝트 확인
   - 필요한 API 활성화:
     - Cloud Build API
     - Cloud Run API
     - Firestore API
     - Cloud Scheduler API
     - Secret Manager API

## 🔑 GitHub Secrets 설정

GitHub 저장소의 Settings > Secrets and variables > Actions에서 다음 시크릿을 추가하세요:

### 1. FIREBASE_PROJECT_ID

Firebase 프로젝트 ID를 설정합니다.

```bash
# .firebaserc 파일에서 확인 가능
cat .firebaserc
```

**예시**: `money-39f64`

### 2. FIREBASE_SERVICE_ACCOUNT

Firebase 서비스 계정 키를 JSON 형식으로 설정합니다.

#### 서비스 계정 키 생성 방법:

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 프로젝트 선택
3. **IAM 및 관리자** > **서비스 계정** 메뉴로 이동
4. **서비스 계정 만들기** 클릭
   - 이름: `github-actions-deployer`
   - 설명: `GitHub Actions deployment service account`
5. 다음 역할 부여:
   - **Firebase Admin**
   - **Cloud Run Admin**
   - **Cloud Build Editor**
   - **Service Account User**
   - **Secret Manager Secret Accessor**
6. **키 추가** > **새 키 만들기** > **JSON** 선택
7. 다운로드된 JSON 파일의 전체 내용을 복사하여 GitHub Secret에 추가

#### JSON 파일 예시:
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "github-actions-deployer@your-project-id.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "..."
}
```

⚠️ **주의**: JSON 파일 전체를 그대로 복사하세요. 줄바꿈과 공백도 유지되어야 합니다.

## 🚀 배포 워크플로우

### 자동 배포 (main/master 브랜치)

`main` 또는 `master` 브랜치에 푸시하면 자동으로 배포가 시작됩니다:

```bash
git add .
git commit -m "Deploy to Firebase"
git push origin main
```

### 수동 배포

GitHub 저장소의 **Actions** 탭에서:
1. **Firebase Deployment** 워크플로우 선택
2. **Run workflow** 클릭
3. 환경 선택 (production/staging)
4. **Run workflow** 버튼 클릭

## 📊 배포 프로세스

GitHub Actions 워크플로우는 다음 단계를 수행합니다:

1. **코드 체크아웃**: 저장소 코드를 가져옵니다
2. **Python 설정**: Python 3.10 환경을 구성합니다
3. **의존성 설치**: requirements.txt의 패키지를 설치합니다
4. **Node.js 설정**: Firebase CLI를 위한 Node.js를 설정합니다
5. **Firebase CLI 설치**: Firebase 도구를 설치합니다
6. **Google Cloud 인증**: 서비스 계정으로 인증합니다
7. **Firestore 배포**: 데이터베이스 규칙과 인덱스를 배포합니다
8. **Hosting 배포**: 정적 파일을 Firebase Hosting에 배포합니다
9. **Cloud Run 배포**: Streamlit 대시보드를 Cloud Run에 배포합니다

## 🔍 배포 확인

배포가 완료되면 GitHub Actions 로그에서 다음 정보를 확인할 수 있습니다:

- **Firebase Hosting URL**: `https://[PROJECT_ID].web.app`
- **Cloud Run URL**: 워크플로우 로그에 표시됨

## 🐛 문제 해결

### 인증 오류

```
Error: Unable to authenticate
```

**해결 방법**:
- `FIREBASE_SERVICE_ACCOUNT` 시크릿이 올바른 JSON 형식인지 확인
- 서비스 계정에 필요한 권한이 모두 부여되었는지 확인

### API 활성화 오류

```
Error: API [xxx] not enabled
```

**해결 방법**:
```bash
gcloud services enable [API_NAME] --project=[PROJECT_ID]
```

### Cloud Run 배포 실패

```
Error: Cloud Run deployment failed
```

**해결 방법**:
- Blaze 플랜으로 업그레이드 확인
- Cloud Run API가 활성화되었는지 확인
- Dockerfile이 올바른지 확인

## 📝 로컬 배포 테스트

GitHub Actions에 푸시하기 전에 로컬에서 배포를 테스트할 수 있습니다:

```bash
# 스크립트 실행 권한 부여
chmod +x scripts/deploy_firebase.sh

# 배포 실행
./scripts/deploy_firebase.sh
```

## 🔐 보안 권장사항

1. **서비스 계정 키 보호**
   - JSON 키 파일을 절대 Git에 커밋하지 마세요
   - `.gitignore`에 `*.json` 패턴 추가

2. **최소 권한 원칙**
   - 서비스 계정에 필요한 최소한의 권한만 부여

3. **정기적인 키 교체**
   - 서비스 계정 키를 정기적으로 교체 (3-6개월)

4. **감사 로그 모니터링**
   - Google Cloud의 감사 로그를 정기적으로 확인

## 📚 추가 리소스

- [Firebase CLI 문서](https://firebase.google.com/docs/cli)
- [Cloud Run 문서](https://cloud.google.com/run/docs)
- [GitHub Actions 문서](https://docs.github.com/en/actions)
- [Firebase Hosting 문서](https://firebase.google.com/docs/hosting)

## 🎯 다음 단계

1. GitHub Secrets 설정 완료
2. 코드를 main 브랜치에 푸시
3. GitHub Actions 탭에서 배포 진행 상황 확인
4. 배포된 URL에서 애플리케이션 확인

---

**문제가 발생하면**: GitHub Issues에 문제를 보고하거나 Firebase 콘솔의 로그를 확인하세요.
