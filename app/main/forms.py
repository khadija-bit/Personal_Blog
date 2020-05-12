from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required,Email
from ..models import User


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators =[Required()])
    email = StringField('Email',validators =[Required()])
    submit = SubmitField('Submit')    

class BlogForm(FlaskForm):
    title = StringField('blog title',validators = [Required()])
    content = TextAreaField('content',validators = [Required()])
    submit = SubmitField('Post')   

class CommentForm(FlaskForm):
    comment = TextAreaField('comment',validators = [Required()])
    submit = SubmitField('Add Comment') 


# class BlogForm(FlaskForm):
#     title = StringField('blog title',validators = [Required()])
#     content = TextAreaField('content',validators = [Required()])
#     submit = SubmitField('Post')     
