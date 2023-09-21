"""
This module contains controllers for normal HTML views
"""

from typing import Any
from flask import Blueprint, request, redirect, flash
import pandas as pd
from interfaces import *
from utils import render_view, ensure_path_exist
from store import room_name

from wtforms import MultipleFileField, StringField, SubmitField
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.validators import DataRequired

from flask_wtf.file import FileAllowed
from markupsafe import Markup
from werkzeug.datastructures import FileStorage
from wtforms.fields import MultipleFileField, SubmitField
from wtforms.validators import InputRequired, StopValidation
from pathlib import Path

normal_routes = Blueprint('normal_routes', __name__,
                          template_folder='templates')


class MultiFileAllowed(object):
    def __init__(self, upload_set, message=None):
        self.upload_set = upload_set
        self.message = message

    def __get_file_ext(self, file_name):
        return Path(file_name).suffix

    def __call__(self, form, field):
        all_file_valid = all([self.__get_file_ext(
            i) in self.upload_set for i in field.data])
        if all_file_valid:
            return
        else:
            raise StopValidation('File type not match')


class CheckRoomIdExisted(object):
    def __init__(self, message=None):
        self.message = message

    def __check_room_exist(self, room_to_check):
        return room_to_check in room_name

    def __call__(self, form, field):
        if self.__check_room_exist(field.data):
            raise StopValidation('Duplicated room name')
        else:
            return


class UploadForm(FlaskForm):
    files = MultipleFileField('files', validators=[InputRequired(), MultiFileAllowed(['.csv', '.xlsx'])], render_kw={
                              "accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, text/csv"})
    room_name = StringField('Room name', validators=[
                            DataRequired(), CheckRoomIdExisted()])
    submit = SubmitField('Submit')


@normal_routes.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if request.method == 'POST':
        return redirect('/')
        # if form.validate_on_submit():
        #     upload_files = request.files.getlist("files")
        #     request_room_name = request.form.get('room_name')
        #     ensure_path_exist(f'./uploads/{request_room_name}')
        #     for file in upload_files:
        #         if 'sheet' in file.mimetype:
        #             df = pd.read_excel(file)
        #         else:
        #             df = pd.read_csv(file)
        #         df.to_csv(
        #             f'./uploads/{file.filename}.csv')
        #     return redirect('/dashboard')
        # else:
        #     flash('Room existed! Try another room name')
        #     return redirect('/')
    return render_view('index.html', form=form)


@normal_routes.route('/upload', methods=['POST'])
def upload():
    upload_files = request.files.getlist("files")
    print(request.files)
    # request_room_name = request.form.get('room_name')
    # if request_room_name in room_name:
    #     flash('Room existed! Try another room name')
    #     return redirect('/')

    # ensure_path_exist(f'./uploads/{request_room_name}')

    # for file in upload_files:
    #     print(file.filename)
    # if 'sheet' in file.mimetype:
    #     print(f'{file.filename} is an excel file')
    #     df = pd.read_excel(file)
    # else:
    #     print(f'{file.filename} is a csv file')
    #     df = pd.read_csv(file)
    # df.to_parquet(f'./uploads/{request_room_name}/{file.filename}.parquet.gzip', compression='gzip')

    return redirect('/')


@normal_routes.route('/dashboard')
def dashboard():
    return '<p>Dashboard</p>'
