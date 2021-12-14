from flask import Flask
import json
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://jspades:1234@127.0.0.1:5432/promdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




class Teachers(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    about =db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float,  nullable=False)
    picture = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Integer,  nullable=False)
    goals = db.Column(db.String(255))
    mon = db.Column(db.String(1000), nullable=False)
    tue = db.Column(db.String(1000), nullable=False)
    wed = db.Column(db.String(1000), nullable=False)
    thu = db.Column(db.String(1000), nullable=False)
    fri = db.Column(db.String(1000), nullable=False)
    sat = db.Column(db.String(1000), nullable=False)
    sun = db.Column(db.String(1000), nullable=False)
    bron = db.relationship("Bronlist")
 
"""
siz = len(data["teachers"])
for i in range(0,siz):
    s=''
    n=0
    for j in data["teachers"][i]["goals"]:
        n+=1
        if n==1:
            s+=j
        else:
            s+=','+j
    st1 = Teachers(name = data["teachers"][i]["name"], about = data["teachers"][i]["about"], rating = data["teachers"][i]["rating"], picture = data["teachers"][i]["picture"], price = data["teachers"][i]["price"], goals = s, mon = str(data["teachers"][i]["free"]["mon"]), tue = str(data["teachers"][i]["free"]["tue"]), wed = str(data["teachers"][i]["free"]["wed"]), thu = str(data["teachers"][i]["free"]["thu"]), fri = str(data["teachers"][i]["free"]["fri"]), sat = str(data["teachers"][i]["free"]["sat"]), sun = str(data["teachers"][i]["free"]["sun"]))
    db.session.add(st1)
"""
class Bronlist(db.Model):
    __tablename__ = "bronlist"
    id = db.Column(db.Integer, primary_key=True)
    name_cl = db.Column(db.String(50), nullable=False)
    number = db.Column(db.String(50), unique=True, nullable=False)
    day_week = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(1000), nullable=False)
    teach_id =db.Column(db.Integer, db.ForeignKey("teachers.id")) 
    teach = db.relationship("Teachers")


class BronlistNew(db.Model):
    __tablename__ = "bronlistnew"
    id = db.Column(db.Integer, primary_key=True)
    name_cl = db.Column(db.String(50), nullable=False)
    number = db.Column(db.String(50), unique=True, nullable=False)
    day_week = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(1000), nullable=False)
    teach_id =db.Column(db.Integer, db.ForeignKey("teachers.id")) 
    teach = db.relationship("Teachers")


class Reqlist(db.Model):
    __tablename__ = "reqlist"
    id = db.Column(db.Integer, primary_key=True)
    name_cl = db.Column(db.String(50), nullable=False)
    number = db.Column(db.String(50), unique=True, nullable=False)
    hours = db.Column(db.String(1000), nullable=False)
    goals = db.Column(db.String(255))


db.create_all()


db.session.commit()
#print(db.session.query(User).all())