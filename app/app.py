import os

from flask import Flask,render_template,jsonify,request
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
    with open("app/data/lecturer.json", encoding='utf-8') as data:
        profile=json.load(data)
    return render_template("card.html", profile=profile) #data je souhrnný obsah v json souboru ve složce data. V rámci html k nim budeme přistupovat {{data.udaj}}

@app.route("/lecturer/create", methods=["POST"])
def add():
    if request.method=="POST":
        title_before=request.form.get("title_before")
        first_name=request.form.get("first_name")
        middle_name=request.form.get("middle_name")
        last_name=request.form.get("last_name")
        title_after=request.form.get("title_after")
        picture_url=request.form.get("picture_url")
        location=request.form.get("location")
        claim=request.form.get("claim")
        bio=request.form.get("bio")
        price_per_hour=request.form.get("price_per_hour")
        telephone_numbers=request.form.get("telephone_numbers")
        emails=request.form.get("emails")
        tags_names=request.form.get("tags_names")
        cur = mysql.connection.cursor()
        cur.execute(f"INSERT INTO table1 (title_before, first_name, middle_name, last_name, title_after, picture_url, location, claim, bio, price_per_hour, telephone_numbers, emails, tags_names) VALUES ({title_before},{first_name},{middle_name},{last_name},{title_after},{picture_url},{location},{claim},{bio},{price_per_hour},{telephone_numbers},{emails},{tags_names})")
        mysql.connection.commit()
        cur.close()



if __name__ == '__main__':
    app.run()
