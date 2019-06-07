from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class MyLoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class hf_detect(FlaskForm):
    avgbht=StringField('avgbht', 
                           validators=[DataRequired(),Length(min=2,max=4)])
    palpd=StringField('palpd', validators=[DataRequired(),Length(min=2,max=4)])
    cholestrol=StringField('cholestrol',validators=[DataRequired(),Length(min=2,max=4)])
    BMI=StringField('BMI',validators=[DataRequired(),Length(min=2,max=4)])
    age=StringField('age',validators=[DataRequired(),Length(min=2,max=4)])
    exercise=StringField('exercise',validators=[DataRequired(),Length(min=2,max=4)])
    submit = SubmitField('Login')
    





