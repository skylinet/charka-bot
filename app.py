import os
from flask import Flask, request
from dotenv import load_dotenv
from sheet import get_sheet
from datetime import datetime

from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

load_dotenv()

app = Flask(__name__)

configuration = Configuration(
    access_token=os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
)

handler = WebhookHandler(
    os.getenv("LINE_CHANNEL_SECRET")
)


@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    handler.handle(body, signature)

    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):

    text = event.message.text.strip()

    reply_text = "ไม่เข้าใจคำสั่ง"

    if text == "/hello":
        reply_text = "สวัสดีจากเจ้าขา 👋"

    elif text.startswith("/add"):

        try:

            parts = text.split(" ", 2)

            amount = int(parts[1])

            note = parts[2]

            sheet = get_sheet()

            sheet.append_row([
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                amount,
                note,
                event.source.user_id
            ])

            reply_text = (
                f"📝 บันทึกแล้ว\n"
                f"฿{amount:,}\n"
                f"{note}"
            )

        except Exception as e:

            reply_text = f"Error: {str(e)}"

    with ApiClient(configuration) as api_client:

        MessagingApi(api_client).reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(
                        text=reply_text
                    )
                ]
            )
        )


if __name__ == "__main__":
    app.run(port=5001)