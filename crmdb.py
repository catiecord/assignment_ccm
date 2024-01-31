import mysql.connector

dataBase = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='Cordeiro123.'
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE paymentscrm")

print("Database created successfully!")
