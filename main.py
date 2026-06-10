import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SPREADSHEET_ID = "10cCg2T6hn-x9wj8M7zlyLp6ms9Qelv7qA9kM-e7afHQ"

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "service_account.json",
    scopes=scope
)

client = gspread.authorize(creds)

sheet = client.open_by_key(SPREADSHEET_ID).worksheet("expenses")

sheet.append_row([
    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    500,
    "ข้าวเย็น",
    "A"
])

print("เพิ่มข้อมูลเรียบร้อย 🎉")