# - *- coding: utf- 8 - *-
from geopy.geocoders import Nominatim
import mysql.connector
from mysql.connector import Error, MySQLConnection
import MySQLdb
import time

def connect():
    """ Connect to MySQL database """
    try:
        conn = mysql.connector.connect(host='martiik.mysql.pythonanywhere-services.com',
                                       database='martiik$skolky',
                                       user='martiik',
                                       password='databaze')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM netradicni")

        table = cursor.fetchall()
        for row in table:
            while row is not None:
                if row[8] == "":
                    adresa = row[1]
                    print(adresa)

                    """


                    geolocator = Nominatim(user_agent="martiik@seznam.cz")
                    location = geolocator.geocode(adresa)
                    lat1 = location.latitude
                    lon1 = location.longitude
                    query1 = ("Adresa je: {}, GPS souřadnice: {}, {}".format(adresa, lat1, lon1))
                    print(query1)
                    #query = "INSERT INTO netradicni (souradnicea, souradniceb)\ VALUES("{0}, {1}".format(lat1, lon1))";
                    #cursor.execute(query)
            #print(row)
            time.sleep(3)
            #row = cursor.fetchone()


    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    connect()




import MySQLdb
#import time

geolocator = Nominatim(user_agent="mooi@email.cz")
#location = geolocator.geocode(adresa)
#lat1 = location.latitude
#lon1 = location.longitude

#print(lat1, lon1)

conn = MySQLdb.connect("martiik.mysql.pythonanywhere-services.com", "martiik", "databaze", "martiik$skolky", charset="utf8", use_unicode=True)
c = conn.cursor()
c.execute("SELECT * FROM netradicni")
rows = c.fetchall()
for row in rows:
    if row[8] == "":
        adresa = row[3]
        typ = row[0]
        souradnicea = row[8]
        print(adresa)
        print(typ)
        print(souradnicea)




        try:
            location = geolocator.geocode(adresa)
            print("{0}; {1}; {2}".format(row[0], location.latitude, location.longitude))
            time.sleep(3)
        except Exception:
            pass """