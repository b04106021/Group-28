import smtplib
from email.mime.text import MIMEText

gmail_user = 'unclewatersource@gmail.com'
gmail_password = 'Businesscomputing0610'

msg = MIMEText("您的腳踏車剛剛已被檢舉，趕快去把腳踏車移走吧" + '\n' + '\n' + "水源阿伯")
msg['From'] = "unclewatersource@gmail.com"
msg['To'] = "@ntu.edu.tw"
msg['Subject'] = "腳踏車違規提醒"

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(gmail_user, gmail_password)
server.send_message(msg)
server.quit()