from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import Writer,Comment,Post
from .forms import UpdateProfile,PostForm,CommentForm
from flask_login import login_required,current_user
from .. import db,photos
import markdown2 
import datetime


@main.route('/')
def index():
   '''
   View root page function that returns the index page and its data
   '''

   posts = Post.query.all()
 
   title = 'Home - Welcome to blog_posts website'

   return render_template('index.html', title = title , posts=posts)



@main.route('/writer/<uname>') 
def profile(uname):
    writer = Writer.query.filter_by(username = uname).first()
    posts_count = Post.count_posts(uname)

    if writer is None:
        abort(404)

    return render_template("profile/profile.html", writer = writer,posts = posts_count)

@main.route('/writer/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    writer = Writer.query.filter_by(username = uname).first()
    if writer is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        writer.bio = form.bio.data

        db.session.add(writer)
        db.session.commit()

        return redirect(url_for('.profile',uname=writer.username))

    return render_template('profile/update.html',form =form)

@main.route('/writer/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    writer = Writer.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        writer.profile_pic_path = path
        db.session.commit()
        return redirect(url_for('main.profile',uname=uname))

# CREATE POST
@main.route('/post/new', methods = ['GET','POST'])
@login_required
def new_post():
    post_form = PostForm()
    posts = Post.query.all()
    
    if post_form.validate_on_submit():
        post = Post(title = post_form.title.data, content = post_form.content.data , writer=current_user)

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('index.html'))

    title = 'New post'
    return render_template('new_post.html',title = title,post_form = post_form, legend = 'New Post',posts=posts)


@main.route('/post/<int:post_id>', methods = ['GET','POST'])
def post(post_id):
    post = Post.query.get(post_id)

    return render_template('post.html',title=post.title,post=post)

#    UPDATE POST
@main.route('/post/<int:post_id>/update', methods = ['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get(post_id)
    if post.author != current_writer:
        abort(404)

    post_form = PostForm()
    if post_form.validate_on_submit():
        post.title = post_form.title.data
        post.content = post_form.content.data 

        # db.session.add()
        db.session.commit()

        return redirect(url_for('post',post_id = post.id))
    elif request.method == 'GET':
        post_form.title.data =  post.title 
        post_form.content.data = post.content
    
    return render_template('new_post.html',title = 'Update Post',post_form = post_form,legend = 'Update Post')

  
@main.route('/post/<int:post_id>/delete', methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post.author != current_writer:
        abort(404)
    db.session.delete(post)
    db.session.commit()
    
    return redirect(url_for('.index'))



