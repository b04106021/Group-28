#以下為email的import
import smtplib
from email.mime.text import MIMEText

#設定寄email的相關資訊
gmail_user = 'unclewatersource@gmail.com'
gmail_password = 'Businesscomputing0610'

msg = MIMEText("您的腳踏車剛剛已被檢舉，趕快去把腳踏車移走吧" + '\n' + '\n' + "水源阿伯")
msg['From'] = "unclewatersource@gmail.com"
msg['To'] = "@ntu.edu.tw"
msg['Subject'] = "腳踏車違規提醒"

#以下為import學號認證的function
from verify_studentid import funtion(is_student_number)

#以下為linebot的import
from flask import Flask, request, abort
from urllib.request import urlopen

#from oauth2client.service_account import ServiceAccountCredentials

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,LineBotApiError
)

################################

from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi("bz73tyjUExIIdgZ3h4VTsKC4L3Y/mmdoxW16daM8nMnjC5ii3wC23rRE0fF8Ry7+sFyINeMRHbWsdC9PY6F8xixBtnVYsPaTjF5zBfEzbywS7Lqkx1aK9JxJlbl5PnvHBAL1RiW3BD7wDoTd+QB0mwdB04t89/1O/w1cDnyilFU=")
# Channel Secret
handler = WebhookHandler("eee486e5d9aa1ed8ff0ff78eef9fd1ef")

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
# 做 chatbot 的人是要寫在這裡
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    if #獲得我要檢舉的指令:
        reply_text = '請告訴我又是哪個白癡亂停腳踏車呢，快告訴我他的學號?'
        stat = 'report'
    elif text.is_student_number() == True and stat == 'report':
        reply_text = '我知道了，那台車在哪呢，我幫你呼叫水源阿北'
    elif text == '':
        reply_text = '收到了，但檢舉不附圖，此風不可長，快上傳證據照片'
    elif event.message.type == 'image':
        reply_text = '謝謝您的幫忙，打擊亂停自行車，人人有責~ 水源感謝您'
        
#查詢的code
    elif #獲得我要查詢的指令:
        reply_text = '請輸入你的學號'
        stat = 'search'
    elif text.is_student_number == True and stat = 'search':
        #尋找資料庫
        if #在資料庫中:
    else:
        #回到原本選單

    message = TextSendMessage(reply_text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)