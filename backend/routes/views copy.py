"""
This module contains controllers for normal HTML views
"""

from flask import Blueprint, request, redirect
import pandas as pd
from interfaces import *
from utils import render_view
from store import room_name

from wtforms import MultipleFileField, StringField, SubmitField
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.validators import DataRequired


normal_routes = Blueprint('normal_routes', __name__,
                          template_folder='templates')


class UploadForm(FlaskForm):
    files = MultipleFileField(
        'Files', validators=[FileRequired(), FileAllowed(['.csv', '.xlsx'])],
        render_kw={"hidden": True,
                   "accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,text/csv",
                   "x-ref": "upload_btn",
                   "x-on:change": "files=$event.target.files; console.log($event.target.files);"})
    room_name = StringField('Room name', validators=[DataRequired()],
                            render_kw={'Placeholder': "Enter room name"})
    submit = SubmitField('Upload')


@normal_routes.route('/')
def index():
    return render_view('index.html')


@normal_routes.route('/sad')
def sad():
    return '<p>Sad quá</p>'

@normal_routes.route('/haha')
def haha():
    form = UploadForm()
    return render_view('haha.html', form=form)


@normal_routes.route('/upload', methods=['POST'])
def upload():
    upload_files = request.files.getlist("file")
    print(request.form.get('room_name'))
    # for file in upload_files:
    #     if 'sheet' in file.mimetype:
    #         print(f'{file.filename} is an excel file')
    #     else:
    #         print(f'{file.filename} is a csv file')
    #         df = pd.read_csv(file)
    #         print(df.info())
    #     # df = pd.read_csv(file)
    #     # print(df.info())
    return redirect('/haha')
