from datetime import datetime
from . import db
from flask_login import UserMixin,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager
datetime.utcnow

@login_manager.user_loader
def load_writer(writer_id):
    return Writer.query.get(int(writer_id))

class Writer(UserMixin,db.Model):
    __tablename__ = 'writers'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    profile_pic_path = db.Column(db.String())  
    password_hash = db.Column(db.String(255))
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
    __tablename__='posts'
    id = db.Column(db.Integer,primary_key = True)
    post_title = db.Column(db.String)
    post_content = db.Column(db.String(255))
    writer_id = db.Column(db.Integer,db.ForeignKey("writers.id"))
    comments = db.relationship('Comment',backref = 'posts',lazy = "dynamic")
   

    def save_post(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_posts(cls,id):
        posts = Post.query.filter_by(id=id).all()
        return posts

    def delete (self,id):
        comments = Comment.query.filter_by(id=id).all()
        for comment in comments:
            db.session.delete(comment)
            db.session.commit()

        db.session.delete(self)
        db.session.commit()

    def __repr__(sel):
        return f'Post {self.content}'


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
    comment = db.Column(db.Text())
    writer_id = db.Column(db.Integer,db.ForeignKey("writers.id"))
    post_id= db.Column(db.Integer,db.ForeignKey("posts.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_comment(self):
        Comment.comments.clear()
        
    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(post_id=id).all()
        return comments

    @classmethod
    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'Comment{self.comment}'

class Quotes:

    def __init__(self,author,quote):
        self.author = author
        self.quote = quote

class Subscription(db.Model):
    __tablename__="subscribers"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))

    def __repr__(self):
        return f'Subscription{self.name}'

  

