from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))

    blog = db.relationship('Blog',backref = 'user',lazy="dynamic")

    @property
    def password(self):
        '''
        raise error when someone try reading the password
        '''
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        '''
        Generate password hash
        '''
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        '''
        Confirm password is same as the password hash during login
        '''
        return check_password_hash(self.password_hash,password)
    

    def __repr__(self):
        return f'User {self.username}'

class Blog(db.Model):
    '''
    '''
    __tablename__ = 'blogs'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String,nullable=False)
    content = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False)
    posted = db.Column(db.DateTime,default=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def get_blogs(cls,blog_id):
        blog = Blog.query.filter_by(blog_id = blog_id).all()
        return blog

    def __repr__(self):
        return f'Blog {self.title}, Date it was posted: {self.posted}, content: {self.content}'


class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String(255))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False)
    blog_id = db.Column(db.Integer,db.ForeignKey('blogs.id'), nullable=False)
    posted = db.Column(db.DateTime,default=datetime.utcnow)


    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_comments(cls,blog_id):
        comments = Comment.query.filter_by(blog_id = blog_id).all()
        return comments

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"Comment:( {self.id})"   

class Subscirbe(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"Comment: {self.email}"       


class Quotes:
    def __init__(self,author,quote):
        '''
        Method to intialised the quote class
        '''
        self.author = author
        self.quote = quote
