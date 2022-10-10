
from unicodedata import category
from flask import Flask, render_template, request, session, url_for, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from io import BytesIO
from datetime import datetime
import os
import io
import urllib.request,json
import requests
import ast

app = Flask(__name__)
app.secret_key = "abcd"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cashflow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
APP_ROOT=os.path.dirname(os.path.abspath(__file__))

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(50))
    password = db.Column(db.String(20))
    income = db.Column(db.Integer)
    phoneNo = db.Column(db.String(15))
    threshold = db.Column(db.Integer)

    def __init__(self, name, email, password, income, phoneNo, threshold):
        self.name=name
        self.email=email
        self.password=password
        self.income=income
        self.phoneNo=phoneNo
        self.threshold=threshold

class Expense(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    week = db.Column(db.String(20))
    category = db.Column(db.String(20))
    spent = db.Column(db.Float)

    def __init__(self, email, week, category, spent):
        self.email=email
        self.week=week
        self.category=category
        self.spent=spent
    


class Budget(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    food = db.Column(db.Integer)
    rent = db.Column(db.Integer)
    life = db.Column(db.Integer)
    others = db.Column(db.Integer)
    

    def __init__(self, email, food, rent, life, others):
        self.email=email
        self.food=food
        self.rent=rent
        self.life=life
        self.others=others
        

@app.route("/", methods = ["GET", "POST"])
def index():
    return render_template('index.html')


@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == 'POST':
        print("im in post")
        name = request.form.get('name')
        income = request.form.get('income')
        email = request.form.get('email')
        password = request.form.get('password')
        phoneNo = request.form.get('phoneNo')
        threshold = int(0.7*income)
        print(name, email, password, phoneNo, income)
        users = User.query.all()
        for user in users:
            try:
                if email == user.email:
                        return render_template('signup.html', password=0, email=1, user_exist=0)
                    
            except:
                return "There is an error"
        
        new_entry=User(name=name, email=email, password=password, income=income, phoneNo=phoneNo, threshold=threshold)
        new_budget=Budget(email=email, food=20, rent=30, life=10, others=20)
        db.session.add(new_budget)
        db.session.commit()
        db.session.add(new_entry)
        db.session.commit()
        return render_template("login.html")
        
    else:
        return render_template("signup.html", password=0, email=0, user_exist=0)


@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == 'POST':
        print("im in post")
        email = request.form['email']
        password = request.form['password']
        print(email, password)
        users = User.query.all()
        for user in users:
            # print(user.email)
            if email == user.email: 
                if password == user.password:
                    session['name'] = user.name
                    session['email'] = user.email
                    session['income'] = user.income
                    return redirect(url_for('home'))
                
                else:
                    return render_template('login.html', credentials_incorrect=1)
            
        return render_template('signup.html', password=0, email=0, user_exist=1)
        
    else:
        return render_template("login.html", credentials_incorrect=0)


@app.route("/home", methods = ["GET", "POST"])
def home():
    if 'name' in session:
        if request.method == 'POST':
            img = request.files['img']
            filename = secure_filename(img.filename)
            # filename = 'pic'
            print(filename)
            target = os.path.join(APP_ROOT, 'static/images/')
            destination = "/bills/".join([target, filename])
            img.save(destination)
            with io.open('C:\\Users\sivaa\Desktop\Rubbix\static\images\\bills\{}'.format(filename), 'rb') as image_file:
                content = image_file.read()

            url='http://18.117.96.57:80/'
            response = requests.post(
                url, data=content,
                headers={'Content-Type': 'application/json'}
                )

            mydata=ast.literal_eval(response.content.decode('UTF-8'))
            print(mydata)
            spent=0
            for val in mydata['prices']:
                spent+=val[0]
            
            category='food'
            # mydate=datetime.date.today()
            # week=datetime.date(2022,1,20).isocalendar()[1]
            week=datetime.utcnow().isocalendar()[1]
            print(week)
            new_entry=Expense(email=session['email'], week='week '+str(week),category=category,spent=spent)
            db.session.add(new_entry)
            db.session.commit()
            
            os.remove('C:\\Users\sivaa\Desktop\Rubbix\static\images\\bills\{}'.format(filename))
            return render_template("home.html")
        
        expenses = Expense.query.all()
        expensedict={'week 1':{},'week 2':{},'week 3':{},'week 4':{}}
        total=[]
        food=[]
        rent=[]
        life=[]
        others=[]
        for expense in expenses:
            if session['email']==expense.email:
                if expense.category in expensedict[expense.week]:
                    expensedict[expense.week][expense.category]+=expense.spent
                else:
                    expensedict[expense.week][expense.category]=expense.spent
        for week,vals in expensedict.items():
            temp=0
            for key,val in vals.items():
                temp+=val
                if key=='food':
                    food.append(val)
                elif key=='rent':
                    rent.append(val)
                elif key=='life':
                    life.append(val)
                else:
                    others.append(val)
            total.append(temp)
        print(total, expensedict.values())
        session['totalcat']={'food':sum(food),'rent':sum(rent),'life':sum(life),'others':sum(others)}
        print(session['totalcat'])

        return render_template("home.html", logged=1, food=food, rent=rent, life=life, others=others, total=total)
    else:
        return render_template("index.html")

@app.route("/budget", methods = ["GET", "POST"])
def budget():
    if 'name' in session:
        if request.method == 'POST':
            email=session['email']
            food=request.form['food']
            rent=request.form['rent']
            life=request.form['life']
            others=request.form['others']
            # print(email, food, rent, life, others)
            exist_data = Budget.query.filter_by(email=email).first()
            exist_data.food=food
            exist_data.rent=rent
            exist_data.life=life
            exist_data.others=others
            db.session.commit()
        print(session['totalcat'])   
        data = Budget.query.filter_by(email=session['email']).first()
        return render_template("budget.html", income=session['income'], data=data, food=session['totalcat']['food'],rent=session['totalcat']['rent'],life=session['totalcat']['life'],others=session['totalcat']['others'])
    else:
        return render_template("index.html")


@app.route('/income', methods = ['GET','POST'])
def income():
    email=session['email']
    income=request.form['income']
    # print(income)
    exist_data = User.query.filter_by(email=email).first()
    exist_data.income=income
    session['income']=income
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/threshold', methods = ['GET','POST'])
def threshold():
    email=session['email']
    threshold=request.form['threshold']
    # print(income)
    exist_data = User.query.filter_by(email=email).first()
    exist_data.threshold=threshold
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    db.create_all()
    app.run()