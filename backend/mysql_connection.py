import pymysql

connection = pymysql.connect(user="root",
                       password="admin@123",
                       host="localhost",
                       port=3306,
                       database="trading_sim",
                       cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
    sql = "SHOW TABLES"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
