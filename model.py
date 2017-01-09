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








