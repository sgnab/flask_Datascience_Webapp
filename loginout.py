from flask import url_for,flash,redirect,session
from functools import wraps
# class Log(object):

def login_required(f):

        @wraps(f)
        def wrap(*args,**kwargs):
            if "logged_in" in session:

                return f(*args,**kwargs)
            else:
                flash("You need to login")
                return redirect(url_for("login_page"))
        return wrap

