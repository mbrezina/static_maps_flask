from flask import Flask, render_template, url_for, request

from geopy.geocoders import Nominatim
import math
import MySQLdb

app = Flask(__name__)

@app.route("/")
@app.route("/home")
@app.route("/map")
def map():
    return render_template("map.html", title="Map")

@app.route("/uvod")
def uvod():
    return render_template("uvod.html", title = "Najděte nejlepší školku")

@app.route("/analyza")
def analyza():
    return render_template("analyza.html", title = "Analýza dat")

@app.route("/autorka")
def autorka():
    return render_template("autorka.html", title = "Autorky")

@app.route("/english")
def english():
    return render_template("english.html", title = "English")

@app.route("/skolky", methods=["POST"])
def skolky():
    hledanemisto=request.form["misto"]

    """geolocator.geocode() je funkce, která vrátí souřadnice hledaného místa:"""
    geolocator = Nominatim(user_agent="mooi@email.cz")
    try:
        location = geolocator.geocode(hledanemisto)
        print(location.raw)
        lat1 = location.latitude
        lon1 = location.longitude
        #print(lat1, lon1)
    except AttributeError as error:
        return render_template("zadne_skolky.html", title="Žádné školky v oblasti", misto=hledanemisto)

    poradi_vzdalenosti = []
    conn = MySQLdb.connect("martiik.mysql.pythonanywhere-services.com", "martiik", "databaze", "martiik$skolky", charset="utf8", use_unicode=True)
    c = conn.cursor()
    c.execute("SELECT * FROM lesni2")
    rows = c.fetchall()
    ######zoom = 11
    for row in rows:
        lat2 = float(row[4])
        lon2 = float(row[5])
        """vybere pouze ty školky, které jsou ve čtverci 10x10km kolem zadaného místa:"""
        if ( lat2 < (lat1+0.065)) and (lat2 > (lat1-0.065)) and (lon2 > (lon1-0.163)) and (lon2 < (lon1+0.163)):
            coord1 = lat1, lon1
            coord2 = lat2, lon2
            vzdalenost = (haversine(coord1, coord2))/1000
            poradi_vzdalenosti.append([row[1], row[2], row[3], float('%2.2f' % (vzdalenost)), row[4], row[5]])

    if len(poradi_vzdalenosti) == 0:
        for row in rows:
            lat2 = float(row[4])
            lon2 = float(row[5])
            """zvětší se oblast pro hledání školek:"""
            if (lat2 < (lat1 + 0.1)) and (lat2 > (lat1 - 0.1)) and (lon2 > (lon1 - 0.25)) and (
                lon2 < (lon1 + 0.25)):
                coord1 = lat1, lon1
                coord2 = lat2, lon2
                vzdalenost = (haversine(coord1, coord2)) / 1000
                poradi_vzdalenosti.append([row[1], row[2], row[3], float('%2.2f' % (vzdalenost)), row[4], row[5]])
        if len(poradi_vzdalenosti) > 0:
            zoom = 10
        else:
            return render_template("zadne_skolky.html", title="Žádné školky v oblasti", misto=hledanemisto, zoom=10)

    poradi = sorted(poradi_vzdalenosti, key=lambda x: x[3])
    return render_template("skolky.html", title = "Nalezené školky", misto=hledanemisto, vysledne_poradi=poradi, zoom=11)


def haversine(coord1, coord2):
    """funkce vypočítá vzdálenost mezi dvěma body na zemi z GPS souřadnic"""
    R = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2

    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))


"""
fname = request.form.get('fname')

if __name__=="__name__":
	app.run(debug=True)
"""
