from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import Writer,Comment,Post,Quotes,Comment,Subscription
from .forms import UpdateProfile,PostForm,CommentForm,SubscriptionForm
from flask_login import login_required,current_user
from .. import db,photos
import markdown2 
from ..request import get_quotes


@main.route('/' ,methods = ['GET','POST'])
def index():
   '''
   View root page function that returns the index page and its data
   '''
   quote = get_quotes()
#    comments = Comment.get_comments(id)
   posts = Post.query.all()

   title = 'Home - Welcome to blog_posts website'
   form = SubscriptionForm()
   if form.validate_on_submit():
       name = form.name.data
       email = form.email.data

       subscriber = Subscription(name=name,email=email)
       db.session.add(subscriber)
       db.session.commit()

       return redirect(url_for('.index'))
       mail_message("Welcome to blog posts","subscriber/subscriber_user",subscriber.email,subscriber = subscriber)

   return render_template('index.html', title = title , posts=posts,quote=quote, form = form)



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
    writer = Writer.query.filter_by(id=current_user.id).first()
    comments = Comment.query.filter_by(post_id = id).first()
    print(post_form.validate_on_submit())
    
    if post_form.validate_on_submit():
       

        post = Post(post_title = post_form.title.data, post_content = post_form.content.data , writer_id=current_user.id)

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('.index'))

    title = 'New post'
    return render_template('new_post.html', post_form = post_form, writer=writer, comments=comments)


@main.route('/post/<int:post_id>', methods = ['GET','POST'])
def post(post_id):
    post = Post.query.get(post_id)

    return render_template('post.html',title=post.title,post=post)

#    UPDATE POST
@main.route('/post/<int:post_id>/update', methods = ['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get(post_id)
    if post is None:
        abort(404)

    post_form = PostForm()
    if post_form.validate_on_submit():
        Post.query.filter_by(id=post_id).update({"post_title": post_form.title.data, "post_content": post_form.content.data})
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('.index'))
   
    
    return render_template('new_post.html',title = 'Update Post',post_form = post_form)

  
@main.route('/post/<int:post_id>/delete', methods = ['GET','POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    post_form = PostForm()
  
    if post_form.validate_on_submit():
        post.title = post_form.title.data
        post.content = post_form.content.data 

    db.session.delete(post)
    db.session.commit()
    
    return redirect(url_for('.index'))
@main.route("/comment/<int:post_id>/create",methods = ['GET','POST'])
def comment(post_id):
    form = CommentForm()
    comments = Comment.query.filter_by(post_id=post_id).all()
    posts = Post.query.get(post_id)

    title=f'Write a comment'

    if form.validate_on_submit():
        comment = form.comment.data
        post_id = post_id

        new_comment = Comment(comment = comment,post_id = post_id)
        new_comment.save_comment()
        
        return redirect(url_for('.index'))
    return render_template("comment.html", posts = posts, comments = comments, form= form)

@main.route("/index/<int:id>/delete_comment")
@login_required
def delete_comment(id):
    available_post = Comment.query.filter_by(id=id).first()
    print(available_post)
    if available_post is None:
        abort(404)
    db.session.delete(available_post)
    db.session.commit()

    return redirect(url_for('.index'))
    # return render_template('comment.html')




    



