from flask import Flask,session,redirect,url_for,request,make_response
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager,UserMixin,login_required, login_user, logout_user
from subprocess import call
import os
import subprocess
#from flask.ext.session import Session
app = Flask(__name__)
#app.secret_key = 'super_secret_key'
#app.config['SECRET_KEY'] = 'oh_so_secret'
#app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///127.0.0.1.sqlite3'
db = SQLAlchemy(app)
#app.config['SERVER_NAME'] = '127.0.0.1:3000'
# app.secret_key = 'super_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "loginpage"

class students(db.Model,UserMixin):
   #id = db.Column('student_id', db.Integer, primary_key = True)
    __tablename__ = 'students'
    #id = db.Column('student_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100),primary_key = True)
    password = db.Column(db.String(100))

    def __init__(self, name,password):
        self.name = name
        self.password = password

    def __repr__(self):
        return "%s/%s" % (self.name,self.password)


class ordersdb(db.Model,UserMixin):
    #id = db.Column('student_id', db.Integer, primary_key = True)
    __tablename__ = 'ordersdb'
    id = db.Column('ordersdb_id', db.Integer, primary_key = True, autoincrement=True)
    productid = db.column(db.String(100))
    productname = db.Column(db.String(100))
    productstatus = db.Column(db.String(100))
    producturl = db.Column(db.String(100))
    costprice= db.Column(db.String(100))

    def __init__(self,productid,productname,productstatus,producturl,costprice):
        self.productid = productid
        self.productname = productname
        self.productstatus = productstatus
        self.producturl = producturl
        self.costprice = costprice

    def __repr__(self):
        return "%s/%s/%s/%s/%s" % (self.productid,self.productname,self.productstatus,self.producturl,self.costprice)

@app.route("/index",methods= ['POST','GET'])
def index():
    if request.method == 'POST':
        option = request.form['option']
        print option
        stuData = ordersdb.query.filter(ordersdb.productstatus == option)
        print stuData
        return render_template('index.html',stu = stuData)
    else:
        stuData = ordersdb.query.all()
        return render_template('index.html', stu = stuData )

@app.route("/createorder",methods = ['POST','GET'])
#@login_required
def createorder():
    if request.method == 'POST':
        productid = request.form['productid']
        productname = request.form['productname']
        orderstatus = request.form['orderstatus']
        producturl = request.form['producturl']
        costprice = request.form['costprice']
        print productid
        print productname
        print orderstatus
        print producturl
        print costprice
        order = ordersdb(productid,productname,orderstatus,producturl,costprice)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        if 'username' in session:
            return render_template('createorder.html')
        else:
            return render_template('loginpage.html',error = "please login for createorder")

@app.route("/registerpage",methods = ['POST','GET'])
def registerpage():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        if not len(name) or not len(password) or not len(confirm_password):
            return render_template('registerpage.html',error = "please use correct username and password for register page")
        if password != confirm_password:
            return render_template('registerpage.html',error = "password and confirm password must be same.")
        stu = students.query.filter(students.name == name).count()
        if stu == 1:
            return render_template('registerpage.html',error = "user already exist")
        #print "check2"
        student = students(name,password)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('loginpage'))
    else:
        return render_template('registerpage.html')

@app.route('/loginpage',methods = ['POST','GET'])
def loginpage():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        #print request.form[0]
        if not len(name) or not len(password):
            return render_template('loginpage.html',error = "please fill username and password")
        stu = students.query.filter(students.name == name).first()
        if stu == None:
            return render_template('loginpage.html',error = "please fill correct username and password")
        print stu
        correct_name = stu.name
        correct_password = stu.password
        if name == correct_name and password == correct_password:
            session['username'] = name
            print session['username']
            return redirect(url_for('index'))
        else:
            return render_template('loginpage.html',error = "please use correct username and password for login")

    if request.method == 'GET':
        return render_template('loginpage.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
        return redirect(url_for('index'))
    else:
        return render_template('loginpage.html',error = "please login for logout")

@app.route('/filemanagement',methods = ['POST','GET'])
def filemanagement():
    if request.method == 'POST':
        if 'scrap' in request.form:
            session['scrap'] = True
            print "dfsgd"
            os.getcwd()
            os.chdir("tutorial")
            os.getcwd()
            print "dfgde"
            call(["ls","-l"])
            call(["scrapy","crawl","quotes"])
            os.chdir("../")
            call(["ls","-l"])
        elif 'download' in request.form:
            txt_again = open("tutorial/quotes-1.html")
            file_data = txt_again.read()
            print file_data
            response = make_response(file_data)
            cd = 'attachment; filename=mycsv.csv'
            response.headers['Content-Disposition'] = cd
            response.mimetype='text/csv'
            return response
        else:
            print "dsfhg"
            os.getcwd()
            call(["ls","-l"])
            os.chdir("tutorial")
            os.getcwd()
            print "dfgde"
            call(["ls","-l"])
            call(["rm","quotes-1.html"])
            call(["rm","quotes-2.html"])
            call(["ls","-l"])
            session.pop('scrap', None)
            return render_template('filemanagement.html')
    if request.method == "GET" and 'username' in session:
        return render_template('filemanagement.html')
    elif request.method == "GET" and not 'username' in session:
        return render_template('loginpage.html',error = "please login for file management")

if __name__ == "__main__":
    app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
    db.create_all()
    app.debug = True
    app.run(
        host="127.0.0.1",
        port=int("8080")
  )
