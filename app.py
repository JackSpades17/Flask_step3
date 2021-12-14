from flask import Flask, render_template,request
from flask_wtf import FlaskForm
import requests
from wtforms.validators import InputRequired, Email, NumberRange
from wtforms import StringField,TextAreaField,IntegerField,BooleanField,RadioField,SelectField
import data
import os
import ast
import json
import random
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://jspades:1234@127.0.0.1:5432/promdb"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.secret_key=os.urandom(20)

### DATABASE ###
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
 

class Bronlist(db.Model):
    __tablename__ = "bronlist"
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
 #########################################################

class BookingForm(FlaskForm):
    name_cl = StringField('name_client', [InputRequired()])
    phone = StringField('phone', [InputRequired()])
class BookingFormTwo(FlaskForm):
    day_w = StringField('clientWeekday', [InputRequired()])
    day_t = StringField('clientTime', [InputRequired()])
    clnt_id = StringField('clientTeacher', [InputRequired()])
class SelectForm(FlaskForm):
    slct = SelectField('inlineFormCustomSelectPref', choices = [("В случайном порядке"),("Сначала лучшие по рейтингу"),("Сначала дорогие"),("Сначала недорогие")])

class RequestForm(FlaskForm):
    slct_rq = RadioField('goal', choices = [("Для путешествий"),("Для школы"),("Для работы"),("Для переезда"),("Для программирования")])
    slct_time = RadioField('goal_time', choices = [("1-2 часа в неделю"),("3-5 часов в неделю"),("5-7 часов в неделю"),("7-10 часов в неделю")])

def get_dir():
    test= db.session.query(Teachers)
    rez=[]
    n=-1
    for i in test.all():
        n+=1
        goals = i.goals.split(',')
        rez.append({"id":n,"name":i.name,"about":i.about,"rating":i.rating,"picture": i.picture,"price": i.price,"goals":goals,"mon":ast.literal_eval(i.mon),"tue":ast.literal_eval(i.tue),"wed":ast.literal_eval(i.wed),"thu":ast.literal_eval(i.thu),"fri":ast.literal_eval(i.fri),"sat":ast.literal_eval(i.sat),"sun":ast.literal_eval(i.sun)})
    n+=1
    return rez,n


@app.route('/')
def render_index():
    data = {}
    data["teachers"],a = get_dir()
    mas = random.sample(range(1,a),6)
    return render_template("index.html",data=data,mas=mas)

@app.route('/profiles/<id>')
def profiles_id(id):
    g = {"travel": "Для путешествий","study": "Для учебы","work": "Для работы","relocate": "Для переезда","it": "Для программирования"}
    id = int(id)
    id+=1
    test= db.session.query(Teachers).filter(Teachers.id==id)
    rez=[]
    data={}
    for i in test.all():
        goals = i.goals.split(',')
        rez.append({"id":id,"name":i.name,"about":i.about,"rating":i.rating,"picture": i.picture,"price": i.price,"goals":goals,"mon":ast.literal_eval(i.mon),"tue":ast.literal_eval(i.tue),"wed":ast.literal_eval(i.wed),"thu":ast.literal_eval(i.thu),"fri":ast.literal_eval(i.fri),"sat":ast.literal_eval(i.sat),"sun":ast.literal_eval(i.sun)})
    data["teachers"]=rez
    data=data["teachers"][0]
    return render_template("profile.html",data=data,data_goals=g)

@app.route('/booking/<id>/<day_week>/<day_time>/')
def booking_form(id,day_week,day_time):
    D = {"mon":"Понедельник","tue":"Вторник","wed":"Среда","thu":"Четверг","fri":"Пятница","sat":"Суббота","sun":"Воскресенье"}
    form2 = BookingFormTwo()
    form = BookingForm ()
    data = {}
    data["teachers"],a = get_dir()
    id = int(id)
    data=data["teachers"][id-1]

    return render_template("booking.html",data=data,day_week=day_week,day_time=day_time,d_week=D[day_week],form=form,form2=form2)

@app.route('/booking_done', methods=["GET","POST"])
def bookings_done():
    D = {"Понедельник":"mon","Вторник":"tue","Среда":"wed","Четверг":"thu","Пятница":"fri","Суббота":"sat","Воскресенье":"sun"}
    form = BookingForm()
    form2 = BookingFormTwo()
    book = Bronlist(name_cl=form.name_cl.data,number=form.phone.data,day_week=D[form2.day_w.data],time=form2.day_t.data,teach_id=int(form2.clnt_id.data))
    db.session.add(book)
    db.session.commit()

    return render_template("booking_done.html",name_cl=form.name_cl.data,day_w=form2.day_w.data,day_t=form2.day_t.data,phone=form.phone.data)

@app.route('/all')
def coach_all():
    form = SelectForm()
    data = {}
    data["teachers"],a = get_dir()
    return render_template("all.html",a=a,data=data,form=form)


@app.route('/all',methods=["POST"])
def coach_all_post():
    form = SelectForm()
    slct_check = form.slct.data
    data = {}
    sorted_rating = {}
    data["teachers"],a = get_dir()
    #sorted_rating["teachers"],a = get_dir()
    lst=[]
    if slct_check == "Сначала лучшие по рейтингу":

        test= db.session.query(Teachers).order_by(Teachers.rating.desc())
        rez=[]
        for i in test.all():
            goals = i.goals.split(',')
            n = i.id - 1
            rez.append({"id":n,"name":i.name,"about":i.about,"rating":i.rating,"picture": i.picture,"price": i.price,"goals":goals,"mon":ast.literal_eval(i.mon),"tue":ast.literal_eval(i.tue),"wed":ast.literal_eval(i.wed),"thu":ast.literal_eval(i.thu),"fri":ast.literal_eval(i.fri),"sat":ast.literal_eval(i.sat),"sun":ast.literal_eval(i.sun)})
        
        sorted_rating["teachers"] = rez
        data=sorted_rating
    elif slct_check == "Сначала дорогие":

        test= db.session.query(Teachers).order_by(Teachers.price.desc())
        rez=[]
        for i in test.all():
            goals = i.goals.split(',')
            n = i.id - 1
            rez.append({"id":n,"name":i.name,"about":i.about,"rating":i.rating,"picture": i.picture,"price": i.price,"goals":goals,"mon":ast.literal_eval(i.mon),"tue":ast.literal_eval(i.tue),"wed":ast.literal_eval(i.wed),"thu":ast.literal_eval(i.thu),"fri":ast.literal_eval(i.fri),"sat":ast.literal_eval(i.sat),"sun":ast.literal_eval(i.sun)})
      
        sorted_rating["teachers"] = rez
        data=sorted_rating
    elif slct_check == "Сначала недорогие":

        test= db.session.query(Teachers).order_by(Teachers.price)
        rez=[]
        for i in test.all():
            goals = i.goals.split(',')
            n = i.id - 1
            rez.append({"id":n,"name":i.name,"about":i.about,"rating":i.rating,"picture": i.picture,"price": i.price,"goals":goals,"mon":ast.literal_eval(i.mon),"tue":ast.literal_eval(i.tue),"wed":ast.literal_eval(i.wed),"thu":ast.literal_eval(i.thu),"fri":ast.literal_eval(i.fri),"sat":ast.literal_eval(i.sat),"sun":ast.literal_eval(i.sun)})
        sorted_rating["teachers"] = rez
        data=sorted_rating
    return render_template("all.html",a=a,data=data,form=form)

@app.route('/request')
def request_form():
    form = RequestForm()
    form1 = BookingForm()
    return render_template("request.html",form=form,form1=form1)


@app.route('/request_done',methods=["GET","POST"])
def requests_done():
    form = RequestForm()
    form1 = BookingForm()
    rq = Reqlist(name_cl=form1.name_cl.data,number=form1.phone.data,goals=form.slct_rq.data,hours=form.slct_time.data)
    db.session.add(rq)
    db.session.commit() 
    return render_template("request_done.html",goal_check=form.slct_rq.data,time=form.slct_time.data,name_cl=form1.name_cl.data,phone=form1.phone.data)




@app.route('/goal/<goal>')
def goals(goal):
    g = {"travel": "Для путешествий","study": "Для учебы","work": "Для работы","relocate": "Для переезда","it": "Для программирования"}
    data = {}
    data["teachers"],a = get_dir()
    some_d = {}
    k=-1
    for i in data["teachers"]:
        for j in i["goals"]:
            if j==goal:
                k+=1
                some_d[k]=i
    label = g[goal]
    label = "д"+label[1:]
    a=len(some_d)
    return render_template("goal.html",data=some_d,mas=a,label = label)
    
if __name__ == '__main___':
    app.run(debug=True)



