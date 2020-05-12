from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import UpdateProfile,BlogForm,CommentForm
from flask_login import login_required,current_user
from ..models import User,Blog,Quotes,Subscirbe,Comment
from .. import db,photos
from ..requests import getQuotes

# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    quotes = getQuotes()
    blogs = Blog.query.all()
    title = 'Welcome to the blog'
    
    return render_template('index.html',title = title,quotes = quotes,blogs = blogs )


@main.route('/newblog',methods=['GET','POST'])
@login_required
def new_blog():
    
    form = BlogForm()
    if form.validate_on_submit():
        # blog = form.blog.data
        title = form.title.data
        content = form.content.data
        new_blog = Blog(title = title,content= content,user = current_user)
        db.session.add(new_blog)    
        db.session.commit()
        return redirect(url_for('.index'))
    title = 'Add a blog'    
    return render_template('new_post.html',title= title, blogform= form )

@main.route('/comment/<int:blog_id>',methods=['GET','POST'])
@login_required
def Comment(blog_id):
    current_blog = Blog.query.filter_by(id = blog_id).first()
    if request.method == "POST":
        comment = request.form.get('comment')
        new_comment = Comment(comment = comment,user= current_user,blog = current_blog)
        db.session.add(new_comment)
        db.session.commit()
    comments = Comment.get_omments(blog_id)
    title = 'comment'
    return render_template('comment.html',title= title,comments = comments)


@main.route('/newblog',methods=['GET','POST'])
@login_required
def Delete_blog(blog_id):
    current_blog = Blog.query,filter_by(id = blog_id).first()
    if current_blog.user != current_user:
        abort(403)
    db.session.delete(current_blog)    
    db.session.commit()
    return redirect(url_for('.index'))


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data
        user.email = form.email.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))