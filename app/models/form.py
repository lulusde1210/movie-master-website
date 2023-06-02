from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CreateEditForm(FlaskForm):
    rating = StringField("Rating", validators=[DataRequired()])
    review = TextAreaField("Review", validators=[DataRequired()], render_kw={
                           'class': 'form-control', 'rows': 8})
    submit = SubmitField("Submit")


class CreateAddForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Search")
