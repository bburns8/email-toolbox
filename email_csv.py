import csv, smtplib, ssl
import pandas as pd
import mysql.connector as msql
from mysql.connector import Error


customerData = pd.read_csv(r'/home/blake/PycharmProjects/email-toolbox/customers.csv', index_col=False)
df = pd.DataFrame(customerData, columns=['Name', 'Email', 'Balance'])
# print(df)
customerData.head()
try:
    conn = msql.connect(host='localhost', user='root', password='password')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE customers_db")
        print("customers_db database is created")

except Error as e:
    print("Error while connecting to MySQL", e)
try:
    conn = msql.connect(host='localhost', database='customers_db', user='root', password='')

    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS customers;')
        print('Creating table....')
        cursor.execute("CREATE TABLE customers_info (name VARCHAR(60) NULL, email VARCHAR(60) NULL, balance INT NULL)")
        print("customers table is created....")
        for i,row in customerData.iterrows():
            sql = "INSERT INTO customers_db VALUES (%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            conn.commit()
except Error as e:
    print("Error while connecting to MySQL", e)

sql = "SELECT * FROM customers"
cursor.execute(sql)
result = cursor.fetchall()
for i in result:
    print(i)
if conn.is_connected():
    cursor.close()
    conn.close()
    print("MySQL connection is closed")

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
