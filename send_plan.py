import smtplib
from email.mime.text import MIMEText
import Topology


gmail_user = '------------@gmail.com'
gmail_password = '----------------'

to = '--------------------------'
my_message = 'This is my message'

def sendPlan(mailDict):
    to = mailDict["user_email"]
    my_message = "This is your plan.\n"
    my_message += "Total cost " + str(mailDict["cost"]) +"\n"
    for i in mailDict["plan"]:
        my_message += i + "\n"
    my_message += "Your hotel is " + mailDict["hotel_detail"]["name"] +"\n"
    my_message += "\nYour hotel address is\n" + str(mailDict["hotel_detail"]["address"]) +"\n"
    my_message += "\nYour hotel price is " + mailDict["hotel_detail"]["price"]["amount"] +"\n"
    my_message += "\nYour flight price is \n" + mailDict["flight_detail"]["fare"]["total_price"] + "\n"
    my_message += "\nYour flight information \n" + str(mailDict["flight_detail"]) + "\n"
    sendEmail(to,my_message)

def sendEmail(to,my_message):
    smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_password)
    msg = MIMEText(my_message)
    msg['Subject'] = 'Your Tourism Plan'
    msg['From'] = gmail_user
    msg['To'] = to
    smtpserver.sendmail(gmail_user, [to], msg.as_string())
    smtpserver.quit()
