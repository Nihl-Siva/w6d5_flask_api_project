from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Email


class UserLoginForm(FlaskForm):
    # email, password, first_name, last_name
    email = StringField('Email', validators = [DataRequired(), Email()])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    password = PasswordField('Password', validators = [DataRequired()])
    submit_button = SubmitField()

class BrickForm(FlaskForm):
    set_num = StringField('Set Number')
    name = StringField('name')
    year = IntegerField('year')
    theme_id = IntegerField('theme_id')
    num_parts = IntegerField('num_parts')
    set_img_url = StringField('set_img_url')
    set_url = StringField('set_url')
    submit_button = SubmitField()

