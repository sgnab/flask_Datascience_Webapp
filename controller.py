from flask import Flask,request,render_template,flash,redirect,session,url_for
import flask_login,flask_mail,flask_sqlalchemy
from wtforms import FloatField,Form,validators
from loginout import login_required
from MySQLdb import escape_string as thwart
import bcrypt
from model import InputForm,RegisterationForm,LoginForm
from mycompute import compute
import gc
import MySQLdb
import sqlite3


db = sqlite3.connect('mydata.db')

app = Flask(__name__)

app.secret_key="super_secret_key"
@app.route("/",methods = ['GET','POST'])
def index():
    return render_template('homepage.html')

@app.route('/logout')
@login_required
def log_out():
    session.clear()
    flash("You have been logged out")
    gc.collect()
    return redirect(url_for("index"))


@app.route('/todo', methods = ['GET','POST'])
@login_required
def todo():
    # session.clear()

    form = InputForm(request.form) #making a form object based on datab in model
    if request.method=="POST" and form.validate(): # make sure that user is posting something
        for field in form:
            exec('%s = %s' %(field.name,field.data))
        result = compute(A, w, b,T) #defining the inputs "from.?.data" and execute computation
        print result[0]
    else:
        result = None
    return render_template("mainpage.html",form=form,result=result) #passing the variables to the template
    # return render_template("test_main.html",form=form,result=result) #passing the variables to the template



@app.route('/register', methods = ['GET','POST'])
def register1():
    try:
        form = RegisterationForm(request.form)
        print "form"
        if request.method =="POST" and form.validate():
            print "post validated"
            username = form.user.data
            email = form.email.data
            password = str(form.pswd.data)
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            print "variables valid"
            conn = sqlite3.connect('mydata.db')
            c = conn.cursor()
            print "cursor"
            c.execute('CREATE TABLE IF NOT EXISTS users2(uid INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR(50), password VARCHAR(50)'
                      ', email VARCHAR(50))')
            print "table created"
            x=c.execute("SELECT * FROM users2 WHERE username = ('%s')" %(username))
            x = c.fetchone()
            if x:
                flash("This username is already taken, please choose another")
                return render_template("register.html",form=form)
            else:
                print "some"
                c.execute("INSERT INTO users2(username, password, email) VALUES('%s','%s','%s')" %(username,hashed,email))
                conn.commit()
                flash("Thanks for Registering :)")
                c.close()
                conn.close()
                gc.collect()
                session['logged_in']=True
                session['username'] = username
                return redirect(url_for('todo'))
        return render_template("register.html",form=form)
    except Exception as e:
        return str(e)

@app.route('/login', methods = ['GET','POST'])
def login_page():
    try:
        form = LoginForm(request.form)
        if request.method =="POST":
            conn = sqlite3.connect('mydata.db')
            c = conn.cursor()
            c.execute("SELECT * FROM users2 WHERE username = ('%s')" %(request.form['user']))
            user_login = c.fetchone()
            if user_login:
                user_login = c.execute("SELECT * FROM users2 WHERE username = ('%s')" % (request.form['user']))
                user_pw = c.fetchone()[2]
                if bcrypt.checkpw(request.form['pswd'].encode('utf-8'),user_pw.encode('utf-8'))==True:
                    print "goo"
                    session['logged_in']=True
                    session['username'] = request.form['user']
                    flash("Congrat you are logged-in now!")
                    return redirect(url_for("todo"))
                else:
                    flash("Invalid Credentioals! Try again")
            else:
                flash("Invalid Credentioals! Try again")
        return render_template("login.html",form=form)
    except Exception as e:
        return str(e)

if __name__ =="__main__":
    app.run(debug=True)
#
