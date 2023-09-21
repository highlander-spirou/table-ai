from flask_wtf import FlaskForm
from wtforms import MultipleFileField, SubmitField
from flask_wtf.file import FileAllowed, FileRequired


class DataUpload(FlaskForm):
    files = MultipleFileField('File(s) Upload', validators=[FileRequired(), FileAllowed(['csv', 'xlsx'])])
    submit = SubmitField('Submit')