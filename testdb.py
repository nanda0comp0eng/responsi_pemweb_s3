import mysql.connector
from mysql.connector import Error

hostname = "876ke.h.filess.io"
database = "dbkuliah_honormice"
port = "3307"
username = "dbkuliah_honormice"
password = "e3a960a71b43773752b6f42a4099582c62f0f9fa"

try:
    connection = mysql.connector.connect(host=hostname, database=database, user=username, password=password, port=port)
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

