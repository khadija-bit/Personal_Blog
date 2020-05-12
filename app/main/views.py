from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import UpdateProfile,BlogForm,CommentForm
from flask_login import login_required,current_user
from ..models import User,Blog,Quotes,Comment
from .. import db,photos
from ..requests import getQuotes


@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    quotes = getQuotes()
    blogs = Blog.query.all()
    title = 'Welcome to the blog'
    
    return render_template('index.html',title = title,quotes = quotes,blogs = blogs,current_user= current_user )


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
def new_comment(blog_id):
    form = CommentForm()
    blog = Blog.query.filter_by(id=blog_id).first()
    if form.validate_on_submit():
        comment = form.comment.data
        blog_id = blog_id
        new_comment = Comment(comment=comment,blog_id=blog_id,user_id = current_user.id)
        new_comment.save()
        return redirect(url_for('main.new_comment',blog_id=blog_id))
    comments = Comment.query.filter_by(blog_id=blog_id).all()    
    return render_template('comment.html',form=form,blog=blog,comments=comments)    

  

@main.route('/comment/',methods=['GET','POST'])
@login_required
def Delete_comment(blog_id):
    form = CommentForm()
    get_comments = Comment.query,filter_by(id = blog_id).first()
    
    db.session.delete(get_comment)    
    db.session.commit()
    return redirect(url_for('.index',form = form,blog = get_comments.blog_id))


@main.route('/newblog',methods=['GET','POST'])
@login_required
def Delete_blog(blog_id):
    form = BlogForm()
    get_blogs = Blog.query,filter_by(id = blog_id).first()
    
    db.session.delete(get_comment)    
    db.session.commit()
    return redirect(url_for('.index',form = form,blog = get_blogs))


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