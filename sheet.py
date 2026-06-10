import os
import json
import tempfile
import gspread

from google.oauth2.service_account import Credentials

def get_sheet():

    creds_json = json.loads(
        os.getenv("GOOGLE_CREDENTIALS_JSON")
    )

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        delete=False
    ) as f:

        json.dump(creds_json, f)

        temp_file = f.name

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_file(
        temp_file,
        scopes=scope
    )

    client = gspread.authorize(creds)

    spreadsheet_id = os.getenv("SPREADSHEET_ID")

    return client.open_by_key(
        spreadsheet_id
    ).worksheet("expenses")