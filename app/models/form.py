from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CreateEditForm(FlaskForm):
    rating = StringField("Rating", render_kw={
                         "placeholder": "Rate the movie(1-10)"}, validators=[DataRequired()])
    review = TextAreaField("Review", validators=[DataRequired()], render_kw={
                           'class': 'form-control', 'rows': 8, "placeholder": "Type your review"})
    submit = SubmitField("Submit", render_kw={'class': 'button'})


class CreateAddForm(FlaskForm):
    title = StringField("Movie Title", render_kw={
                        "placeholder": "Search by movie title"}, validators=[DataRequired()])
    submit = SubmitField("Search", render_kw={'class': 'button'})
