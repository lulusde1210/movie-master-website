from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CreateEditForm(FlaskForm):
    rating = StringField("New Rating", validators=[DataRequired()])
    review = StringField("Review", validators=[DataRequired()])
    submit = SubmitField("Submit")


class CreateAddForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Submit")
