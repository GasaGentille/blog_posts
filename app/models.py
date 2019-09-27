from datetime import datetime
from . import db
from flask_login import UserMixin,WriterMixin
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager

@login_manager.writer_loader
def load_writer(writer_id):
    return Writer.query.get(int(writer_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(255),unique = True,index = True)
    posts = db.relationship('Post',backref = 'user',lazy = "dynamic")
    comments = db.relationship('Comment',backref = 'user',lazy="dynamic") 

class Writer(WriterMixin,db.Model):
    __tablename__ = 'writters'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
   
    password_secure = db.Column(db.String(255))

    pass_secure = db.Column(db.String(255))
    posts = db.relationship('Post',backref = 'writer',lazy = "dynamic")
    comments = db.relationship('Comment',backref = 'writer',lazy = "dynamic")
   

    @property
    def password(self):
        raise AttributeError('You can not read the password attribute')

    
    @password.setter 
    def password(self,password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)
    def __repr__(self):
        return f'Writer {self.username}'

