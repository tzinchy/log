import mysql.connector
import hashlib

log =  mysql.connector.connect(user='root', password='', host = 'localhost', database = 'lr2')
con = log.cursor()
con.execute("SELECT * FROM Employee")
data_employee = con.fetchall()
for i in data_employee:
    print(i)

