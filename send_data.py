import os
import smtplib
from email.message import EmailMessage
from datetime import date,datetime

def to(to_email,body=""):
    try:
        email = 'deveshthechamp@gmail.com'
        passwd = 'DEVEsh2003'

        

        msg = EmailMessage()
        msg['To'] = to_email
        msg['Subject'] = 'Bus Data for {}'.format(str(date.today()))
        msg['From'] = email
        msg.set_content('Location data for 100 buses')

        if body != "":
            msg.set_content(body)
        
        try:
            with open('data.csv','rb') as file:
                data = file.read()

            msg.add_attachment(data,maintype='csv',subtype='csv',filename='data.csv')
        except Exception as e:
            msg.set_content("Error occurred while reading data : " + str(e) + '\n\n' + 
            'Please Contact me at +91 9978633872')

        with smtplib.SMTP('smtp.gmail.com',587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(email,passwd)

            # subject = 'Python mail'
            # body = "Mail sent from program"

            # msg = 'Subject: {}\n\n{}'.format(subject,body)

            smtp.send_message(msg)

            print('[*] Data sent to {}'.format(to_email))
    except Exception as e:
        print('[*] Error occurred while sending data')
        with open('errors.log','a') as file:
            meta_data = str(date.today()) + "  " + datetime.now().time().strftime("%H:%M:%S") + "  " + ':' + "  "
            file.write(meta_data + str(e) + '\n')
            