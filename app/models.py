from datetime import datetime
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager

@login_manager.writer_loader
def load_writer(writer_id):
    return Writer.query.get(int(writer_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    posts = db.relationship('Post',backref = 'user',lazy = "dynamic")
    comments = db.relationship('Comment',backref = 'user',lazy="dynamic") 
    
