import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def ini_calendar_api():
    global creds
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    return build('calendar', 'v3', credentials=creds)


def check_or_create_cal(calendar_name):
    page_token = None
    existing_calendar_id = None
    service = ini_calendar_api()
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()

        for entry in calendar_list['items']:
            if entry['summary'] == calendar_name:
                existing_calendar_id = entry['id']
                break
        if existing_calendar_id or not calendar_list.get('nextPageToken'):
            break
        page_token = calendar_list.get('nextPageToken')
    if existing_calendar_id:
        return existing_calendar_id
    
    new_calendar = {
        'summary': 'Reminders',
        'description':'These are your most pressing thing to complete',
        'timeZone': 'America/Edmonton'
    }
    created_calendar = service.calendars().insert(body=new_calendar).execute()
    return created_calendar['id']



def create_ygbfkm(name,about,begin,end,popup_reminder,email_reminder,calendar_id):
    try:
        service = build("calendar", "v3", credentials=creds)
        event = {
        'summary' : name ,
        'discription' : about,
        'colorId': 11,
        'start' : {
            'dateTime': begin,
            'timeZone': 'America/Edmonton',
        },
        'end': {
            'dateTime': end,
            'timeZone': 'America/Edmonton',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': popup_reminder},
                {'method': 'popup', 'minutes': email_reminder},
                ],
            },
        }
        event = service.events().insert(calendarId=calendar_id, body=event).execute()
    except HttpError as error:
      print(f"An error occurred: {error}")

def create_mid(name,about,begin,end,popup_reminder,email_reminder):
    try:
        service = build("calendar", "v3", credentials=creds)
        event = {
        'summary' : name ,
        'discription' : about,
        'colorId': 5,
        'start' : {
            'dateTime': begin,
            'timeZone': 'America/Edmonton',
        },
        'end': {
            'dateTime': end,
            'timeZone': 'America/Edmonton',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': popup_reminder},
                {'method': 'popup', 'minutes': email_reminder},
                ],
            },
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
    except HttpError as error:
      print(f"An error occurred: {error}")

def create_meh(name,about,begin,end,popup_reminder,email_reminder):
    try:
        service = build("calendar", "v3", credentials=creds)
        event = {
        'summary' : name ,
        'discription' : about,
        'colorId': 10,
        'start' : {
            'dateTime': begin,
            'timeZone': 'America/Edmonton',
            },
        'end': {
            'dateTime': end,
            'timeZone': 'America/Edmonton',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': popup_reminder},
                {'method': 'popup', 'minutes': email_reminder},
                ],
            },
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
    except HttpError as error:
      print(f"An error occurred: {error}")

def main(): 
    # 1. Initialize API and find/create the calendar
    global target_cal_id 
    target_cal_id= check_or_create_cal("Reminders")
    
    # 2. Setup Data
    name = "test"
    about = "test critical dates"
    begin = "2026-03-29T03:00:00-06:00"
    end = "2026-03-29T04:00:00-06:00" 
    popup = 10
    email = 10
    
    # 3. Create Event using the found ID
    create_ygbfkm(name, about, begin, end, popup, email, target_cal_id)
    print("Successfully added event to Reminders calendar!")

if __name__ == "__main__":
    main()