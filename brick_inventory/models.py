from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    brick = db.relationship('Brick', backref = 'owner', lazy=True)

    def __init__(self, email, password, first_name = '', last_name = '', id = '', token = ''):
        self.id = self.set_id()
        self.password = self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.token = self.set_token(24)


    def set_id(self):
        return str(uuid.uuid4())

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f"User {self.email} has been added to the database!"


class Brick(db.Model):
    id = db.Column(db.String, primary_key = True)
    set_num = db.Column(db.String)
    name = db.Column(db.String)
    year = db.Column(db.Numeric)
    theme_id = db.Column(db.Numeric)
    num_parts = db.Column(db.Numeric)
    set_img_url = db.Column(db.String)
    set_url = db.Column(db.String)
    random_joke = db.Column(db.String)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)


    def __init__(self, set_num, name, year, theme_id, num_parts, set_img_url, set_url, random_joke, user_token, id =''):
        self.id = self.set_id()
        self.set_num = set_num
        self.name = name
        self.year = year
        self.theme_id = theme_id
        self.num_parts = num_parts
        self.set_img_url = set_img_url
        self.set_url = set_url
        self.random_joke = random_joke
        self.user_token = user_token

    def set_id(self):
        return secrets.token_urlsafe()

    def __repr__(self):
        return f"The following set has been added to your collection: {self.name}"



class BrickSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'year', 'theme_id', 'num_parts', 'set_img_url', 'set_url', 'random_joke']



brick_schema = BrickSchema()
bricks_schema = BrickSchema(many=True)

    






