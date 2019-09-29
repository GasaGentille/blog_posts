from datetime import datetime
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager

@login_manager.user_loader
def load_writer(writer_id):
    return Writer.query.get(int(writer_id))

# class User(UserMixin,db.Model):
#     __tablename__ = 'users'
#     email = db.Column(db.String(255),unique = True,index = True)
#     posts = db.relationship('Post',backref = 'user',lazy = "dynamic")
#     comments = db.relationship('Comment',backref = 'user',lazy="dynamic") 

class Writer(UserMixin,db.Model):
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

class Post(db.Model):
    __tablename__='pitches'
    id = db.Column(db.Integer,primary_key = True)
    post_title = db.Column(db.String)
    post_content = db.Column(db.String(255))
    writer_id = db.Column(db.Integer,db.ForeignKey("writers.id"))
    comments = db.relationship('Comment',backref = 'post_id',lazy = "dynamic")
   

    def save_post(self):
        db.session.add(self)
        db.session.commit()

    # @classmethod
    # def get_s(cls,category):
    #     pitches = Pitch.query.filter_by(category=category).all()
    #     return pitches

    @classmethod
    def get_post(cls,id):
        post = Post.query.filter_by(id=id).first()
        return post

    @classmethod
    def count_posts(cls,uname):
        writer = Writer.query.filter_by(username=uname).first()
        posts = Post.query.filter_by(writer_id=writer.id).all()

        posts_count = 0
        for post in posts:
            posts_count +=1
        return posts_count

class Comment(db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String(255))
    writer_id = db.Column(db.Integer,db.ForeignKey("writers.id"))
    post = db.Column(db.Integer,db.ForeignKey("posts.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def get_comments(cls,post):
        comments = Comment.query.filter_by(post_id=post).all()
        return comments

