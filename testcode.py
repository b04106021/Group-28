from verify_studentid import funtion(is_student_number)

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
# Channel Secret
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

#第一則推播
try:
    line_bot_api.push_message(to, TextSendMessage(text='歡迎使用台大腳踏車機器人'))
except LineBotApiError as e:
    # error handle
    raise e

##選擇我要檢舉or我要查詢

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
def handle_message(event):
    message = Text''
