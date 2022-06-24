from constants import *
from Database import *
from User import *
import time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()

database = Database(SCOPE, CREDS, SHEET_NAME)
data = database.db
msg_db = Database(SCOPE, CREDS, CHAT_NAME)
messages = msg_db.db

def get_all_ips():
    return [
        user['User IP Address'] for user in data.get_all_records()
    ]

def clear_message():
    messages.update_acell('A2', '')
    messages.update_acell('B2', '')
    messages.update_acell('C2', '')
    messages.update_acell('D2', '')

def format_time(time):
    if len(time) == 4:
        return time+' '
    else:
        return time

def run():
    while ip in data.col_values(1):
        time.sleep(BOZO_NUMBER)
        if len(messages.get_all_records()) != 0:
            print(messages.get_all_records())
            print(f"|{messages.acell('B2').value}||{format_time(messages.acell('D2').value)}| {messages.acell('C2').value}")
            clear_message()

run()

input(f"{ip} not found in active users! \nYou cannot view the chat without logging in! Please run app.py")

