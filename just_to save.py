###controller.py   ##############################################
from flask import Flask,request,render_template,flash,redirect,session,url_for
import bcrypt
from loginout import login_required
from model import InputForm,RegisterationForm,LoginForm
from MySQLdb import escape_string as thwart
from dbconnect import connection
from mycompute import compute
import gc
# db = sqlite3.connect('/home/seyed54/mysite/todo.db')

app = Flask(__name__)
app.secret_key = 'super secret key'





@app.route("/",methods = ['GET','POST'])
def index():
    # form = InputForm(request.form)
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
    else:
        result = None
    return render_template("mainpage.html",form=form,result=result) #passing the variables to the template

    # return render_template('mainpage.html',form = form,new_task=new_task)





@app.route('/register', methods = ['GET','POST'])
def register():
    try:
        form = RegisterationForm(request.form)
        if request.method =="POST" and form.validate():
            username = form.user.data
            email = form.email.data
            password=(str(form.pswd.data))
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            c,conn = connection()
            x = c.execute("SELECT * FROM users2 WHERE username =('%s')" %(thwart(username)))

            if int(x)>0:
                flash("This username is already taken, please choose another")
                return render_template("register.html",form=form)
            else:
                c.execute("INSERT INTO users2(username, password, email) VALUES(%s,%s,%s)",(thwart(username),thwart(hashed),thwart(email)))
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
            c,conn = connection()
            user_login = c.execute("SELECT * FROM users2 WHERE username = ('%s')" %(thwart(request.form['user'])))
            if int(user_login)!=0:
                user_pw = c.fetchone()[2]
                if bcrypt.checkpw(thwart(request.form['pswd']),user_pw)==True:
                    session['logged_in']=True
                    session['username'] = request.form['user']
                    flash("Congrat you are logged-in now!")
                    return redirect(url_for("todo"))

                else:
                    flash("Invalid Credentioals! Try again")
                    # return redirect(url_for("login"))
            else:
                flash("Invalid Credentioals! Try again")
                # return redirect(url_for("login"))
        return render_template("login.html",form=form)
    except Exception as e:
        return str(e)








if __name__ =="__main__":
    app.run(debug=True)

####controller.py

#### model.py#################

from wtforms import Form,validators,TextField,PasswordField,BooleanField,FloatField
from math import pi

class InputForm(Form):
    A = FloatField(label='Amplitude (m)', default = 1.0, validators= [validators.InputRequired()])
    b = FloatField(label='Damping Factor (kg/s)', default=0.0, validators= [validators.NumberRange(0,1E+20)])
    w = FloatField(label='Freuency (1/s)', default = 2*pi, validators= [validators.InputRequired()])
    T = FloatField(label='Time Interval (s)', default = 18.0, validators= [validators.InputRequired()])
class RegisterationForm(Form):
        user = TextField(label='Username',default='',validators=[validators.Length(min=8,max=12)])
        email = TextField(label='Email Address',default='',validators=[validators.input_required()])
        pswd = PasswordField(label='Password',default='',validators =[validators.required(),
                                                          validators.EqualTo('confirm', message="Passwords must match.")])
        confirm = PasswordField("Repeat Password")
        accept_tos = BooleanField('I accept the Terms of Service and the Privacy Notice (last updated Dec 2016)',validators=[validators.required()])
class LoginForm(Form):
            user = TextField(label='Username')
            pswd = PasswordField(label='Password')
            remember = BooleanField('Remember Credentials')

##end my model


#### dbconnect.py

import  MySQLdb
def connection():
    conn = MySQLdb.connect(host = 'seyed54.mysql.pythonanywhere-services.com', user="seyed54",passwd ="Pythontodo",db = "seyed54$register_info")
    c = conn.cursor()
    return c,conn

###### end dbconnect.py


###### mycompute.py
from numpy import cos,linspace,exp
import matplotlib.pyplot as plt
import os,time,glob

def damped_vibrations(A,w,b,t):
    return A*exp(-b*t)*cos(w*t)



def compute(A,w,b,T, resolution = 500):
    """Return filename of plot of the damped_vibration function."""
    t = linspace(0,T,resolution+1)
    u = damped_vibrations(A,w,b,t)
    plt.figure() # needed to avoid adding curves in plot???
    plt.plot(t,u)
    plt.title('A=%g,w=%g,b=%g'%(A,w,b))
    if not os.path.isdir('static'):
        #if the directory does not exist ,make one
        os.mkdir('static')
    else:
        #if directory does exist,
        #remove old plots
         for filename in glob.glob(os.path.join('static','*png')):
             os.remove(filename)
    #adding the plots to the directory
    # Use time since Jan 1, 1970 in filename in order make
    # a unique filename that the browser has not chached
    plotfile = os.path.join('static',str(time.time())+'.png')
    plt.savefig(plotfile)
    return  plotfile
if __name__=="__main__":
    print compute(1, 0.1, 1, 20)


######



