from flask import Flask, render_template, url_for, request

from geopy.geocoders import Nominatim
import math
import MySQLdb

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title = "Najděte nejlepší školku")

@app.route("/projekt")
def projekt():
    return render_template("projekt.html", title = "O projektu")

@app.route("/autorky")
def autorky():
    return render_template("autorky.html", title = "Autorky")

@app.route("/english")
def english():
    return render_template("english.html", title = "English")

@app.route("/map")
def map():
    return render_template("map.html", title = "Map")

@app.route("/skolky", methods=["POST"])
def skolky():
    hledanemisto=request.form["misto"]

    def haversine(coord1, coord2):
        R = 6372800  # Earth radius in meters
        lat1, lon1 = coord1
        lat2, lon2 = coord2

        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi       = math.radians(lat2 - lat1)
        dlambda    = math.radians(lon2 - lon1)

        a = math.sin(dphi/2)**2 + \
            math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2

        return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))

    geolocator = Nominatim(user_agent="mooi@email.cz")
    location = geolocator.geocode(hledanemisto)
    lat1 = location.latitude
    lon1 = location.longitude

    #print(lat1, lon1)

    poradi_vzdalenosti = []

    conn = MySQLdb.connect("martiik.mysql.pythonanywhere-services.com", "martiik", "databaze", "martiik$skolky", charset="utf8", use_unicode=True)
    c = conn.cursor()
    c.execute("SELECT * FROM lesni2")
    rows = c.fetchall()
    for row in rows:
        lat2 = float(row[4])
        lon2 = float(row[5])
        if ( lat2 < (lat1+0.065)) and (lat2 > (lat1-0.065)) and (lon2 > (lon1-0.163)) and (lon2 < (lon1+0.163)):
        	coord1 = lat1, lon1
        	coord2 = lat2, lon2
        	vzdalenost = (haversine(coord1, coord2))/1000
        	poradi_vzdalenosti.append([row[1], row[2], row[3], float('%2.2f' % (vzdalenost)), row[4], row[5]])

    poradi = sorted(poradi_vzdalenosti, key=lambda x: x[3])

    return render_template("skolky.html", title = "Nalezené školky", misto=hledanemisto, vysledne_poradi=poradi)



"""
fname = request.form.get('fname')

if __name__=="__name__":
	app.run(debug=True)
"""