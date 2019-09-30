from flask import render_template,redirect,url_for, flash,request
from . import auth
from flask_login import login_user,logout_user,login_required
from ..models import Writer
from .forms import LoginForm,RegistrationForm
from .. import db
from ..email import mail_message



@auth.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        writer = Writer.query.filter_by(email = login_form.email.data).first()
        if writer is not None and writer.verify_password(login_form.password.data):
            login_user(writer,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or Password')

    title = "blog_posts login"
    return render_template('auth/login.html',login_form = login_form,title=title)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

@auth.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        writer = Writer(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(writer)
        db.session.commit()
        mail_message("Successfully sign up to blog posts","email/welcome_writer",writer.email,writer=writer)
        return redirect(url_for('auth.login'))
        title = "New Account"
    return render_template('auth/register.html',registration_form = form)