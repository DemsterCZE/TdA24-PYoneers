import os

from flask import Flask,render_template,jsonify,request,abort
from flask_mysqldb import MySQL, MySQLdb
from . import db
import json

class HTTPMethodOverrideMiddleware(object):
    allowed_methods = frozenset([
        'GET',
        'HEAD',
        'POST',
        'DELETE',
        'PUT',
        'PATCH',
        'OPTIONS'
    ])
    bodyless_methods = frozenset(['GET', 'HEAD', 'OPTIONS', 'DELETE'])

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        method = environ.get('HTTP_X_HTTP_METHOD_OVERRIDE', '').upper()
        if method in self.allowed_methods:
            environ['REQUEST_METHOD'] = method
        if method in self.bodyless_methods:
            environ['CONTENT_LENGTH'] = '0'
        return self.app(environ, start_response)

app = Flask(__name__)
app.wsgi_app=HTTPMethodOverrideMiddleware(app.wsgi_app)

app.config.from_mapping(
    DATABASE=os.path.join(app.instance_path, 'tourdeflask.sqlite'),
)

app.config["MYSQL_HOST"] = "dbs.spskladno.cz"
app.config["MYSQL_USER"] = "student3"
app.config["MYSQL_PASSWORD"] = "spsnet"
app.config["MYSQL_DB"] = "vyuka3"
mysql = MySQL(app)

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

@app.route('/api/lecturer')
def card():
    with open("app/data/lecturer.json", encoding='utf-8') as data:
        profile=json.load(data)
    return render_template("card.html", profile=profile) #data je souhrnný obsah v json souboru ve složce data. V rámci html k nim budeme přistupovat {{data.udaj}}

@app.route('/api/lecturer/preadd')
def preadd():
    return render_template("lecturercreate.html")

@app.route('/api/lecturer', methods=["POST"])
def addLecturer():
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
        cur.execute("INSERT INTO table1 (title_before, first_name, middle_name, last_name, title_after, picture_url, location, claim, bio, price_per_hour, telephone_numbers, emails, tags_names) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (title_before, first_name, middle_name, last_name, title_after, picture_url, location, claim, bio, price_per_hour, telephone_numbers, emails, tags_names))
        mysql.connection.commit()
        cur.close()
        return render_template("index.html")


@app.route('/api/lecturer')
def showAll():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM table1')
    profile = cur.fetchall()
    print(profile)
    cur.close()
    return render_template("lecturershowall.html", profile=profile)

@app.route('/api/lecturer/<int:id>')
def showLecturer(id):
    try:
        cur =mysql.connection.cursor()
        cur.execute("select * from table1 where id=(%s)",(id,))
        profile = cur.fetchone()
        print(profile[10])
        cur.close()
        return render_template("card.html", profile=profile)
    except:
        abort(404)

@app.route('/api/lecturer/<int:id>/edit')
def preEditLecturer(id):
    return render_template("lectureredit.html", id=id)

@app.route('/api/lecturer/<int:id>', methods=['PUT'])
def editLecturer(id):  
    try:  
        if request.method=='PUT':
            cur =mysql.connection.cursor()
            cur.execute("SELECT * FROM table1 WHERE id=(%s)",(id,))
            profile = cur.fetchone()

            
            id=str(request.form.get("id"))
            titleBefore=str(request.form.get("title_before_edit"))
            firstName=str(request.form.get("first_name_edit"))
            middleName=str(request.form.get("middle_name_edit"))
            lastName=str(request.form.get("last_name_edit"))
            titleAfter=str(request.form.get("title_after_edit"))
            pictureUrl=str(request.form.get("picture_url_edit"))
            location=str(request.form.get("location_edit"))
            claim=str(request.form.get("claim_edit"))
            bio=str(request.form.get("bio_edit"))
            pricePerHour=str(request.form.get("price_per_hour_edit"))
            telephoneNumbers=str(request.form.get("telephone_numbers_edit"))
            emails=str(request.form.get("emails_edit"))
            tagsNames=str(request.form.get("tags_names_edit"))

            profileEdit=[id,titleBefore,firstName,middleName,lastName,titleAfter,pictureUrl,location,claim,bio,pricePerHour,telephoneNumbers,emails,tagsNames]

            for value in profileEdit:
                if value=="":
                    continue
                else:
                    cur.execute("UPDATE table1 SET title_before=%s, first_name=%s, middle_name=%s, last_name=%s, title_after=%s, picture_url=%s, location=%s, claim=%s, bio=%s, tags_names=%s, price_per_hour=%s, telephone_numbers=%s, emails=%s WHERE id=%s",(titleBefore, firstName, middleName, lastName, titleAfter, pictureUrl, location, claim, bio,tagsNames, pricePerHour, telephoneNumbers, emails, id))
                    mysql.connection.commit()
            cur.close()
            cur =mysql.connection.cursor()
            cur.execute("SELECT * FROM table1 WHERE id=(%s)",(id,))
            profile = cur.fetchone()
        
            cur.close()
            return render_template("card.html", profile=profile)
    except:
        abort(404)
    

@app.route('/api/lecturer/<int:id>', methods=['DELETE'])
def deleteLecturer(id):
    try:
        if request.method=='DELETE':
            cur =mysql.connection.cursor()
            cur.execeute("DELETE FROM table1 where id=%s",id)
            mysql.connection.commit()
    except:
        abort(404)



#python -m flask --app app/app.py run


if __name__ == '__main__':
    app.debug=True
    app.run()
