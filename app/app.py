import os

from flask import Flask,render_template,jsonify
from flask_mysqldb import MySQL, MySQLdb
from . import db

app = Flask(__name__)
app.config.from_mapping(
    DATABASE=os.path.join(app.instance_path, 'tourdeflask.sqlite'),
)

mysql = MySQL(app)

app.config["MYSQL_HOST"] = ""
app.config["MYSQL_USER"] = ""
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = ""


# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db.init_app(app)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")

@app.route('/api')
def data():
    return jsonify({"secret":'The cake is a lie'})

@app.route('/lecturer')
def card():
    return render_template("card.html", 
                        uuid="67fda282-2bca-41ef-9caf-039cc5c8dd69", 
                        title_before="Mgr.", 
                        first_name="Petra", 
                        middle_name="Swil", 
                        last_name="Plachá", 
                        title_after="MBA", 
                        picture_url="https://tourdeapp.cz/storage/images/2023_02_25/412ff296a291f021bbb6de10e8d0b94863fa89308843b/big.png.webp",
                        location="Brno",
                        claim="Aktivní studentka / Předsedkyně spolku / Projektová manažerka",
                        bio="Baví mě organizovat věci. Ať už to bylo vyvíjení mobilních aplikací ve Futured, pořádání konferencí, spolupráce na soutěžích Prezentiáda, pIšQworky, <b>Tour de App</b> a Středoškolák roku, nebo třeba dobrovolnictví, vždycky jsem skončila u projektového managementu, rozvíjení soft-skills a vzdělávání. U studentských projektů a akcí jsem si vyzkoušela snad všechno od marketingu po logistiku a moc ráda to předám dál. Momentálně studuji Pdf MUNI a FF MUNI v Brně.",
                        price_per_hour=1200,
                        telephone_number="+420 722 482 974",
                        emails=["placha@scg.cz","predseda@scg.cz"])
                        


if __name__ == '__main__':
    app.run()
