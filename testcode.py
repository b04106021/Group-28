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
# 做 chatbot 的人是要寫在這裡，下面的 code 只是測試用的。因為下面這樣寫，所以現在輸 Hi 會得到回應 Hello ，以此類推
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    text=event.message.text

    if (text=="Hi"):
        reply_text = "Hello"
        #Your user ID

    elif(text=="你好"):
        reply_text = "哈囉"
    elif(text=="機器人"):
        reply_text = "叫我嗎"
    else:
        reply_text = text
#如果非以上的選項，就會學你說話

    message = TextSendMessage(reply_text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)