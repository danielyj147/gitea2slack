# Gitea2Slack - Gitea 알림을 Slack과 연동하기
[English](./README.md)

## 시작하기
### 1단계: 프로젝트 복제하기
```bash
git clone <이 리포지토리의 링크>
```
### 2단계: Slack 앱 생성하기
Slack API 페이지로 이동하여 새 앱을 생성. 이 앱은 Gitea에서 Slack 워크스페이스로 알림을 관리함

### 3단계: 앱 권한 설정하기
앱의 OAuth & Permissions 페이지에서 다음 권한을 추가하여 필요한 권한을 활성

- channels:write.invites: 공개 채널에 멤버를 초대합니다.
- chat:write: @Gitea Notifications으로 메시지를 보냅니다.
- groups:write: Gitea Notifications이 추가된 비공개 채널을 관리하고 새로 만듭니다.
- im:write: 사람들과 직접 메시지를 시작합니다.
- incoming-webhook: Slack의 특정 채널에 메시지를 게시합니다.
- users:read: 워크스페이스의 사람들을 봅니다.
- users:read.email: 워크스페이스의 사람들의 이메일 주소를 봅니다.

### 4단계: 환경 변수 설정하기
앱의 Bot User OAuth Token을 복사하여 프로젝트 디렉토리의 .env 파일에 붙여넣기

### 5단계: 의존성 설치 및 서버 실행하기
.env 파일을 설정한 후, 프로젝트 디렉토리로 이동하여 Python 환경을 설정:

```bash
cd <로컬_프로젝트_경로>
python -m venv ./.venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 6단계: Gitea 웹훅 구성하기
- Gitea 프로젝트에서 설정 > 웹훅으로 이동
- 웹훅 추가 > Gitea를 클릭
- 대상 URL에 http://<gitea2slack_ip>:8765/webhook을 입력. 여기서 <gitea2slack_ip>는 Gitea2Slack을 실행하는 서버의 IP 주소나 도메인
- HTTP 방식을 POST로 설정
- POST 콘텐츠 유형으로 application/json을 선택
- Trigger On에서 Custom Events를 선택
- Pull Request Assigned와 Pull Request Reviewed를 체크하여 어떤 이벤트가 알림을 트리거할지 지정
  
모든 설정이 완료되었으며 이제 Gitea2Slack은 지정된 이벤트에 대한 Gitea 리포지토리의 알림을 직접 Slack 워크스페이스로 전달함