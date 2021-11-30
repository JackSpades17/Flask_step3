from flask import Flask, render_template,request
from flask_wtf import FlaskForm
import requests
from wtforms.validators import InputRequired, Email, NumberRange
from wtforms import StringField,TextAreaField,IntegerField,BooleanField,RadioField,SelectField
import data
import os
import json
import random

app = Flask(__name__)
app.secret_key=os.urandom(20)

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
    slct_rq = RadioField('goal', choices = [("Для путешествий"),("Для школы"),("Для работы"),("Для переезда")])
    slct_time = RadioField('goal_time', choices = [("1-2 часа в неделю"),("3-5 часов в неделю"),("5-7 часов в неделю"),("7-10 часов в неделю")])

@app.route('/')
def render_index():

    with open('data.json') as f:
        data = json.load(f)
    a=len(data["teachers"])
    mas = random.sample(range(1,a),6)
    return render_template("index.html",data=data,mas=mas)

@app.route('/profiles/<id>')
def profiles_id(id):
    with open('data.json') as f:
        data = json.load(f)
    id = int(id)
    data_goals = data["goals"]
    data=data["teachers"][id]

    return render_template("profile.html",data=data,data_goals=data_goals)

@app.route('/booking/<id>/<day_week>/<day_time>/')
def booking_form(id,day_week,day_time):
    D = {"mon":"Понедельник","tue":"Вторник","wed":"Среда","thu":"Четверг","fri":"Пятница","sat":"Суббота","sun":"Воскресенье"}
    form2 = BookingFormTwo()
    form = BookingForm ()
    with open('data.json') as f:
        data = json.load(f)
    id = int(id)
    data=data["teachers"][id]

    return render_template("booking.html",data=data,day_week=day_week,day_time=day_time,d_week=D[day_week],form=form,form2=form2)

@app.route('/booking_done', methods=["GET","POST"])
def bookings_done():
    D = {"Понедельник":"mon","Вторник":"tue","Среда":"wed","Четверг":"thu","Пятница":"fri","Суббота":"sat","Воскресенье":"sun"}
    form = BookingForm()
    form2 = BookingFormTwo()
    name_cl=form.name_cl.data
    phone=form.phone.data
    day_w=form2.day_w.data
    day_week = D[day_w]
    day_t=form2.day_t.data
    clnt_id=form2.clnt_id.data
    clnt_id = int(clnt_id)
    with open('data.json') as f:
        data = json.load(f)
        data["teachers"][clnt_id]["free"][day_week][day_t]=False    
    with open ('data.json','w') as f:
        json.dump(data,f,indent=4,ensure_ascii=False)
    return render_template("booking_done.html",name_cl=name_cl,day_w=day_w,day_t=day_t,phone=phone)
@app.route('/all')
def coach_all():
    form = SelectForm()
    with open('data.json') as f:
        data = json.load(f)
    a=len(data["teachers"])
    return render_template("all.html",a=a,data=data,form=form)


@app.route('/all',methods=["POST"])
def coach_all_post():
    form = SelectForm()
    slct_check = form.slct.data
    with open('data.json') as f:
        data = json.load(f)
    with open('data.json') as g:   
        sorted_rating = json.load(g)
    a=len(data["teachers"])
    lst=[]

    if slct_check == "Сначала лучшие по рейтингу":

        for i in range(0,a):    
            lst.append(data["teachers"][i]["rating"])
        lst=sorted(lst)
        lst=reversed(lst)
        j=-1
        del_lst=[]
        for x in lst:
            j+=1
            for i in range(0,a):
                if data["teachers"][i]["rating"]==x and i not in del_lst:
                    sorted_rating["teachers"][j]=data["teachers"][i]
                    del_lst.append(i)
                    break
        data=sorted_rating

    elif slct_check == "Сначала дорогие":

        for i in range(0,a):    
            lst.append(data["teachers"][i]["price"])
        lst=sorted(lst)
        lst=reversed(lst)
        j=-1
        del_lst=[]
        for x in lst:
            j+=1
            for i in range(0,a):
                if data["teachers"][i]["price"]==x and i not in del_lst:
                    sorted_rating["teachers"][j]=data["teachers"][i]
                    del_lst.append(i)
                    break
        data=sorted_rating

    elif slct_check == "Сначала недорогие":

        for i in range(0,a):    
            lst.append(data["teachers"][i]["price"])
        lst=sorted(lst)
        j=-1
        del_lst=[]
        for x in lst:
            j+=1
            for i in range(0,a):
                if data["teachers"][i]["price"]==x and i not in del_lst:
                    sorted_rating["teachers"][j]=data["teachers"][i]
                    del_lst.append(i)
                    break
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
    goal_check = form.slct_rq.data
    time = form.slct_time.data
    name_cl=form1.name_cl.data
    phone=form1.phone.data   
    return render_template("request_done.html",goal_check=goal_check,time=time,name_cl=name_cl,phone=phone)




@app.route('/goal/<goal>')
def goals(goal):
    with open('data.json') as f:
        data = json.load(f)
    some_d = {}
    k=-1
    for i in data["teachers"]:
        for j in i["goals"]:
            if j==goal:
                k+=1
                some_d[k]=i
    label = data["goals"][goal]
    label = "д"+label[1:]
    a=len(some_d)
    return render_template("goal.html",data=some_d,mas=a,label = label)
    
if __name__ == '__main___':
    app.run(debug=True)

