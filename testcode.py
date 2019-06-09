#以下為database的import
#import database as db
from datetime import datetime

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
    #message_id = event.message.id
    if len(text) == 9:
        if is_student_number(text) == False:
            reply_text = '請輸入的學號'
        else:
            reply_text = '我們收到學號惹'

    else:
        reply_text = text
    
    message = TextSendMessage(reply_text)
    line_bot_api.reply_message(event.reply_token, message)

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        LocationSendMessage(
            title=event.message.title, address=event.message.address,
            latitude=event.message.latitude, longitude=event.message.longitude
        )
    )

@handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage))
def handle_content_message(event):
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
    elif isinstance(event.message, VideoMessage):
        ext = 'mp4'
    elif isinstance(event.message, AudioMessage):
        ext = 'm4a'
    else:
        return

    message_content = line_bot_api.get_message_content(event.message.id)
    with open(file_path, 'wb') as fd:
    for chunk in message_content.iter_content():
        fd.write(chunk)
    """
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)"""

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text="我收到圖片了")#,
#            TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
#        ])

@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=("您好，歡迎使用line台大線上檢舉違停系統!"
                                "檢舉流程: 1.按鈕: 我要檢舉"
                                                    "2.輸入被檢舉人學號(e.g. b06303150)"
                                                    "3.傳送照片違規照片"
                                                    "4.檢舉完成!"
                                                    "5.將資料傳入資料庫"
                                "查詢流程: 1.按鈕: 我想查詢"
                                                    "2.輸入您的學號:(e.g.b06303200)"
                                                    "3.系統會自動回報您的腳踏車有無被檢舉")))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(gmail_user, gmail_password)
server.send_message(msg)
server.quit()