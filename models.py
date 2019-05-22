from __init__ import db
from flask_login import UserMixin
from datetime import datetime
class Article(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    author=db.Column(db.String(32),nullable=False)
    category=db.Column(db.String(8),nullable=False)
    title=db.Column(db.String(32),nullable=False)
    content=db.Column(db.Text,nullable=False)
    comment_num=db.Column(db.Integer,nullable=False,default=0)
    pic=db.Column(db.String(32),nullable=False)
    time=db.Column(db.DateTime,nullable=False)
class Comment(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    article_id=db.Column(db.Integer,nullable=False)
    uid=db.Column(db.String(32),nullable=False)
    content=db.Column(db.String(255),nullable=False)
    like_num=db.Column(db.Integer,nullable=False,default=0)
    read_num=db.Column(db.Integer,nullable=False,default=0)
    time=db.Column(db.DateTime,default=datetime.now)
class User(db.Model,UserMixin):#继承了UserMixin才有get_id这些方法，也可以自己覆盖
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    email=db.Column(db.String(32),nullable=False,unique=True)
    username=db.Column(db.String(32),nullable=False)
    password=db.Column(db.String(32),nullable=False)
    fans_num=db.Column(db.Integer,nullable=False,default=0)
    follow_num=db.Column(db.Integer,nullable=False,default=0)
    pic=db.Column(db.String(16),nullable=False,default='http://127.0.0.1:5050/static/img/default.jpg')

class User_headline(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    uid=db.Column(db.Integer,nullable=False)
    content=db.Column(db.String,nullable=False)
    like_num=db.Column(db.Integer,nullable=False,default=0)
    read_num=db.Column(db.Integer,nullable=False,default=0)
    pic=db.Column(db.String,nullable=False,default="")
    time=db.Column(db.DateTime,nullable=False,default=datetime.now)
    
class Collection(db.Model):
    article_id=db.Column(db.Integer,nullable=False)
    uid=db.Column(db.Integer,nullable=False)
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    time=db.Column(db.DateTime,nullable=False,default=datetime.now)
    __table_args__ = (
        db.UniqueConstraint('uid', 'article_id'),)
class Ucollection(db.Model):
    article_id=db.Column(db.Integer,nullable=False)
    uid=db.Column(db.Integer,nullable=False)
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    time=db.Column(db.DateTime,nullable=False,default=datetime.now)

    __table_args__ = (
        db.UniqueConstraint('uid', 'article_id'),)
class Authentication(db.Model):
    auth_code=db.Column(db.Integer,nullable=False)
    email=db.Column(db.String(32),nullable=False)
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    time=db.Column(db.Float,nullable=False,default=datetime.now)
class Fans(db.Model):
    uid=db.Column(db.Integer,nullable=False)
    fans_id=db.Column(db.Integer,nullable=False)
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
class Follow(db.Model):
    uid=db.Column(db.Integer,nullable=False)
    followed_id=db.Column(db.Integer,nullable=False)
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)    
class Reply(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    from_id=db.Column(db.Integer,nullable=False)
    to_name=db.Column(db.String(32),nullable=False)
    cid=db.Column(db.Integer,nullable=False)
    content=db.Column(db.String(255),nullable=False)
    like_num=db.Column(db.Integer,default=0,nullable=False)
    time=db.Column(db.DateTime,nullable=False,default=datetime.now)
    to_id=db.Column(db.Integer,nullable=False)
    reply_id=db.Column(db.Integer,nullable=False)
    type=db.Column(db.Integer,nullable=False)
class Zan(db.Model):
    uid=db.Column(db.Integer,primary_key=True)
    article_id=db.Column(db.Integer,primary_key=True)
    type=db.Column(db.Integer)

