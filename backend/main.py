"""
FastAPI
Be in directory
1. first create venv

python -m venv .venv

2. Activate Virtual Env
powershell:

.venv\Scripts\Activate.ps1

3. Add .venv to gitignore
4. Install FastAPI (be in proper dir)

pip install "fastapi[standard]"

fastapi dev main.py

5. Deactivate when done working

deactivate

"""
#deactivate when done
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

app = FastAPI()

origins = [
    "http://localhost:3000",  # Default Vite port
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["+"],
)

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

@app.post("/create-test-event")
async def create_event():
    creds = None
    # Check for token.json (standard format, not pickle)
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If no valid creds, trigger the local login flow
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials to token.json
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    event_body = {
        'summary': 'React-FastAPI Test Event',
        'start': {'dateTime': '2026-05-01T09:00:00Z'},
        'end': {'dateTime': '2026-05-01T10:00:00Z'},
    }

    event = service.events().insert(calendarId='primary', body=event_body).execute()
    return {"status": "success", "event_id": event.get('id')}