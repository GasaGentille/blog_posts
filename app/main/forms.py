from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required



class UpdateProfile(FlaskForm):
   bio = TextAreaField('Tell us about you.',validators = [Required()])
   submit = SubmitField('Submit')
   submit = SubmitField('Submit')
class CommentForm(FlaskForm):
    text = TextAreaField('Leave a comment:',validators = [Required()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    title = StringField('Title')
    content = TextAreaField('Content')
    submit = SubmitField('Post')
