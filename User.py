import socket
from datetime import datetime
from constants import *

class User:
    def __init__(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.ip = s.getsockname()[0]
        s.close()
        self.nickname = self.ip
        self.most_recent_msg = (None, None)
        

    def get_nickname(self):
        self.nickname = input("Nickname: ")

    def type_msg(self, msg):
        self.most_recent_msg = (msg, datetime.now().strftime('%H:%M'))

class AmbiguousUser:
    def __init__(self, ip, nickname):
        self.ip = ip
        self.nickname = nickname

    def __str__(self):
        return (f"{self.nickname}: {self.ip}")

class Server:
    def __init__(self):
        self.most_recent_request = (None, None)

    def make_request(self, request):
        self.most_recent_msg = (request, datetime.now().strftime('%H:%M'))