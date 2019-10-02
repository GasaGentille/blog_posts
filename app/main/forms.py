from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required, Email
from ..models import Subscription



class UpdateProfile(FlaskForm):
   bio = TextAreaField('Tell us about you.',validators = [Required()])
   submit = SubmitField('Submit')
   submit = SubmitField('Submit')
class CommentForm(FlaskForm):
    comment = TextAreaField('Leave a comment:',validators = [Required()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    title = StringField('Title')
    content = TextAreaField('Content')
    submit = SubmitField('Post')

class SubscriptionForm(FlaskForm):
    name = StringField('Name', validators = [Required()])
    email = StringField('Email',validators=[Required(),Email()])
    submit = SubmitField('submit')

    def validate_email(self,data_field):
        if Subscription.query.filter_by(email =data_field.data).first():
            raise ValidationError('There is an account with that email')

    def validate_name(self,data_field):
        if Subscription.query.filter_by(name = data_field.data).first():
            raise ValidationError('That name is taken')
