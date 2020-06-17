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

        curA = conn.cursor(buffered =  True)
        curB = conn.cursor(buffered =  True)

        hledani = ("SELECT id, adresa, souradnicea, souradniceb FROM netradicni WHERE souradnicea =''")
        souradnice = []
        curA.execute(hledani)

        for item in curA:
            geolocator = Nominatim(user_agent="mooi@email.cz")
            location = geolocator.geocode(item[1])
            print(item[0])
            print(item[1])
            lat = location.latitude
            print(lat)
            lon = location.longitude
            print(lon)
            souradnice.append([lat, lon, item[0]])
            time.sleep(3)

        print(souradnice)
        for row in souradnice:
            zapisovani = ("UPDATE netradicni SET souradnicea = {}, souradniceb = {} WHERE id = {}".format(row[0], row[1], row[2]))
            curB.execute(zapisovani)

        conn.commit()
        conn.close()

    except Error as e:
        print ("Error while connecting to MySQL", e)

if __name__ == '__main__':
    connect()

