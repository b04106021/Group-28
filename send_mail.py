import smtplib
from email.mime.text import MIMEText

def send(studentID):

    gmail_user = 'unclewatersource@gmail.com'
    gmail_password = 'Businesscomputing0610' # your gmail password

    msg = MIMEText('您被檢舉了！請儘速移車～～～')
    msg['Subject'] = '檢舉通知信'
    msg['From'] = gmail_user
    msg['To'] = str(studentID) + '@ntu.edu.tw'

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.send_message(msg)
    server.quit()

    print('Email sent!')