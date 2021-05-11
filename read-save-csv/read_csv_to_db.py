import csv
import MySQLdb

mydb = MySQLdb.connect(host='localhost', user='root', password='password', database='customers_db')

with open('customers.csv') as csv_file:
    csvfile = csv.reader(csv_file, delimiter=',')
    all_value = []
    for row in csvfile:
        value = (row[0], row[1], row[2])
        all_value.append(value)

query = "insert into customer_tbl(name, email, balance) values (%s,%s,%s)"

mycursor = mydb.cursor()
mycursor.executemany(query, all_value)
mydb.commit()
