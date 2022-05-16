from app import db, login
from flask_login import UserMixin 
from datetime import datetime as dt, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name =  db.Column(db.String)
    email =  db.Column(db.String, unique=True, index=True)
    password =  db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)

    def __repr__(self):
        return f'<User: {self.email} | {self.id}>'

    def __str__(self):
        return f'<User: {self.email} | {self.first_name} {self.last_name}>'

    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email=data['email']
        self.password = self.hash_password(data['password'])
        self.icon = data['icon']

    def save(self):
        db.session.add(self) 
        db.session.commit() 

    def to_dict(self):
        return {
            'id':self.id,
            'first_name':self.first_name,
            'last_name':self.last_name,
            'email':self.email,
            'created_on':self.created_on,
            'icon':self.icon,
            'is_admin':self.is_admin,
            'token':self.token
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    img = db.Column(db.String)
    category_id = db.Column(db.ForeignKey('category.id'))
    created_on = db.Column(db.DateTime, index=True, default=dt.utcnow)
    



@login.user_loader
def load_user(id):
    return User.query.get(int(id))

