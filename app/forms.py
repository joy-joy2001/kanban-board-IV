from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import PasswordInput


class LoginForm(FlaskForm):
    username = StringField(label="User Name", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()],
                             widget=PasswordInput(hide_value=False))
    login_btn = SubmitField(label="LOGIN")
    recaptcha = RecaptchaField()


class RegisterForm(FlaskForm):
    username = StringField(label="User Name", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=8)],
                             widget=PasswordInput(hide_value=False),)
    login_btn = SubmitField(label="REGISTER")
    recaptcha = RecaptchaField()
