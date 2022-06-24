from constants import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC

class Database:
    def __init__(self, scope, creds, sheet_name):
        self.creds = SAC.from_json_keyfile_name(creds, scope)
        self.client = gspread.authorize(self.creds)
        self.db = self.client.open(sheet_name).sheet1