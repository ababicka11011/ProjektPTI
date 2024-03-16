import mysql.connector
from mysql.connector import Error


try:
    cnx = mysql.connector.connect(user="user", password="OdczytDanych", host="projektpti.mysql.database.azure.com",
                                  port=3306, database="projektpti")

    if cnx.is_connected():
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM artist;")
        record = cursor.fetchall()
        print("You're connected to database: ", record)
        cursor.close()
        cnx.close()
        print("MariaDB connection is closed")

except Error as e:
    print("Error while connecting to MariaDB", e)
