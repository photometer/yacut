from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URLForm(FlaskForm):
    original_link = URLField(
        'Long link',
        validators=[DataRequired(message='Required field'), ]
    )
    custom_id = StringField(
        'Your option for short link',
        validators=[Length(max=16), Optional()]
    )
    submit = SubmitField('Generate')
