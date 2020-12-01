import string
import tensorflow.keras
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
from flask import Flask, request, jsonify, url_for, send_file, send_from_directory, safe_join
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import nltk
import pickle
import json
import numpy as np
import requests
import random
import secrets
import csv

from werkzeug.exceptions import abort

db = create_engine('sqlite:///Employee.db')

from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

with open("data.pickle", "rb") as f:
    bag, labels, trainX, trainY = pickle.load(f)


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Employee.db'
app.config["CLIENT_CSV"]='C:/Users/hp/PycharmProjects/chatbot'


db=SQLAlchemy(app)
db.init_app(app)


class Employee(db.Model):
    EmployeeId = db.Column(db.Integer,primary_key=True)
    EmployeeName = db.Column(db.String(100),nullable=False)
    ActiveInactive = db.Column(db.String(100), nullable=False)
    Status=db.Column(db.String(100), nullable=True)
    ReleaseType=db.Column(db.String(100), nullable=True)
    PlannedReleaseDate=db.Column(db.String(100), nullable=True)
    ActualReleaseDate=db.Column(db.String(100), nullable=True)
    BillingEndDate=db.Column(db.String(100), nullable=True)
    Group=db.Column(db.String(100), nullable=True)
    BRM=db.Column(db.String(100), nullable=True)
    EM=db.Column(db.String(100), nullable=True)
    DM=db.Column(db.String(100), nullable=True)
    FPorTandM=db.Column(db.String(100), nullable=True)
    FactoryNameorFPSOWName=db.Column(db.String(100), nullable=True)
    TCSRateCardRole=db.Column(db.String(100), nullable=True)
    Location=db.Column(db.String(100), nullable=True)
    PersonType=db.Column(db.String(100), nullable=True)
    IOU=db.Column(db.String(100), nullable=True)
    Unit=db.Column(db.String(100), nullable=True)
    MarchRationalizationEligibility=db.Column(db.String(100), nullable=True)
    TCSJoiningDate=db.Column(db.String(100), nullable=True)
    BillingStartDate=db.Column(db.String(100), nullable=True)
    ContactNumber=db.Column(db.String(100), nullable=True)
    Skill=db.Column(db.String(100), nullable=True)
    WorkdayID=db.Column(db.String(100), nullable=True)
    DeptIDandProjectCode=db.Column(db.String(100), nullable=True)
    ReasonForRelease=db.Column(db.String(100), nullable=True)
    Coments=db.Column(db.String(100), nullable=True)
    TCSRateCardRole=db.Column(db.String(100), nullable=True)
    RampdownFutureHoldingOpportunity=db.Column(db.String(100), nullable=True)
    AssetID = db.Column(db.String(100), nullable=False)

class Asset(db.Model):
    EmployeeId = db.Column(db.Integer, primary_key=True)
    EmployeeName = db.Column(db.String(100), nullable=True)
    DM=db.Column(db.String(100), nullable=True)
    BCPworkingMode=db.Column(db.String(100), nullable=True)
    Branch=db.Column(db.String(100), nullable=True)
    AssetID=db.Column(db.Unicode(100), nullable=True)
    OldDeskId=db.Column(db.Unicode(100), nullable=True)
    MakeandModel=db.Column(db.Unicode(100), nullable=True)

def findaddress(sentence):
    print('entered find location')
    user = []
    entity=""
    for word in sentence.split(" "):
        if word not in bag:
            try:
                user = Employee.query.filter_by(Location=str(word).capitalize()).limit(10).all()
                if user:
                    break
            except:
               pass
    print("user find successfully")
    print(user)
    if not user:
        print(" if entered ")
        str2 = "sorry , employee not found"
        return str2
    else:
        print(" else entered")
        print("user find successfully")
        str1 = ""
        #for i in user:
            #str1 = str1 + "\n" + 'ID:' + " " + str(i.EmployeeId) + "  " + 'NAME:' + " " + str(i.EmployeeName) + " "
        #print(str1)
        
        res = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(10))
        fname=res+'.csv'
        with open(fname, mode='w') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow(
                ["EmployeeId", "EmployeeName", "Status", "ReleaseType", "Group", "BRM", "TCSRateCardRole", "Location",
                 "PersonType", "Unit", "TCSJoiningDate", "Skill", "WorkdayID"])
            for i in user:
                employee_writer.writerow(
                    [i.EmployeeId, i.EmployeeName, i.Status, i.ReleaseType, i.Group, i.BRM, i.TCSRateCardRole,
                     i.Location, i.PersonType, i.Unit, i.TCSJoiningDate, i.Skill, i.WorkdayID])

        #print(url_for(documents(res)))

        #return url_for(documents(res))
        print("http://localhost:5500/get-csv/"+res+"csv")
        #return "C:/Users/hp/PycharmProjects/chatbot/"+res
        return "http://localhost:5500/get-csv/" + res+".csv"

def findpost(sentence):
    print('entered find persontype')
    user = []
    for word in sentence.split(" "):
        if word not in bag:
            try:
                user = Employee.query.filter_by(PersonType=str(word)).limit(5).all()
                if user:
                    break
            except:
                pass
    print("user find successfully")
    print(user)

    if not user:
        print(" if entered ")
        str2 = "sorry , employee not found"
        return str2
    else:
        print(" else entered")
        print("user find successfully")
        str1 = ""
        for i in user:
            str1 = str1 + "\n" + 'ID:' + " " + str(i.EmployeeId) + "  " + 'NAME:' + " " + str(i.EmployeeName) + " "
        print(str1)
        return user

def findunit(sentence):
    print('entered find technology')
    user = []
    word_list=sentence.split()
    w=word_list[-1]
    for word in sentence.split():
        if word not in bag:
            print(word)
            try:
                if 'and' in sentence:
                    user = Employee.query.filter_by(Unit=str(word).capitalize(),Location=str(w).capitalize()).limit(10).all()
                else:
                    user = Employee.query.filter_by(Unit=str(word).capitalize()).limit(10).all()
                if user:
                    break
            except:
                pass
    print("user find successfully")
    print(user)

    if not user:
        print(" if entered ")
        str2="sorry , employee not found"
        return str2
    else:
        print(" else entered")
        print("user find successfully")
        str1 = ""
        # for i in user:
        # str1 = str1 + "\n" + 'ID:' + " " + str(i.EmployeeId) + "  " + 'NAME:' + " " + str(i.EmployeeName) + " "
        # print(str1)

        res = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(10))
        fname = res + '.csv'
        with open(fname, mode='w') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow(
                ["EmployeeId", "EmployeeName", "Status", "ReleaseType", "Group", "BRM", "TCSRateCardRole", "Location",
                 "PersonType", "Unit", "TCSJoiningDate", "Skill", "WorkdayID"])
            for i in user:
                employee_writer.writerow(
                    [i.EmployeeId, i.EmployeeName, i.Status, i.ReleaseType, i.Group, i.BRM, i.TCSRateCardRole,
                     i.Location, i.PersonType, i.Unit, i.TCSJoiningDate, i.Skill, i.WorkdayID])

        # print(url_for(documents(res)))

        # return url_for(documents(res))
        print("http://localhost:5500/get-csv/" + res + "csv")
        # return "C:/Users/hp/PycharmProjects/chatbot/"+res
        return "http://localhost:5500/get-csv/" + res + ".csv"


def findid(sentence):
    print('entered find id')
    entity=""
    user=[]
    for word in sentence.split():
        print(word)
        if word not in bag:
            print(word)
            try:
                user = Employee.query.filter(Employee.EmployeeName.like(str(word)+"%")).limit(5).all()
                if user:
                    break
            except:
                pass

    print(user)
    if not user:
        print(" if entered ")
        dict1={}
        str2="sorry , employee not found"
        print(dict1)
        return dict1
    else:
        print(" else entered")
        print("user find successfully")
        str1=""
        dict={}
        for i in user:
            str1 = str1+" "+'ID:'+" "+str(i.EmployeeId)+"  "+'NAME:'+" "+str(i.EmployeeName)
            dict[i.EmployeeId]=i.EmployeeName
        print(str1)
        return dict

def findlocation(sentence):
    print('entered find location')
    entity=""
    for word in sentence.split():
        print(word)
        if word not in bag:
            print(word)
            try:
                user = Employee.query.filter(Employee.EmployeeName.like(str(word)+"%")).first()
                if user:
                    break
            except:
                pass

    print(user)
    if not user:
        print(" if entered ")
        str2="sorry , employee not found"
        return str2
    else:
        print(" else entered")
        print("user find successfully")
        str1=""

        str1 = 'NAME:'+" "+str(user.EmployeeName)+" "+'Location:'+" "+str(user.Location)
        print(str1)
        return str1

def findcontact(sentence):
    print('entered find contact')
    entity=""
    for word in sentence.split():
        print(word)
        if word not in bag:
            print(word)
            try:
                user = Employee.query.filter(Employee.EmployeeName.like(str(word)+"%")).first()
                if user:
                    break
            except:
                pass

    print(user)
    if not user:
        print(" if entered ")
        str2="sorry , employee not found"
        return str2
    else:
        print(" else entered")
        print("user find successfully")
        str1=""

        str1 = 'NAME:'+" "+str(user.EmployeeName)+" "+'Contact:'+" "+str(user.ContactNumber)
        print(str1)
        return str1

def findAssetid(sentence):
    print('entered find Asset id')
    entity=""
    for word in sentence.split():
        print(word)
        if word not in bag:
            print(word)
            try:
                user = Employee.query.filter(Employee.EmployeeName.like(str(word)+"%")).first()
                if user:
                    break
            except:
                pass

    print(user)
    if not user:
        print(" if entered ")
        str2 = "sorry , employee not found"
        return str2
    else:
        print(" else entered")
        print("user find successfully")
        str1 = ""
        str3=user.EmployeeName
        r= db.session.query(Employee,Asset).outerjoin(Asset,Employee.EmployeeId==Asset.EmployeeId)
        for row in r:
            if row[1]:
                if row[0].EmployeeName==str3:
                    print('Assetid: '+ row[1].AssetID)
                    str1 = 'NAME:' + " " + str(row[0].EmployeeName) + "  " + 'AssetId:' + " " + str(row[1].AssetID) + " "
        print(str1)
        return str1

def findBranch(sentence):
    print('entered find Branch')
    entity = ""
    for word in sentence.split():
        if word not in bag:
            try:
                user = Employee.query.filter(Employee.EmployeeName.like(str(word)+"%")).first()
                if user:
                    break
            except:
                pass

    print(user)
    if not user:
        print(" if entered ")
        str2 = "sorry , employee not found"
        return str2
    else:
        print(" else entered")
        print("user find successfully")
        str1 = ""
        str3=user.EmployeeName
        r= db.session.query(Employee,Asset).outerjoin(Asset,Employee.EmployeeId==Asset.EmployeeId)
        for row in r:
            if row[1]:
                if row[0].EmployeeName==str3:
                    print('Assetid: '+ row[1].AssetID)
                    str1 = 'NAME:' + " " + str(row[0].EmployeeName) + "  " + 'Branch:' + " " + str(row[1].Branch) + " "
        print(str1)
        return str1

def findupdatedetails(sentence):
    print('entered find update-details')
    entity = ""
    for word in sentence.split():
        if word not in bag:
            try:
                user = Employee.query.filter(Employee.EmployeeName.like(str(word)+"%")).first()
                if user:
                    break
            except:
                pass

    print(user)
    word_list=sentence.split()
    newnum=word_list[-1]
    print(user.EmployeeName,user.ContactNumber,newnum)

    if not user:
        print(" if entered ")
        str2 = "sorry , employee not found"
        return str2
    else:
        print(" else entered")
        print("user find successfully")
        user.ContactNumber=newnum
        db.session.commit()
        str2 = "Contact updated successfully"
        return str2


def findmakemodel(sentence):
    print('entered find make and model')
    entity=""
    for word in sentence.split():
        if word not in bag:
            try:
                user = Employee.query.filter(Employee.EmployeeName.like(str(word)+"%")).first()
                if user:
                    break
            except:
                pass

    print(user)
    if not user:
        print(" if entered ")
        str2 = "sorry , employee not found"
        return str2
    else:
        print(" else entered")
        print("user find successfully")
        str1 = ""
        str3=user.EmployeeName
        r= db.session.query(Employee,Asset).outerjoin(Asset,Employee.EmployeeId==Asset.EmployeeId)
        for row in r:
            if row[1]:
                if row[0].EmployeeName==str3:
                    print('Assetid: '+ row[1].AssetID)
                    str1 = 'NAME:' + " " + str(row[0].EmployeeName) + "  " + 'Make/Model:' + " " + str(row[1].MakeandModel) + " "
        print(str1)
        return str1

def findworkingmode(sentence):
    print('entered find BCP working mode')
    entity=""
    for word in sentence.split(" "):
        if word not in bag:
            try:
                user = Employee.query.filter(Employee.EmployeeName.like(str(word)+"%")).first()
                if user:
                    break
            except:
                pass

    print(user)
    if not user:
        print(" if entered ")
        str2 = "sorry , employee not found"
        return str2
    else:
        print(" else entered")
        print("user find successfully")
        str1 = ""
        str3=user.EmployeeName
        r= db.session.query(Employee,Asset).outerjoin(Asset,Employee.EmployeeId==Asset.EmployeeId)
        for row in r:
            if row[1]:
                if row[0].EmployeeName==str3:
                    print('Assetid: '+ row[1].AssetID)
                    str1 = 'BCP working mode' + " " + str(row[1].BCPworkingMode) + " "
        print(str1)
        return str1

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]


    out=[]
    for w in words:
        if w in s_words:
            out.append(1)
        else:
            out.append(0)
    return np.array([out])

@app.route('/get-csv/<path:token>')
def documents(token):
    print("document function entered")
    filename = f"{token}"
    print(filename)
    safe_path = safe_join(app.config["CLIENT_CSV"], filename)
    try:
       return send_file(safe_path,as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route('/',methods=['Post'])
def chat():
    res=request.json
    inp=res['text']
    model=tf.keras.models.load_model('chatbot')
    print(model)
    print("Exsisting model loaded")

    results = model.predict([bag_of_words(inp,bag)])[0]
    results_index = np.argmax(results)
    tag = labels[results_index]
    print("tag traced", tag)

    t = {'text': '',
         'link':'',
         'list':''
         }
    if tag == 'employee->post':
        t['text'] = findpost(inp)

    elif tag == "employee->branch":
        t['text'] = findBranch(inp)

    elif tag == 'employee->details':
        t['text'] = findAssetid(inp)

    elif tag == 'emplyeeid':
        t['list'] = findid(inp)

    elif tag == 'employee->address':
        t['link'] = findaddress(inp)

    elif tag == "employee->technology":
        t['link'] = findunit(inp)

    elif tag == "employee->location":
        t['text'] = findlocation(inp)

    elif tag == "employee->contact":
        t['text'] = findcontact(inp)

    elif tag == "employee->update-details":
        t['text'] = findupdatedetails(inp)

    elif tag == "employee->model":
        t['text'] = findmakemodel(inp)

    elif tag == "employee->workingmode":
        t['text'] = findworkingmode(inp)

    elif tag == 'greet': 
        t['text']='sorry'

    elif tag == 'thank':
        t['text']= 'Welcome!'

    else:
        t['text'] = 'Sorry didnt get that'

    res = requests.post(url='http://127.0.0.1:5200/reply', json=t)
    print(res)
    return jsonify(t)

def chat2(inp):
    model=tf.keras.models.load_model('chatbot')
    print("Exsisting model loaded")

    results = model.predict([bag_of_words(inp,bag)])[0]
    print("line1")
    results_index = np.argmax(results)
    print("line1")
    tag = labels[results_index]
    print("tag traced")

    t = {'text': '',
         'link':'',
         'list':''
         }
    if tag == 'employee->post':
        t['text'] = findpost(inp)

    elif tag == 'employee->details':
        t['text'] = findAssetid(inp)

    elif tag == 'emplyeeid':
        t['list'] = findid(inp)

    elif tag == 'employee->address':
        t['link'] = findaddress(inp)

    elif tag == "employee->technology":
        t['text'] = findunit(inp)

    elif tag == "employee->branch":
        t['text'] = findBranch(inp)

    elif tag == "employee->update-details":
        t['text'] = findupdatedetails(inp)

    elif tag == "employee->model":
        t['text'] = findmakemodel(inp)

    elif tag == "employee->workingmode":
        t['text'] = findworkingmode(inp)

    elif tag == 'greet': 
        t['text']='Hi, How can I help you?'

    elif tag == 'thank':
        t['text']= 'Welcome!'

    else:
        t['text'] = 'Sorry didnt get that'

    res = requests.post(url='http://127.0.0.1:5200/reply', json=t)
    print(res)
    return jsonify(t)
    #print(res)
    #return t['text']

if __name__ =='__main__':
	app.run(port=5500,debug=True)





