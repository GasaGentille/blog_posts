from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import Writer,Comment,Post
from .forms import UpdateProfile,PostForm,CommentForm
from flask_login import login_required,current_writer
from .. import db,photos
import markdown2 
import datetime


@main.route('/')
def index():
   '''
   View root page function that returns the index page and its data
   '''
 
   title = 'Home - Welcome to blog_posts website'

   return render_template('index.html', title = title)



@main.route('/writer/<uname>') 
def profile(uname):
    writer = Writer.query.filter_by(username = uname).first()
    pitches_count = Pitch.count_pitches(uname)

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


@main.route('/post/new', methods = ['GET','POST'])
@login_required
def new_post():
    post_form = PostForm()
    
    if post_form.validate_on_submit():
        title = post_form.title.data
        post = post_form.text.data
        
      
        #post instance
        new_post = Post(post_title=title,post_content=post,writer=current_writer)
        #save post
        print(new_post.post_title)
        new_post.save_post()
        return redirect(url_for('.index'))

    title = 'New post'
    return render_template('new_post.html',title = title,post_form = post_form)

@main.route('posts')

def posts():
    posts = Post.get_posts()
    
    return render_template("posts.html", posts = posts)


@main.route('/pitch/<int:id>', methods = ['GET','POST'])
def pitch(id):
    pitch = Pitch.get_pitch(id)

    if request.args.get("upvote"):
        pitch.upvotes = pitch.upvotes + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))

    elif request.args.get("downvote"):
        pitch.downvotes = pitch.downvotes + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))

    comment_form =  CommentForm()
    if comment_form.validate_on_submit():
        comment = comment_form.text.data

        new_comment = Comment(comment = comment,user = current_user,pitch_id=pitch)
        new_comment.save_comment()

    comments = Comment.get_comments(pitch)
    return render_template("pitch.html", pitch = pitch, comment_form = comment_form, comments = comments)

@main.route('/user/<uname>/pitches')
def user_pitches(uname):
    user = User.query.filter_by(username=uname).first()
    pitches = Pitch.query.filter_by(user_id=user.id).all()
    pitches_count = Pitch.count_pitches(uname)


    return render_template("profile/pitches.html", user=user,pitches=pitches,pitches_count=pitches_count)   
    


