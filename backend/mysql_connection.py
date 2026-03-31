import pymysql

connection = pymysql.connect(user="root",
                       password="admin@123",
                       host="localhost",
                       port=3306,
                       database="trading_sim",
                       cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()
