import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient import errors
from email.message import EmailMessage
import base64


CLIENT_SECRET_FILE = '/accounts/google_api\\credentials.json'
# CLIENT_SECRET_FILE = '/var/www/poty/accounts/google_api/credentials.json'

# gmail api 토큰 인증서 확인
def gmail_authenticate():
    SCOPES = ['https://mail.google.com/']

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)


# Gmail 메세지 작성
def create_message(sender, to, subject, message_text):
    message = EmailMessage()
    message["From"] = sender
    message["To"] = to.split(",")
    message["Subject"] = subject
    message.set_content(message_text)
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode('utf8')}


# Gmail 만든 이메일 전송
def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        return message
    except errors.HttpError as error:
        return error


def gmail_api(user_email, mail_text):
    service = gmail_authenticate()
    message = create_message("poty관리자",
                             user_email,
                             "poty커뮤니티에서 인증번호 발송해드립니다.",
                             mail_text)
    send_message(service, "me", message)
