import os

from flask import Flask,render_template,jsonify
from flask_mysqldb import MySQL, MySQLdb
from . import db
import json

app = Flask(__name__)
app.config.from_mapping(
    DATABASE=os.path.join(app.instance_path, 'tourdeflask.sqlite'),
)

mysql = MySQL(app)

app.config["MYSQL_HOST"] = "dbs.spskladno.cz"
app.config["MYSQL_USER"] = "student3"
app.config["MYSQL_PASSWORD"] = "spsnet"
app.config["MYSQL_DB"] = "vyuka3"


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
    with open("./data/lecturer.json") as data:
        profile=json.load(data)
    return render_template("card.html", data=data) #data je souhrnný obsah v json souboru ve složce data. V rámci html k nim budeme přistupovat {{data.udaj}}

if __name__ == '__main__':
    app.run()
