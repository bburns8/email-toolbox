import smtplib, ssl, email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_server = 'smtp.gmail.com'
port = 465

sender = 'bburns858@gmail.com'
password = input('Enter your password here: ')
receiver = 'test@smartCDR.com'

message = MIMEMultipart('alternative')
message['Subject'] = 'Multipart Test'
message['From'] = sender
message['To'] = receiver

text = """\
Hi,
How are you?
Real Python has many great tutorials!
www.realpython.com
"""

html = """\
<html>
    <body>
        <p>Hi,<br>
            How are you?<br>
            <a href="http://www.realpython.com">Real Python</a>
            has many great tutorials.
        </p>
    </body>
</html>
"""

part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

filename = 'download.jpg'

with open(filename, 'rb') as attachment:
    part_a = MIMEBase('application' ,'octetc-stream')
    part_a.set_payload(attachment.read())

encoders.encode_base64(part_a)

part_a.add_header(
    'Content-Disposition',
    f'attachment; filename= {filename}'
)

message.attach(part1)
message.attach(part2)
message.attach(part_a)

context = ssl.create_default_context()

with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender, password)
    # send email
    server.sendmail(sender, receiver, message.as_string())
