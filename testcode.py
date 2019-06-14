from flask import Flask, request, abort
from urllib.request import urlopen
# from oauth2client.service_account import ServiceAccountCredentials

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,LineBotApiError
)

################################
import database as db

# 送信的
import send_mail as mail

# 存圖的
# import numpy as np
# import cv2

import os

from linebot.models import *

from os import listdir
from os.path import isfile, isdir, join

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
# 做 chatbot 的人是要寫在這裡，下面的 code 只是測試用的。因為下面這樣寫，所以現在輸 Hi 會得到回應 Hello ，以此類推
@handler.add(MessageEvent, message = (TextMessage, ImageMessage))
def handle_message(event):
    print(event)
    text_type = event.message.type
    if text_type == 'text':
        text = event.message.text
        if text == '我要檢舉':
            reply_text = '請輸入被檢舉人車證號碼' + '\n' + 'ex. b05702018-01'

        elif text == '我要查詢':
            reply_text = '請輸入您的學號' + '\n' + 'ex. b05702018'

        elif len(text) == 12:
            studentID = text[0:9]
            file = open('/Users/meg/PBC_finalProject/python-getting-started/photo/' + str(studentID).upper() + '.txt', 'w')
            file.close()
            mail.send(str(studentID))
            reply_text = '收到車證號碼了' + '\n' + '請傳送圖片'

        elif len(text) == 9:
            studentID = text
            mypath = "/Users/meg/PBC_finalProject/python-getting-started/photo"
            files = listdir(mypath)
            In = False
            for f in files:
                if f == str(studentID).upper() + '.txt' and str(studentID) == 'B06703028':
                    reply_text = '你去吃屎'
                    In = True
                    break
                if f == str(studentID).upper() + '.txt' and f != 'B06703028.txt':
                    reply_text = '您有被檢舉！' + '\n' + '請盡速移車或至水源牽車～'
                    In = True
                    break
            if not In:
                reply_text = '您沒有被檢舉～' + '\n' + '看來都有好好停車呢～'
        else:
            reply_text = text

    elif text_type == 'image':
        reply_text = '收到圖片了！' + '\n' + '謝謝您，檢舉已完成'

    message = TextSendMessage(reply_text)
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)