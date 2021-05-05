import csv, smtplib, ssl
import pandas as pd

data = pd.read_csv(r'/home/blake/PycharmProjects/email-toolbox/customers.csv')
df = pd.DataFrame(data, columns=['Name', 'Email', 'Balance'])
print(df)


message = """\
From: {sender}
To: {email}
Subject: Your Balance

Hi {name} your balance is {balance}.
"""

sender = 'bburns858@gmail.com'
password = input('Please enter password here:')

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
    server.login(sender, password)
    with open('customers.csv') as file:
        reader = csv.reader(file)
        next(reader)
        for name, email, balance in reader:
            server.sendmail(
                sender,
                email,
                message.format(
                    sender=sender,
                    email=email,
                    name=name,
                    balance=balance,
                )
            )
