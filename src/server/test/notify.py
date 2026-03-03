import os
import requests
from dotenv import load_dotenv

load_dotenv()

def main():
    send_line_notify('\nWarning!\n雨が降り始めました。洗濯物を回収してください。')

def send_line_notify(notification_message):
    line_notify_token = os.environ['LINE_NOTIFY_TOKEN']
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'{notification_message}'}
    requests.post(line_notify_api, headers = headers, data = data)

if __name__ == "__main__":
    main()